---
id: b2.interview.side-effect-committed-message-unacked
kind: interview
title: Собеседование — side effect committed, message unacked
owner_track: b2
module: b2.module.background-message-workflows
coverage:
  - target: b2.level-outcome.design-asynchronous-workflows-l2-implement-background-flow
    role: probe
  - target: b2.level-outcome.design-asynchronous-workflows-l3-design-recoverable-workflow
    role: probe
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

# Собеседование: side effect committed, message unacked

## История для кандидата

RabbitMQ 4.3.5 доставляет persistent `OrderConfirmed(event_id, order_id, operation_id, confirmed_at)` из durable quorum queue `orders.fulfillment`. Один Python worker на `aio-pika` 10.0.1 использует manual acknowledgement и `prefetch_count=1`. Он создаёт `fulfillment_requests` в PostgreSQL 18.6; `source_event_id` уникален.

Source queue имеет `delivery-limit=3`. Ошибка возвращает delivery через `IncomingMessage.reject(requeue=True)`. После превышения limit broker через `at-least-once` DLX переносит message в durable quorum queue `orders.fulfillment.poison`. Positive path использует `ack(multiple=False)`.

В инциденте transaction завершилась, заявка создана, но process упал до ack. После restart то же событие пришло снова. Попросите кандидата спроектировать поведение и способы доказательства. Producer outbox, общий shutdown и выбор test strategy уже решены вне этого интервью.

## 1. L2 — разместить acknowledgement

**Вопрос.** Где должен находиться ack и что делает handler при первом и повторном delivery?

<details>
<summary>Ориентиры сильного ответа</summary>

Первый delivery валидируется, затем consumer в transaction создаёт заявку с unique `source_event_id`; только после confirmed commit отправляет ack. При duplicate он читает существующую строку по тому же `event_id`, проверяет, что это тот же определённый результат, и ack-ает текущий delivery. Ack до commit создаёт потерю результата, а безусловная повторная вставка — второй результат либо неконтролируемый unique error.

</details>

**Follow-up.** Достаточно ли успешного возврата `await message.ack()`?

<details>
<summary>Ответ</summary>

Нет. `aio-pika` отправляет ack-frame в socket без отдельного ответа broker-а. Потеря connection оставляет неопределённость, получил ли broker frame. Поэтому terminal evidence включает состояние source queue и PostgreSQL, а duplicate после такого окна остаётся корректным.

</details>

## 2. L2 — владение ошибками и retry

**Вопрос.** Разведите normal, transient, duplicate и permanently invalid paths без альтернативной retry-модели.

<details>
<summary>Ориентиры сильного ответа</summary>

Normal и duplicate завершаются `ack` после durable result. Transient и permanently invalid delivery возвращаются одним `reject(requeue=True)`. Source quorum queue считает `basic.reject` failed delivery; `delivery-limit=3` ограничивает путь, а DLX задаёт один poison outcome. Handler владеет классификацией ошибки, broker policy — счётчиком и terminal transition. `nack(requeue=True)` не подменяет выбранный метод, потому что в RabbitMQ 4.3 не увеличивает `delivery-count`.

</details>

**Follow-up.** Почему три быстрых requeue всё же не являются хорошей production backoff policy?

<details>
<summary>Ответ</summary>

Limit прекращает бесконечный loop, но не решает длительный outage зависимости и может быстро исчерпать попытки. В этом bounded slice он служит воспроизводимому poison evidence для одной операции. Production delay/backoff требует отдельного решения и наблюдений, которых здесь нет.

</details>

## 3. L3 — карта failure points

**Вопрос.** Предскажите state для четырёх точек: до commit; после commit до ack; после duplicate detection до ack; после отправки ack до уверенности в получении broker-ом.

<details>
<summary>Ориентиры сильного ответа</summary>

- До commit: business row отсутствует; unacked delivery возвращается и может быть обработан заново.
- После commit до ack: row существует; redelivery находит её и не создаёт вторую.
- После duplicate detection до ack: state не меняется; следующий delivery снова находит ту же row.
- После локальной отправки ack: broker мог получить frame и удалить delivery либо не получить и redeliver; обе ветви дают ту же row.

