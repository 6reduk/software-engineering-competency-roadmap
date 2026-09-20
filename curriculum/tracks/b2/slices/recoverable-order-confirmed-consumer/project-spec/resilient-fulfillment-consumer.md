---
id: b2.project-spec.resilient-fulfillment-consumer
kind: project-spec
title: Проектная спецификация — восстанавливаемый fulfillment consumer
owner_track: b2
module: b2.module.background-message-workflows
coverage:
  - target: b2.level-outcome.design-asynchronous-workflows-l2-implement-background-flow
    role: integrate
  - target: b2.level-outcome.design-asynchronous-workflows-l2-implement-background-flow
    role: assess
  - target: b2.level-outcome.design-asynchronous-workflows-l3-design-recoverable-workflow
    role: integrate
  - target: b2.level-outcome.design-asynchronous-workflows-l3-design-recoverable-workflow
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

# Проектная спецификация: восстанавливаемый fulfillment consumer

## Рабочая ситуация

Fulfillment service превращает `OrderConfirmed` в заявку на исполнение. Команда видела три разных симптома: заявку потеряли из-за раннего ack; после crash появилась вторая заявка; permanently invalid message непрерывно возвращалось в source queue. Нужен один consumer workflow с наблюдаемыми состояниями, границей commit/ack и конечным poison outcome.

В отдельном репозитории выполните один milestone на реальных RabbitMQ 4.3.5 и PostgreSQL 18.6. Спецификация задаёт предметный контракт и evidence, но не диктует архитектуру, SQL, framework или готовый handler.

## Неизменяемый контракт

- Один persistent `OrderConfirmed(event_id, event_type, operation_id, order_id, confirmed_at)`; `event_type="OrderConfirmed"`.
- Один `aio-pika` 10.0.1 consumer читает durable quorum queue `orders.fulfillment` с manual ack и `prefetch_count=1`.
- Один business side effect — `fulfillment_requests` с unique `source_event_id`.
- Ack выполняется только после confirmed commit либо чтения прежнего result.
- Ошибка возвращается только через `reject(requeue=True)`.
- Source policy: `delivery-limit=3`, `dead-letter-exchange=orders.fulfillment.dlx`, routing key `orders.fulfillment.poison`, `dead-letter-strategy=at-least-once`, `overflow=reject-publish`.
- Poison target — durable quorum queue `orders.fulfillment.poison`; source message persistent.

## Один milestone и deliverables

1. Рабочий consumer, воспроизводимые start/stop/restart commands и реальный PostgreSQL store.
2. Явные business-result, acknowledgement, recovery и poison invariants.
3. Детерминированные hooks для четырёх fault points ниже.
4. State observer: event/delivery log, business row, source counters, poison message и dead-letter reason.
5. Автоматизированные evidence profiles и таблица результатов.
6. Короткий decision record о границе commit/ack, identity и retry ownership.

## Обязательные fault points

| ID | Fault point | Ожидаемое поведение |
|---|---|---|
| F0 | После delivery, до database commit | Row отсутствует; unacked delivery возвращается; следующий attempt может создать одну row |
| F1 | После confirmed commit, до ack | Row существует; restart получает redelivery и возвращается к той же row |
| F2 | После duplicate detection, до ack | Row не меняется; следующий delivery снова подтверждает прежний result |
| F3 | Permanently invalid message | Row отсутствует; failed deliveries ограничены, message достигает poison queue |

F0–F2 используют process-level exit без graceful cleanup. F3 использует закреплённый `reject(requeue=True)`, а не альтернативный nack/republish algorithm.

## Evidence A — Workflow L2

Покажите, что заданный flow реализован с явным ownership:

- handler классифицирует normal/duplicate/transient/invalid outcomes;
- PostgreSQL владеет durable business result;
- consumer владеет моментом ack/reject;
- RabbitMQ policy владеет failed-delivery limit и poison transition;
- normal и duplicate завершаются ack после доказанного result;
- invalid message не образует бесконечный source requeue.

Review проверяет поведение, а не наличие классов с именами `RetryPolicy` или `Inbox`.

## Evidence B — Workflow L3

До реализации задайте states и разрешённые transitions. Затем для F0–F2 сопоставьте каждую timeline с business-result, acknowledgement и recovery invariants. Доказательство должно показать, что replay/redelivery после restart не нарушает business result и не требует ручной правки.

Отдельно объясните неопределённость после вызова `ack()`: `aio-pika` не получает broker response на consumer ack, поэтому correctness переживает как terminal ack, так и ещё одну redelivery.

## Measurement envelope

### Recovery profile

