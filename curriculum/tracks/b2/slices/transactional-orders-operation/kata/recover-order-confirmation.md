---
id: b2.kata.recover-order-confirmation
kind: kata
title: Kata — восстановить подтверждение заказа после commit
owner_track: b2
module: b2.module.transactional-persistence-integration
coverage:
  - target: b2.level-outcome.manage-application-transaction-boundaries-l1-use-defined-unit
    role: practice
  - target: b2.level-outcome.manage-application-transaction-boundaries-l1-use-defined-unit
    role: assess
  - target: b2.level-outcome.manage-application-transaction-boundaries-l2-design-operation-boundary
    role: practice
  - target: b2.level-outcome.manage-application-transaction-boundaries-l2-design-operation-boundary
    role: assess
  - target: b2.level-outcome.design-idempotent-service-operations-l2-implement-known-pattern
    role: practice
  - target: b2.level-outcome.design-idempotent-service-operations-l2-implement-known-pattern
    role: assess
status: accepted
updated: 2026-08-24
language: ru
last_verified: 2026-08-21
versions:
  postgresql: 18.6
  psycopg: 3.3.4
---

# Kata: восстановить подтверждение заказа после commit

## Рабочая история

Orders service подтверждает draft order и должен сообщить внешнему приёмнику событий (`event sink`, далее sink) о `OrderConfirmed`. Раньше handler сначала выполнял commit, затем сразу вызывал sink. Во время рестарта процесс упал в промежутке: клиент получил подтверждение, но событие не было отправлено, а способа найти потерянную работу нет.

Новое требование: после подтверждённого commit и падения до первой публикации restart обязан обнаружить незавершённое событие. Повтор той же command не должен создавать второе подтверждение.

Стартового scaffold и готового repository нет. Создайте минимальную систему самостоятельно. Не копируйте production framework: достаточно PostgreSQL 18.6, Psycopg 3.3.4, command-функции, управляемого event sink double и воспроизводимого fault hook.

## Зафиксированный контракт

- Command: `POST /orders/{order_id}/confirm` с UUID `Idempotency-Key`.
- Тело request пустое; успешный `200` содержит `operation_id`, `order_id` и `status="confirmed"`.
- Отпечаток запроса (`request fingerprint`): method + `order_id`; полный result хранится 24 часа, после чего маркер истёкшего key (`tombstone`) запрещает новую мутацию с тем же key.
- Одинаковые key/fingerprint возвращают тот же status/body; другой fingerprint — `409 idempotency_conflict`.
- `orders`, `operation_results` и `order_events` меняются одним `with conn.transaction():` на autocommit connection.
- `READ COMMITTED`, `fsync=on`, `synchronous_commit=on`.
- Publisher вызывает sink вне database transaction и передаёт устойчивый `event_id`.
- `OrderConfirmed` содержит `event_id`, `event_type="OrderConfirmed"`, `operation_id`, `order_id` и `confirmed_at`.

Повтор с возвратом ранее сохранённого результата (`replay`) использует тот же key/fingerprint и не начинает новую мутацию.

Kata исследует ровно одно основное окно отказа F2 (`crash window`): **database commit подтверждён, но процесс останавливается до первого вызова sink**. Unknown commit, отказ после publish до marking и общая доставка входят в project, не в эту задачу.

## Сначала запишите ожидаемое

До кода сохраните короткий файл с тремя invariants и таблицей наблюдений:

1. confirmed order, operation result и event record durable вместе либо отсутствуют вместе;
2. после restart committed pending event снова обнаружим;
3. повтор с тем же key воспроизводит result и не создаёт второй business transition/event record.

Для каждого этапа укажите ожидаемые значения: order status, число operation results, число event records, publish state, число sink calls и `event_id`.

## Ограниченная задача

1. Создайте минимальные tables/constraints, достаточные для контракта.
2. Реализуйте confirm command с явной короткой transaction boundary.
3. Добавьте детерминированную точку инъекции отказа (`fault hook`) `after_commit_before_publish`, которая завершает command path после подтверждённого commit и до первого sink call.
4. Перезапустите только application/publisher process, не очищая PostgreSQL.
5. Реализуйте минимальный recovery path, находящий pending event и отправляющий его.
6. Повторите исходную command с тем же key и сравните сохранённый result.

Способ организации кода, SQL и запуска выбирает участник. Fault hook может быть callback, process barrier или отдельная команда, но обязан срабатывать в названной точке и не подменять commit моками.

## Failure/measurement envelope

Используйте один draft order, один operation key и один event. Выполните не менее 10 независимых прогонов с очисткой fixture между ними:

- 5 контрольных прогонов без fault;
- 5 прогонов с `after_commit_before_publish`, restart и recovery.

В каждом прогоне наблюдайте authoritative PostgreSQL и sink log. Acceptance threshold: во всех 10 прогонах ровно один переход заказа, один operation result и один event record; в fault-прогонах до restart sink calls = 0, после recovery sink содержит исходный `event_id`; replay возвращает исходный status/body. Время не является SLO — число прогонов проверяет воспроизводимость fault hook.

Отдельно от этих десяти основных F2-прогонов выполните ещё три детерминированные проверки — ровно по одному обязательному прогону на case:

- тот же key с другим fingerprint возвращает `409 idempotency_conflict` без мутации;
- новый key для уже подтверждённого заказа возвращает `409 order_not_draft` без второго transition/event;
- после управляемого перевода clock за границу retention тело результата недоступно, tombstone возвращает `409 idempotency_key_expired` без мутации.

Эти три проверки идут сверх десяти основных прогонов и уточняют L2-контракт; они не превращают kata в L3 project.

## Acceptance criteria

- [ ] Invariants и expected observations записаны до реализации.
- [ ] Success commit делает order/result/event record видимыми вместе.
- [ ] Инъекция происходит только после полученного подтверждения commit и до первого sink call.
- [ ] До restart event остаётся `pending`, а sink пуст.
- [ ] После restart recovery находит record без повторной command и отправляет тот же `event_id`.
- [ ] Replay с тем же key/fingerprint возвращает исходный result.
- [ ] Тот же key с другим `order_id` даёт `409 idempotency_conflict` без мутации.
- [ ] После управляемого expiry тот же key даёт `409 idempotency_key_expired` без мутации.
- [ ] Новый key для confirmed order не создаёт второй transition/event.
- [ ] Network I/O отсутствует внутри transaction.
- [ ] Все 10 прогонов удовлетворяют объявленному threshold; raw summary сохранён.
- [ ] Нет готового solution code, distributed transaction, caching или exactly-once claim.

Эти критерии практикуют Transaction L1/L2 и Idempotency L2. Они не заявляют L3: kata не исследует unknown commit, publish-before-marking race и полный concurrent duplicate experiment.

## Что принести на разбор

- формулировки invariants до кода;
- минимальную схему и объяснение unique constraints;
- команду воспроизведения контрольного и fault профилей;
- state snapshots до fault, после commit/crash и после recovery;
- результаты replay/conflict cases;
- raw summary 10 прогонов;
- один абзац об остаточном риске duplicate send после sink acceptance.

## Progressive hints

<details>
<summary>Подсказка 1 — где искать durable работу</summary>

Если единственное знание о будущей публикации живёт в памяти процесса, restart его потеряет. Подумайте, какая запись должна коммититься вместе с заказом.

</details>

<details>
<summary>Подсказка 2 — где поставить fault</summary>

Fault должен срабатывать только после успешного выхода из transaction context. Если он стоит перед commit или заменяет database response, вы проверяете другой failure window.

</details>

<details>
<summary>Подсказка 3 — как распознать повтор command</summary>

Стабильная identity и unique constraint должны привести повтор к сохранённому result. Проверка только `orders.status` не различает replay и случайно выполненную новую command.

</details>

<details>
<summary>Подсказка 4 — почему это ещё не exactly-once</summary>

Добавьте мысленный crash после того, как sink принял event, но до DB marking. Recovery увидит pending record и отправит его снова. Kata не реализует этот профиль, но итоговое объяснение обязано назвать его.

</details>

## Вопросы самопроверки

### Почему clean shutdown вместо fault hook — слабое доказательство?

<details>
<summary>Ответ и объяснение</summary>

Clean shutdown может успеть выполнить publication или cleanup и не воспроизводит выбранное окно. Детерминированный hook фиксирует состояние после confirmed commit и до первого send, поэтому наблюдение относится к нужному механизму.

</details>

### Что доказывает replay, чего не доказывает restart publisher?

<details>
<summary>Ответ и объяснение</summary>

Replay проверяет operation identity и сохранённый result. Restart publisher проверяет обнаружимость pending event. Publisher может восстановиться при неправильно созданном втором business transition, поэтому сигналы различаются.

</details>

## Non-goals

- готовый scaffold, структура файлов или эталонная реализация;
- unknown commit и разрыв DB connection;
- crash после sink acceptance до marking;
- конкурентный stress test нескольких retries;
- production broker, 2PC, saga, consensus или общая delivery theory;
- performance SLO и deployment automation.

Связанный разбор: [граница транзакции и окна отказа](../learn/transaction-boundary-failure-windows.md).
