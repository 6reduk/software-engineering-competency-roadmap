---
id: b2.learn.acknowledgement-redelivery-recovery-boundary
kind: learn
title: Граница acknowledgement, redelivery и восстановления consumer
owner_track: b2
module: b2.module.background-message-workflows
coverage:
  - target: b2.level-outcome.design-asynchronous-workflows-l2-implement-background-flow
    role: explain
  - target: b2.level-outcome.design-asynchronous-workflows-l3-design-recoverable-workflow
    role: explain
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

# Граница acknowledgement, redelivery и восстановления consumer

Fulfillment worker получил `OrderConfirmed(event_id)`, вставил `fulfillment_requests` и завершил PostgreSQL transaction. До следующей строки process аварийно остановился. RabbitMQ не получил ack и позже доставил сообщение снова. Если handler понимает delivery как новую business command, один заказ получит две заявки. Если он ack-ает до commit, crash может оставить сообщение удалённым, а заявку — несозданной.

Решение находится не в обещании «доставить ровно один раз», а в двух раздельных границах: PostgreSQL определяет durable business result, RabbitMQ — завершение конкретного delivery. Между ними неизбежно есть окно частичного отказа (`partial failure`). Consumer должен корректно переживать обе стороны окна.

## Три identity, которые нельзя смешивать

- **Identity события:** устойчивый `event_id` из S07. Он одинаков у всех deliveries одного `OrderConfirmed`.
- **Identity delivery:** channel-scoped `delivery_tag`. Он относится к конкретной попытке и не хранится как business key.
- **Identity результата:** `fulfillment_requests.source_event_id UNIQUE`; по нему consumer возвращается к уже созданной заявке.

Флаг `redelivered` помогает диагностике, но не является business identity. Корректность должна сохраняться даже без знания полной истории доставки.

## Четыре инварианта

1. **Business-result:** один `event_id` создаёт не более одной `fulfillment_request`; duplicate возвращается к той же строке.
2. **Acknowledgement:** ack отправляется только после подтверждённого commit или подтверждённого чтения существующего результата.
3. **Recovery:** после crash и restart redelivery завершается без ручной правки; source queue пуста, заявка одна.
4. **Poison:** необрабатываемое сообщение после ограниченного числа failed deliveries покидает source queue и наблюдается в poison queue с причиной `delivery_limit`.

Это не exactly-once delivery: broker вправе передать событие больше одного раза, а ack-frame может потеряться вместе с соединением. Инвариант ограничивает бизнес-результат данного consumer.

## Где проходит граница

Схема отвечает на вопрос: почему commit и ack должны быть разными наблюдаемыми шагами?

```mermaid
sequenceDiagram
    participant B as RabbitMQ source queue
    participant C as aio-pika consumer
    participant DB as PostgreSQL

    B->>C: delivery OrderConfirmed(event_id)
    C->>DB: BEGIN; INSERT fulfillment_request(source_event_id)
    DB-->>C: COMMIT confirmed
    Note over C: заранее внедрённое и управляемое одноразовое условие отказа (seeded fault) до ack
    C--xB: connection lost; ack отсутствует
    B->>C: redelivery того же event_id
    C->>DB: найти существующий source_event_id
    DB-->>C: прежний fulfillment_request
    C->>B: basic.ack текущего delivery
```

Схема намеренно не показывает producer и общий shutdown: они не меняют consumer-owned invariant. Практический вывод — после commit нельзя «отменить» заявку; после redelivery нужно восстановить прежний результат и лишь затем завершить текущий delivery.

## Одна delivery model

| Исход обработки | Решение consumer | Наблюдаемый результат |
|---|---|---|
| Новый валидный event | Вставить заявку и commit; затем `ack()` | Одна строка, source delivery завершён |
| Duplicate event | Прочитать строку по `source_event_id`; затем `ack()` | Та же строка, новой мутации нет |
| Исправимый transient failure | `reject(requeue=True)` | Failed delivery учитывается, сообщение возвращается |
| Permanently invalid message | `reject(requeue=True)` | После `delivery-limit=3` broker dead-letter-ит message |
| Crash после commit до ack | Не успевает отправить подтверждение | После обнаружения connection loss broker requeue-ит delivery |