- 10 изолированных прогонов для каждого F0, F1 и F2; новый `event_id` на прогон.
- Одно message, один consumer, `prefetch_count=1`, 30 секунд до terminal observation.
- F0: final row count 1, source `0/0`, poison 0 в 10/10.
- F1/F2: минимум две delivery observations, final row count 1 и прежний result id, source `0/0`, poison 0 в 10/10.
- Fault marker обязан подтверждать точку exit до ack.

### Control profile

- 10 valid events без fault.
- Для каждого — одна business row; source в terminal state. Число deliveries записывается, но не превращается в exactly-once assertion.

### Poison profile

- 10 permanently invalid events, по одному на изолированный прогон.
- Не более 30 секунд на достижение observable terminal state.
- В 10/10 source `0/0`, business row 0, poison queue содержит соответствующий message и reason `delivery_limit`.
- Если DLX target недоступен, профиль обязан показать retained/dead-letter-pending source state и считаться незавершённым, а не зелёным.

Эти пороги лабораторные и относятся только к закреплённому substrate; они не являются production SLO.

## Decision record

Зафиксируйте:

1. почему `event_id`, delivery context и business result id различаются;
2. почему ack расположен после durable result;
3. как duplicate возвращается к тому же result;
4. почему выбран `reject(requeue=True)`, а `nack(requeue=True)` отвергнут для RabbitMQ 4.3 delivery counter;
5. кто владеет transient/invalid classification, retry limit и poison observation;
6. что именно доказано и какие risks остались.

Не добавляйте альтернативный broker, queue type или retry/DLQ scheme.

## Review criteria

### Workflow L2 — implement background flow

- Один event/consumer/source queue/business side effect соблюдены.
- Ack/reject/error ownership видимы в коде и evidence.
- Duplicate path возвращает прежний result.
- Poison transition bounded и наблюдаем с обеих queue sides.

### Workflow L3 — design recoverable workflow

- States/transitions и четыре invariants записаны до результатов.
- F0–F2 воспроизводят разные causal windows, а не один exception с разными labels.
- Recovery завершается новым process без ручного queue/database repair.
- Measurement различает control, failure и recovery observations.
- Residual risks и отсутствие exactly-once promise названы явно.

## Вопросы защиты

### Почему F1 и F2 нужны отдельно?

<details>
<summary>Ответ и объяснение</summary>

F1 проверяет восстановление после новой committed row. F2 проверяет, что уже выполненная duplicate detection сама не является ack и может безопасно повториться. Оба должны вернуться к одному result, но проходят разные состояния handler.

</details>

### Почему poison queue не гарантирует terminal outcome сама по себе?

<details>
<summary>Ответ и объяснение</summary>

At-least-once dead-letter transfer зависит от существующего exchange, binding и доступного target. Source удерживает message до publisher confirm target queue. Поэтому evidence наблюдает source и poison sides, а недоступный target считается незавершённым transfer.

</details>

### Где именно отсутствует exactly-once?

<details>
<summary>Ответ и объяснение</summary>

RabbitMQ может выполнить несколько deliveries; connection может оборваться после локальной отправки ack; DLX transfer тоже допускает duplicate target messages. Unique `source_event_id` сохраняет один бизнес-результат конкретного consumer, но не меняет delivery guarantee всей системы.

</details>

### Почему project evidence не добавляет Verification coverage?

<details>
<summary>Ответ и объяснение</summary>

Tests и fault injection здесь служат способом доказать workflow states и recovery. Центральное самостоятельное действие — спроектировать и восстановить consumer workflow. Отдельного действия по выбору service-wide test strategy этот проект не содержит.

</details>

## Non-goals

Второй workflow или consumer, producer/outbox, fan-out, orchestration platform, ordering/partitioning, distributed transaction, saga, consensus, общий graceful shutdown, performance SLO, broker migration, multi-team Workflow L4, универсальный inbox/DLQ и готовая реализация.

## ImplementationReference

Отсутствует до самостоятельного выполнения и независимого review.

## Связанный контекст и источники

- [Engineering brief](../learn/acknowledgement-redelivery-recovery-boundary.md)
- [S07 producer/event identity](../../transactional-orders-operation/README.md)
- [R1 cancellation/lifecycle context](../../runtime-concurrency-lifecycle/learn/cancellation-deadlines-resource-lifecycle.md)
- [V1 truthful verification boundary](../../risk-based-service-verification/learn/truthful-test-boundaries.md)
- [RabbitMQ consumer acknowledgements](https://www.rabbitmq.com/docs/confirms)
- [RabbitMQ quorum queues](https://www.rabbitmq.com/docs/quorum-queues)
- [`aio-pika` API reference](https://docs.aio-pika.com/apidoc.html)