Сильный ответ не обещает моментальную redelivery и не использует delivery tag как durable identity.

</details>

## 4. L3 — invariants и состояния

**Вопрос.** Какие invariants и terminal observations вы запишете до реализации?

<details>
<summary>Ориентиры сильного ответа</summary>

Business-result: `COUNT(*) WHERE source_event_id=:event_id = 1`. Acknowledgement: ack только после commit/duplicate lookup. Recovery: после restart source counters `0/0`, row одна, ручной repair не нужен. Poison: invalid event не создаёт row, покидает source и наблюдается в poison queue с `delivery_limit`. Состояния различают delivered/unresolved, committed, duplicate-confirmed, retryable-failed, recovered и poisoned.

</details>

**Follow-up.** Почему `redelivered=true` не является invariant?

<details>
<summary>Ответ</summary>

Это диагностическое свойство delivery, а не устойчивый ключ события или результата. Оно не доказывает полную историю и не защищает от повторной мутации. Correctness основана на `event_id` и durable unique constraint.

</details>

## 5. L3 — воспроизводимое доказательство recovery

**Вопрос.** Как отличить настоящий crash window от теста, который лишь бросил exception?

<details>
<summary>Ориентиры сильного ответа</summary>

Заранее внедрённый и управляемый одноразовый fault hook (`seeded hook`) для одного `event_id` срабатывает после подтверждённого commit и вызывает немедленный process exit, не проходя exception handler/finally/graceful close. Внешний marker подтверждает fault point. Новый process восстанавливает consumer. В 10 изолированных прогонах ожидаются минимум две deliveries, ровно одна row, source `0/0`, poison `0`. Control profile без hook завершается одной row; invalid profile измеряется отдельно.

</details>

**Follow-up.** Какие остаточные риски нужно назвать?

<details>
<summary>Ответ</summary>

Проверка не доказывает cluster failover, producer recovery, arbitrary external side effects, throughput, ordering и exactly-once. Она действует для закреплённых версий, quorum policy, одного PostgreSQL side effect и заявленного fault point.

</details>

## 6. Poison outcome

**Вопрос.** Какие наблюдения отделяют terminal poison outcome от временно зависшего DLX transfer?

<details>
<summary>Ориентиры сильного ответа</summary>

Terminal: source ready/unacked равны нулю, poison queue содержит persistent message с dead-letter reason `delivery_limit`, business row отсутствует. Если at-least-once DLX не может подтвердить target, source сохраняет dead-lettered message и retry transfer; это operational failure, а не доказанный terminal outcome. Нужно наблюдать обе queue sides.

</details>

## Rubric

| Уровень ответа | Наблюдаемое reasoning |
|---|---|
| Ниже L2 | Ack до commit, новый result на redelivery, бесконечный requeue или «broker даёт exactly-once» |
| L2 | Реализует заданный flow; явно назначает ack/error/retry ownership; различает normal, duplicate и poison paths |
| L3 | Самостоятельно задаёт states/invariants, перечисляет failure points, строит crash/restart evidence и называет пределы доказательства |
| Не доказанный L4 | Разговор о migration нескольких команд без выполненного adoption evidence не повышает уровень |

Сильный кандидат говорит наблюдаемыми состояниями и проверками, а не количеством broker-терминов.

## Типичные ловушки

- перенести producer outbox внутрь consumer solution;
- считать ack частью PostgreSQL commit;
- ловить unique violation и ack-ать, не сверив прежний result;
- использовать `delivery_tag` или `redelivered` вместо `event_id`;
- выбрать `nack` в модели, где poison limit зависит от `delivery-count`;
- считать наличие poison queue доказательством успешного DLX transfer;
- выдать 10 лабораторных прогонов за production guarantee.

## Источники интервьюера

- [Engineering brief](../learn/acknowledgement-redelivery-recovery-boundary.md)
- [RabbitMQ consumer acknowledgements](https://www.rabbitmq.com/docs/confirms)
- [RabbitMQ quorum queues](https://www.rabbitmq.com/docs/quorum-queues)
- [`aio-pika` API](https://docs.aio-pika.com/apidoc.html)