В RabbitMQ 4.3 выбран `basic.reject`, а не `basic.nack`: `reject` и consumer crash увеличивают `delivery-count`, используемый quorum queue для poison limit; `nack(requeue=True)` этот counter не увеличивает. Смешивание этих методов разрушило бы bounded model.

Source quorum queue настроена на `delivery-limit=3`, `dead-letter-strategy=at-least-once`, `overflow=reject-publish` и DLX, связанный с durable quorum queue `orders.fulfillment.poison`. Persistent poison message остаётся в source до подтверждённого приёма target queue; при недоступном DLX target terminal transition может задержаться и должен быть виден операционно.

В закреплённой конфигурации `overflow=reject-publish` — документированное предусловие выбранной `dead-letter-strategy=at-least-once`, а не отдельная рекомендация этого среза о политике переполнения для любых очередей.

## Ack не является второй database transaction

`await message.ack()` в `aio-pika` отправляет `basic.ack` в socket, но broker не отвечает отдельным confirm. Поэтому существует и более узкое окно: handler вызвал ack, но connection оборвалась до получения frame broker-ом. Оно даёт redelivery и обрабатывается тем же `source_event_id`.

Не следует хранить `delivery_tag` в PostgreSQL или пытаться атомарно commit-ить его вместе с заявкой. Tag действует только на исходном channel. Consumer делает business state повторяемым, а не создаёт распределённую transaction.

## Состояния workflow

Полезная модель содержит наблюдаемые состояния, а не только try/except:

- `delivered_unresolved`: message получено, durable result ещё не известен;
- `business_result_committed`: заявка создана, ack ещё может отсутствовать;
- `duplicate_result_confirmed`: существующая заявка найдена;
- `ack_sent`: consumer отправил ack текущего delivery;
- `retryable_failed`: consumer выполнил `reject(requeue=True)`;
- `poisoned`: source delivery отсутствует, сообщение наблюдается в poison queue;
- `recovered`: после restart source queue пуста, row один, ручной repair не нужен.

`ack_sent` — локальное наблюдение клиента, а не доказательство получения broker-ом. Terminal evidence снимается с обеих сторон: queue counters и PostgreSQL state.

## Воспроизводимый fault injection

Одноразовый hook для заданного `event_id` срабатывает сразу после успешного выхода из transaction, записывает маркер `after_commit_before_ack` во внешний журнал и вызывает `os._exit(70)`. `finally`, exception handler и graceful close не выполняются. После restart hook отключён, чтобы проверить recovery, а не бесконечный crash loop.

Минимальный failure/measurement envelope:

- population: 10 изолированных прогонов по одному новому `event_id`;
- нагрузка: одно сообщение, `prefetch_count=1`, не более 30 секунд на прогон;
- fault: process exit после commit и до ack;
- наблюдения: delivery log, marker, `COUNT(*)` по `source_event_id`, source `messages_ready/messages_unacknowledged`, poison queue;
- threshold: 10/10 прогонов — минимум две доставки, ровно одна business row, source counters `0/0`, poison count `0`;
- control: тот же event без hook — одна row и terminal source state;
- recovery: новый consumer instance завершает redelivery без ручной правки.

Для poison profile используется отдельное invalid событие: одна business row не создаётся, source становится `0/0`, poison queue получает сообщение. Это отдельный профиль измерения, а не вторая задача kata.

## Частые ошибки и диагностика

- **Ack до commit.** Симптом: source пуст, business row отсутствует. Исправление — передвинуть ack после durable result.
- **Новая заявка на каждый delivery.** Симптом: один `event_id` связан с несколькими rows. Нужен unique `source_event_id` и read-after-conflict path.
- **Бесконечный requeue.** Симптом: delivery count/consumer load растут, terminal poison state не появляется. Проверить, используется ли `reject`, действует ли policy и маршрутизируется ли DLX.
- **Доверие только `redelivered`.** Flag не заменяет lookup по `event_id`; первая видимая конкретному instance доставка могла ранее обрабатываться другим.
- **Считать `await ack()` end-to-end confirm.** После socket failure возможен duplicate; correctness должна пережить его.
- **Сделать DLQ отдельным курсом.** В этом slice достаточно одного terminal poison outcome и его наблюдений.

