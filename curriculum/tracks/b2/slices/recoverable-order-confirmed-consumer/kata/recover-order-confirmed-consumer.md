---
id: b2.kata.recover-order-confirmed-consumer
kind: kata
title: Kata — восстановить OrderConfirmed consumer после commit
owner_track: b2
module: b2.module.background-message-workflows
coverage:
  - target: b2.level-outcome.design-asynchronous-workflows-l2-implement-background-flow
    role: practice
  - target: b2.level-outcome.design-asynchronous-workflows-l2-implement-background-flow
    role: assess
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

# Kata: восстановить OrderConfirmed consumer после commit

## Рабочая история

Fulfillment worker получает `OrderConfirmed`, создаёт заявку на исполнение заказа и ack-ает message. Во время deployment process остановился после PostgreSQL commit, но до ack. После restart RabbitMQ redeliver-ил событие, и прежний handler попытался создать вторую заявку.

Новое требование: повторная доставка того же `event_id` должна завершить workflow с одной заявкой. Участник сам создаёт минимальную систему; стартового scaffold, repository и готового решения нет.

## Закреплённый substrate

- RabbitMQ 4.3.5, durable quorum queue `orders.fulfillment`, persistent message, `prefetch_count=1`.
- `aio-pika` 10.0.1, `consume(no_ack=False)`, explicit `ack(multiple=False)`.
- PostgreSQL 18.6, Psycopg 3.3.4, одна таблица результата с unique `source_event_id`.
- Event: `event_id`, `event_type="OrderConfirmed"`, `operation_id`, `order_id`, `confirmed_at`.

Kata исследует ровно одно заранее внедрённое и управляемое окно отказа (`seeded`): **`fulfillment_request` committed, ack ещё не отправлен**. Poison/DLX, producer recovery, unknown database commit и общий graceful shutdown не становятся реализационными задачами.

## Сначала запишите ожидаемое

До кода сформулируйте:

1. business-result invariant для одного `event_id`;
2. точку ack относительно commit и duplicate lookup;
3. ожидаемые delivery, database и queue observations до crash и после restart;
4. почему результат не означает exactly-once delivery.

## Ограниченная задача

1. Создайте минимального consumer и таблицу `fulfillment_requests`, поддерживающую один result на `source_event_id`.
2. Добавьте одноразовый fault hook для выбранного `event_id`: после подтверждённого commit записать marker `after_commit_before_ack` и немедленно завершить process с code 70.
3. Опубликуйте одно persistent `OrderConfirmed` и запустите consumer с hook.
4. Убедитесь, что row существует, process завершён, ack не выполнен.
5. Перезапустите consumer без повторного hook. Он должен обработать redelivery, найти прежний result и ack-нуть текущий delivery.
6. Снимите доказательства, не полагаясь только на application log.

Не предоставляйте готовый handler в отчёте kata: принесите собственный код и наблюдения.

## Failure/measurement envelope

- Population: 10 независимых прогонов, новый `event_id` и чистая бизнес-строка на каждый.
- Load: одно message на прогон, один consumer, `prefetch_count=1`.
- Duration: не более 30 секунд от первой доставки до terminal state.
- Fault: process exit после commit, до вызова ack.
- Measurement: внешний fault marker; delivery log; SQL count/result id; source `messages_ready` и `messages_unacknowledged`.
- Acceptance threshold: 10/10 — marker присутствует, delivery наблюдается минимум дважды, row ровно одна и с тем же id, source counters завершаются `0/0`.
- Control: один прогон без hook — одна row и terminal source state.
- Recovery: новый process, без ручного изменения queue или database.

Время обнаружения потерянного connection не фиксировано; 30 секунд — лабораторный timeout, а не broker guarantee.

## Acceptance criteria

- Ack не может выполниться до confirmed commit или duplicate lookup.
- Повторный delivery не создаёт новую row и возвращается к прежнему result.
- Fault hook действительно обходит exception handler и graceful shutdown.
- Каждый из 10 прогонов сохраняет invariant и достигает terminal source state.
- Отчёт различает `event_id`, delivery context и business result id.
- Есть control observation и объяснённый residual risk.
- Решение не содержит второго workflow, producer outbox или готового DLQ curriculum.

## Что принести на разбор

- записанный invariant и короткая timeline;
- способ воспроизведения crash и доказательство точки fault;
- таблицу 10 прогонов: event id, delivery observations, result id/count, final queue counters;
- один control run;
- объяснение, почему unique constraint без duplicate-read path недостаточен;
- ссылку на [poison boundary brief](../learn/acknowledgement-redelivery-recovery-boundary.md#одна-delivery-model) без реализации poison task.

## Progressive hints

<details>
<summary>Подсказка 1 — identity</summary>

Не ищите стабильность в delivery tag. Какая часть `OrderConfirmed` остаётся одинаковой после reconnect?

</details>

<details>
<summary>Подсказка 2 — порядок</summary>

Разделите «business result durable» и «broker получил ack». Какое наблюдение должно предшествовать ack?

</details>

<details>
<summary>Подсказка 3 — duplicate</summary>

Unique constraint предотвращает вторую вставку, но handler ещё должен определить прежний result и завершить текущий delivery.

</details>

<details>
<summary>Подсказка 4 — настоящий crash</summary>

Exception может пройти через cleanup и reject. Нужен process-level exit после внешне наблюдаемого marker.

</details>

## Самопроверка

### Почему два вызова handler в одном process — слабее crash/restart?

<details>
<summary>Ответ и объяснение</summary>

Они проверяют duplicate business logic, но обходят RabbitMQ automatic requeue при потере connection и восстановление consumer. Kata требует причинную цепочку commit → process exit → unacked requeue → новый process.

</details>

### Почему unique violation нельзя просто считать success?

<details>
<summary>Ответ и объяснение</summary>

Нужно прочитать row по `source_event_id` и убедиться, что она представляет ожидаемый прежний result. Иначе handler скрывает конфликт данных и ack-ает message без доказанного business outcome.

</details>

## Non-goals

Poison implementation, delayed retry, producer publication, transaction theory, performance test, cluster failover, ordering, multiple consumers, graceful shutdown, ImplementationReference и production-ready scaffold.
