---
id: b2.index.recoverable-order-confirmed-consumer
kind: index
title: Восстановление consumer после commit до acknowledgement
owner_track: b2
module: b2.module.background-message-workflows
coverage:
  - target: b2.capability.design-asynchronous-workflows
    role: reference
status: accepted
updated: 2026-08-26
language: ru
last_verified: 2026-08-25
versions:
  rabbitmq: 4.3.5
  aio-pika: 10.0.1
  postgresql: 18.6
  psycopg: 3.3.4
---

# Восстановление consumer после commit до acknowledgement

Worker получает `OrderConfirmed`, создаёт заявку на исполнение заказа и успевает сохранить её в PostgreSQL. Затем процесс падает прежде, чем RabbitMQ получает подтверждение обработки (`consumer acknowledgement`, далее ack). После рестарта broker доставляет то же событие снова. Это нормальное следствие незавершённого delivery, но без явной границы состояния оно легко превращается во вторую заявку.

Повторная доставка не равна второму бизнес-результату. Delivery — попытка broker-а передать сообщение, `event_id` — identity события, а строка `fulfillment_requests` — результат consumer. Уникальный `source_event_id` связывает повторные deliveries с одним результатом; ack отправляется лишь после commit или после чтения уже существующего результата.

## Зафиксированный substrate

- RabbitMQ 4.3.5; durable quorum queue `orders.fulfillment`, `prefetch_count=1`.
- `aio-pika` 10.0.1; `Queue.consume(no_ack=False)`, явные `ack(multiple=False)` и `reject(requeue=True)`.
- PostgreSQL 18.6 и Psycopg 3.3.4 из принятого S07 baseline.
- `fulfillment_requests(source_event_id UNIQUE, ...)` — единственный business side effect.
- Source queue имеет `delivery-limit=3`; после превышения limit persistent message переносится с гарантией `at-least-once` через обменник недоставленных сообщений (`dead-letter exchange`, далее DLX) в durable quorum queue `orders.fulfillment.poison`.

Точные решения и первичные источники записаны в [B5/broker readiness record](../../../../../governance/work-packages/M1.8.7-background-message-workflows-s09-slice.md#gate-0--b5broker-readiness-record).

## Маршрут

1. [Engineering brief](learn/acknowledgement-redelivery-recovery-boundary.md) — построить модель границы commit/ack, redelivery, duplicate и poison transition.
2. [Interview](interview/side-effect-committed-message-unacked.md) — пройти от реализации заданного flow к проектированию наблюдаемого recovery.
3. [Kata](kata/recover-order-confirmed-consumer.md) — самостоятельно воспроизвести один crash window после commit и до ack.
4. [Project specification](project-spec/resilient-fulfillment-consumer.md) — проверить несколько fault points того же workflow на реальных RabbitMQ и PostgreSQL.

## Ожидаемый результат

Инженер умеет назначить владельца ack, retry и ошибки; описать состояния одного consumer workflow; воспроизвести crash/redelivery/restart; доказать не более одной заявки на `event_id`; завершить постоянно невалидное сообщение в наблюдаемом poison outcome без бесконечного requeue.

## Предварительный контекст и границы

[S07](../transactional-orders-operation/README.md) уже задаёт устойчивый `event_id` и producer-side публикацию. [R1](../runtime-concurrency-lifecycle/learn/cancellation-deadlines-resource-lifecycle.md) объясняет управляемую остановку, а [V1](../risk-based-service-verification/learn/truthful-test-boundaries.md) — выбор проверки по риску и механизму. Здесь эти темы не преподаются повторно.

Срез не обещает exactly-once delivery, не проектирует producer outbox, общий graceful shutdown, transaction isolation, универсальный inbox/DLQ, ordering, saga, consensus, orchestration platform или migration нескольких команд. Он рассматривает одного consumer, одну source queue, одно событие и один business side effect.