## Самопроверка

### Почему ack должен идти после commit, но это всё равно допускает duplicate?

<details>
<summary>Ответ и объяснение</summary>

Ack до commit допускает потерю business result. Ack после commit закрывает эту потерю, но оставляет окно между двумя системами: process или connection могут исчезнуть до получения ack broker-ом. Поэтому RabbitMQ повторит delivery, а consumer обязан вернуть тот же результат по `event_id`.

</details>

### Почему `delivery_tag` нельзя использовать как ключ заявки?

<details>
<summary>Ответ и объяснение</summary>

Delivery tag scoped текущим channel и относится к попытке доставки. После reconnect/redelivery появляется другой delivery context. Устойчивый `event_id` описывает событие и остаётся одинаковым, поэтому именно он связывает retries с одной заявкой.

</details>

### Почему выбран `reject`, а не `nack`?

<details>
<summary>Ответ и объяснение</summary>

В RabbitMQ 4.3 quorum queue увеличивает `delivery-count` для AMQP 0-9-1 `basic.reject` и crash, но не для `basic.nack`. Poison limit оценивается по этому counter. `nack(requeue=True)` позволил бы сообщениям возвращаться без продвижения к выбранному terminal outcome.

</details>

### Что доказывает recovery profile, а что остаётся за его границей?

<details>
<summary>Ответ и объяснение</summary>

Он доказывает для закреплённых версий и одного workflow: crash после commit до ack даёт redelivery и одну row, затем source terminal state. Он не доказывает broker cluster failover, producer recovery, произвольные side effects, ordering, capacity или exactly-once end to end.

</details>

## Словарь

| Термин | Значение в этом срезе |
|---|---|
| Consumer | Fulfillment worker, обрабатывающий `OrderConfirmed` |
| Delivery | Одна попытка RabbitMQ передать message consumer-у |
| Acknowledgement (ack) | `basic.ack` текущего delivery после durable result |
| Redelivery | Новая доставка сообщения, которое не было положительно подтверждено |
| Duplicate delivery | Повторное получение того же `event_id`; не новый business command |
| Partial failure | PostgreSQL commit завершён, а получение ack broker-ом неизвестно |
| Recovery | Завершение того же workflow после restart без ручной правки |
| Poison message | Message, которое стабильно не может быть обработано и достигает limit |
| Business result | Единственная строка `fulfillment_requests` для `source_event_id` |
| DLX | Exchange, через который broker после terminal delivery outcome маршрутизирует сообщение из source queue в закреплённую poison queue |
| Delivery limit | Ограничение числа возвратов сообщения в quorum queue; в закреплённой модели превышение лимита приводит к причине `delivery_limit` и dead-lettering, а не обозначает абстрактное число попыток обработки |

## Первичные источники и связанный контекст

- [RabbitMQ — Release information](https://www.rabbitmq.com/release-information)
- [RabbitMQ — Consumer acknowledgements](https://www.rabbitmq.com/docs/confirms)
- [RabbitMQ — Quorum queues, delivery limit and dead lettering](https://www.rabbitmq.com/docs/quorum-queues)
- [RabbitMQ — Dead Letter Exchanges](https://www.rabbitmq.com/docs/dlx)
- [`aio-pika` 10.0.1 release](https://github.com/mosquito/aio-pika/releases/tag/10.0.1)
- [`aio-pika` API reference](https://docs.aio-pika.com/apidoc.html)
- [S07: устойчивый event identity](../../transactional-orders-operation/learn/transaction-boundary-failure-windows.md)
- [R1: cancellation и lifecycle](../../runtime-concurrency-lifecycle/learn/cancellation-deadlines-resource-lifecycle.md)
- [V1: правдивая test boundary](../../risk-based-service-verification/learn/truthful-test-boundaries.md)

Версии и version-sensitive assertions проверены 2026-08-25. RabbitMQ 4.3.5 — текущий patch поддерживаемой серии 4.3, `aio-pika` 10.0.1 — текущий официальный release на эту дату.
