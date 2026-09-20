---
id: b2.index.transactional-orders-operation
kind: index
title: Транзакционное подтверждение заказа и восстановление публикации
owner_track: b2
module: b2.module.transactional-persistence-integration
coverage:
  - target: b2.capability.manage-application-transaction-boundaries
    role: reference
  - target: b2.capability.design-idempotent-service-operations
    role: reference
status: accepted
updated: 2026-08-24
language: ru
last_verified: 2026-08-21
versions:
  postgresql: 18.6
  psycopg: 3.3.4
---

# Транзакционное подтверждение заказа и восстановление публикации

Orders service подтверждает заказ через `POST /orders/{order_id}/confirm`. Клиент может увидеть успешный ответ только после записи результата в PostgreSQL, но событие `OrderConfirmed` отправляет отдельный процесс публикации (`publisher`, далее publisher). Поэтому «database commit прошёл» означает лишь, что состояние заказа и намерение публикации зафиксированы вместе. Это ещё не доказывает, что внешний приёмник событий (`event sink`, далее sink) получил событие.

Если процесс упадёт после commit и до publish, заказ уже `confirmed`, а подписчики пока ничего не знают. Если он упадёт после publish и до отметки об отправке, событие может быть послано повторно. Цена слабой модели — потерянное событие, повторная обработка или второй бизнес-результат после слепого retry.

## Зафиксированный substrate

- PostgreSQL 18.6, `READ COMMITTED`, `fsync=on`, `synchronous_commit=on`.
- Psycopg 3.3.4; autocommit-соединение и один внешний `with conn.transaction():` на command.
- Клиент передаёт UUID в `Idempotency-Key`: это идентификатор операции (`operation identity`). Отпечаток запроса (`request fingerprint`) включает HTTP method и `order_id`.
- Тело request пустое. Успешный `200` содержит `operation_id`, `order_id` и `status="confirmed"`; событие содержит `event_id`, `event_type="OrderConfirmed"`, `operation_id`, `order_id` и `confirmed_at`.
- Одинаковые key и fingerprint в течение 24 часов возвращают сохранённые HTTP status/body. Тот же key с другим fingerprint даёт `409 idempotency_conflict`.
- В одной transaction изменяются `orders`, сохраняется `operation_results` и создаётся один `order_events` с устойчивым `event_id`.
- Publisher читает committed event records и вызывает внешний sink вне database transaction. Повторная отправка допустима; sink должен уметь распознавать `event_id` либо принять риск duplicate delivery.

После истечения 24 часов полное тело результата можно удалить, но строка identity остаётся как маркер истёкшего key (`tombstone`). Тот же key получает `409 idempotency_key_expired` и никогда не начинает новую мутацию. Новый key для уже подтверждённого заказа получает `409 order_not_draft`; второй event record не создаётся.

## Четыре контрольные точки

1. **До commit:** исключение откатывает заказ, result и event record вместе.
2. **Во время commit:** потеря DB-соединения оставляет исход неизвестным приложению; broken connection не переиспользуется, а retry с тем же key сверяет durable result через новое соединение.
3. **После подтверждённого commit, до publish:** durable event record остаётся обнаружимым после рестарта.
4. **После publish, до marking:** publisher может отправить тот же `event_id` снова; это неизвестный исход публикации, а не неизвестный исход database commit.

Точки 1–4 соответствуют F0–F3 в project specification. Kata из этого маршрута работает только с F2: commit уже подтверждён, а первая публикация ещё не началась.

## Маршрут

1. [Engineering brief](learn/transaction-boundary-failure-windows.md) — построить ментальную модель границы database transaction, восстановления и инвариантов идемпотентности.
2. [Interview](interview/commit-succeeded-event-unknown.md) — проверить reasoning от заданной unit of work до двух разных L3-наблюдений.
3. [Kata](kata/recover-order-confirmation.md) — воспроизвести одно окно отказа (`crash window`): commit подтверждён, первой публикации ещё не было.
4. [Project specification](project-spec/resilient-order-confirmation.md) — самостоятельно проверить несколько fault points на реальном PostgreSQL.

Предварительно полезны [application operation и направление зависимостей S06](../service-architecture-boundaries/learn/change-isolation-service-boundaries.md), [контекст повторяемой command S04](../../scenarios.md) и [выбор правдивой границы проверки S10](../risk-based-service-verification/learn/truthful-test-boundaries.md).

## Ожидаемый результат

Инженер умеет очертить transaction одной application operation, не удерживает её через внешний network I/O, различает неизвестный commit и неизвестный publish, перечисляет failure windows и подтверждает разными наблюдениями:

- transaction/recovery invariant — заказ и event record durable вместе, а незавершённая публикация восстанавливается;
- инвариант идемпотентности — key имеет явные правила результата, конфликта и хранения, а конкурентный дубликат и повтор с возвратом ранее сохранённого результата (`replay`) не создают второй бизнес-результат.

## Границы

Срез применяет свойства PostgreSQL и Psycopg, но не преподаёт MVCC, WAL internals, taxonomy аномалий или выбор СУБД. Термины partial failure, duplicate delivery и reconciliation используются только для S07; здесь нет курса distributed commit, saga/consensus, общей теории delivery guarantees, caching/S15 или обещания exactly-once.

Версионные допущения подтверждены в [B3 readiness record](../../../../../governance/work-packages/M1.8.5-transactional-persistence-s07-slice.md#b3-readiness-record) по официальной документации PostgreSQL и Psycopg 2026-08-21.
