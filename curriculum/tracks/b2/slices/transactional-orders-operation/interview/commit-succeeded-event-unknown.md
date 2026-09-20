---
id: b2.interview.commit-succeeded-event-unknown
kind: interview
title: Собеседование — commit завершён, публикация неизвестна
owner_track: b2
module: b2.module.transactional-persistence-integration
coverage:
  - target: b2.level-outcome.manage-application-transaction-boundaries-l1-use-defined-unit
    role: probe
  - target: b2.level-outcome.manage-application-transaction-boundaries-l2-design-operation-boundary
    role: probe
  - target: b2.level-outcome.manage-application-transaction-boundaries-l3-resolve-side-effect-consistency
    role: probe
  - target: b2.level-outcome.design-idempotent-service-operations-l2-implement-known-pattern
    role: probe
  - target: b2.level-outcome.design-idempotent-service-operations-l3-design-failure-safe-operation
    role: probe
status: accepted
updated: 2026-08-24
language: ru
last_verified: 2026-08-21
versions:
  postgresql: 18.6
  psycopg: 3.3.4
---

# Собеседование: commit завершён, публикация неизвестна

## История для кандидата

Один Orders service обрабатывает `POST /orders/{order_id}/confirm` с пустым телом request. Клиент передаёт UUID в `Idempotency-Key`: это идентификатор операции (`operation identity`). Отпечаток запроса (`request fingerprint`) — method и `order_id`. Заказ можно перевести только `draft → confirmed`. Успешный `200` содержит `operation_id`, `order_id` и `status="confirmed"`; `OrderConfirmed` содержит `event_id`, `event_type`, `operation_id`, `order_id` и `confirmed_at`, причём `event_type="OrderConfirmed"`.

В PostgreSQL 18.6 используются три минимальные сущности: `orders`, сохранённые результаты `operation_results` и события `order_events`. Psycopg 3.3.4 работает через autocommit connection и явный `with conn.transaction():`; isolation — `READ COMMITTED`, `fsync=on`, `synchronous_commit=on`.

Одна database transaction должна изменить заказ, сохранить HTTP result и создать `OrderConfirmed(event_id)`. Отдельный процесс публикации (`publisher`) после commit отправляет event во внешний приёмник событий (`event sink`, далее sink) и затем помечает record как published. Result по одному key хранится 24 часа. Одинаковые key и fingerprint воспроизводят status/body; тот же key с другим fingerprint даёт `409 idempotency_conflict`.

Процесс может остановиться:

- до commit;
- после отправки commit, но до получения ответа;
- после подтверждённого commit, но до первой публикации;
- после принятия события sink, но до marking в PostgreSQL.

Попросите кандидата думать вслух. Термин `outbox` сам по себе ничего не доказывает: важны граница database transaction, наблюдения и поведение каждого повтора.

## 1. L1 — заданная unit of work

**Вопрос.** Какие изменения должны находиться в одной database transaction и что должны доказать success/rollback checks?

<details>
<summary>Ориентиры сильного ответа</summary>

В transaction входят условный переход `orders`, запись полного result по operation identity и вставка одного `order_events`. На success после commit все три видимы вместе. При exception до commit все отсутствуют вместе. Внешний sink не входит в transaction. Сильный ответ проверяет реальный PostgreSQL commit/rollback, а не только вызов repository mock.

</details>

**Follow-up.** Почему нельзя сначала отправить событие, а при ошибке сделать rollback?

<details>
<summary>Ориентиры сильного ответа</summary>

Rollback управляет только PostgreSQL. Принятый sink side effect не отменится, поэтому появится событие о неподтверждённом заказе. Нужна durable запись намерения внутри transaction и отдельный recovery path после commit.

</details>

## 2. L2 — самостоятельный выбор границы

**Вопрос.** Где начнётся и закончится transaction, если service использует Psycopg `Connection.transaction()`?

<details>
<summary>Ориентиры сильного ответа</summary>

На autocommit connection внешний `with conn.transaction():` охватывает только DB reads/writes одного command: identity claim/result, conditional order update, event record. Нормальный выход коммитит, exception откатывает. Publisher и network I/O идут после выхода. Кандидат учитывает, что transaction block на уже открытой implicit transaction мог бы стать savepoint и скрыть реальную outer boundary, поэтому выбирает явную lifecycle convention.

</details>

**Follow-up.** Чем опасен вызов sink внутри блока, даже если timeout мал?

<details>
<summary>Ориентиры сильного ответа</summary>

Он удерживает row locks/connection на network latency, повышает contention и не решает unknown publish. Sink может принять event, а ответ потеряться; database rollback не отменит внешний эффект. Малый timeout ограничивает ожидание, но не создаёт атомарность.

</details>

## 3. Transaction L3 — failure-window map и recovery

**Вопрос.** Для каждой из четырёх точек отказа назовите наблюдаемое database/sink state и следующее безопасное действие.

<details>
<summary>Ориентиры сильного ответа</summary>

- До commit: order/result/event отсутствуют, можно выполнить command заново с тем же key.
- Потеря связи во время commit: текущий connection даёт unknown outcome; его выбрасывают и через новое соединение сверяют `operation_results` по key. Нельзя считать exception доказательством rollback.
- После confirmed commit до publish: order/result/event durable, publisher после restart находит pending event.
- После publish до marking: sink мог принять event, PostgreSQL видит pending; повторяется тот же `event_id`, а sink или получатель события применяет оговорённую deduplication.

Кандидат явно различает unknown database commit и unknown external publish.

</details>

**Follow-up.** Сформулируйте transaction и recovery invariants и предложите отдельное наблюдение L3.

<details>
<summary>Ориентиры сильного ответа</summary>

Transaction invariant: confirmed order, operation result и event intent durable вместе либо отсутствуют вместе. Recovery invariant: любой committed pending event обнаружим после restart и в итоге получает новый send attempt. Результат L3-проверки — fault injection после confirmed commit до первой публикации, restart publisher и проверка того же `event_id` в sink при неизменном одном business transition. Это наблюдение не проверяет весь контракт идемпотентности.

</details>

**Follow-up.** Что означает успешный `commit()` при `synchronous_commit=on` и чего он не означает?

<details>
<summary>Ориентиры сильного ответа</summary>

Он означает локальный WAL flush для database transaction и позволяет crash recovery восстановить изменения. Он не доказывает, что HTTP client получил ответ, publisher запустился или sink принял событие.

</details>

## 4. Idempotency L2 — известный pattern

**Вопрос.** Опишите identity, result, conflict, retention и concurrent duplicate behavior.

<details>
<summary>Ориентиры сильного ответа</summary>

UUID из `Idempotency-Key` — identity; fingerprint связывает его с method и order. Одинаковые key/fingerprint в течение 24 часов возвращают сохранённые status/body. Тот же key с другим order — `409 idempotency_conflict`. Unique constraint даёт одного владельца key; конкурентный дубликат ждёт commit/rollback, затем выполняет повтор с возвратом ранее сохранённого результата (`replay`) либо продолжает после rollback. После 24 часов полное тело можно удалить, но маркер истёкшего key (`tombstone`) возвращает `409 idempotency_key_expired` и не запускает новую мутацию.

</details>

**Follow-up.** Что вернёт новый key для уже подтверждённого заказа?

<details>
<summary>Ориентиры сильного ответа</summary>

Определённый `409 order_not_draft` без второго `OrderConfirmed`. Это другая operation identity, поэтому прежний `200` не воспроизводится, но бизнес-инвариант остаётся целым.

</details>

## 5. Idempotency L3 — неизвестный клиенту результат и race

**Вопрос.** Клиент не получил response после unknown commit и повторил тот же command дважды конкурентно. Какой отдельный L3 experiment нужен?

<details>
<summary>Ориентиры сильного ответа</summary>

Оба повтора используют тот же key/fingerprint. Fault harness разрывает DB connection в commit window, затем запускает два concurrent retries. Наблюдения: один сохранённый result, не более одного перехода `draft → confirmed`, один event record/event_id, одинаковые replay status/body. Отдельно тот же key с другим order даёт conflict, а retention policy зафиксирована. Это результат проверки идемпотентности; restart publisher здесь не заменяет проверку race и правил результата.

</details>

**Follow-up.** Почему немедленное отсутствие `operation_results` после connection loss ещё не разрешает новую identity?

<details>
<summary>Ориентиры сильного ответа</summary>

Проверка сама может происходить во время завершения/recovery или читать не тот endpoint/replica. Нужна ограниченная политика reconciliation на authoritative primary и повтор с исходным key. Новая identity способна превратить временную неопределённость в второй command.

</details>

## 6. Граница доставки

**Вопрос.** Можно ли назвать решение exactly-once?

<details>
<summary>Ориентиры сильного ответа</summary>

Нет. Между sink acceptance и DB marking остаётся окно, поэтому network send может повториться. Стабильный `event_id` поддерживает deduplication, но не атомарен со всеми downstream side effects. Корректное обещание: durable event intent, recovery/retry и явное допущение о повторной доставке.

</details>

**Follow-up.** Что изменится, если sink не умеет deduplicate?

<details>
<summary>Ориентиры сильного ответа</summary>

Duplicate delivery становится наблюдаемым свойством и потребители должны быть безопасны к повтору либо бизнес должен принять ущерб. Нельзя скрыть это повтором внутри publisher или расширить PostgreSQL transaction через сеть. Изменение общей delivery architecture вышло бы за текущий B2 slice.

</details>

## Rubric

| Уровень ответа | Наблюдаемое рассуждение |
|---|---|
| Слабый | Говорит «обернём всё в transaction» или «outbox даёт exactly-once»; предлагает network call внутри transaction; retry без identity; смешивает unknown commit и unknown publish. |
| L1 | Верно группирует order/result/event и различает success commit от rollback, но следует заданной boundary без самостоятельного анализа. |
| L2 | Сам выбирает короткую DB boundary, определяет key/fingerprint/result/conflict/retention и concurrent behavior, не удерживает transaction через sink. |
| Transaction L3 | Строит полную failure-window map, выбирает recovery и предлагает fault injection, отдельно подтверждающий transaction/recovery invariants. |
| Idempotency L3 | Отдельно проектирует unknown-result retry и concurrent race, проверяет identity/result/conflict/retention и число business transitions. |
| За пределами среза | Уходит в 2PC/consensus, общую taxonomy delivery guarantees, WAL/MVCC internals или межкомандный L4 вместо решения одной Orders operation. |

Интервью имеет роль `probe`: сильное объяснение показывает глубину reasoning, но proficiency L3 требует выполненных наблюдаемых experiments, например из project specification.

## Признаки ошибочной ментальной модели

- exception из `commit()` автоматически считается rollback;
- `commit()` считается подтверждением event sink;
- rollback якобы отменяет уже принятый network side effect;
- idempotency сводится к «не упасть на duplicate key» без result/conflict/retention;
- один restart test объявляется доказательством concurrent duplicate semantics;
- outbox называется универсальным решением без failure windows;
- повторная отправка скрывается за обещанием exactly-once.

## Источники интервьюера

- [PostgreSQL 18 — Transaction Isolation](https://www.postgresql.org/docs/18/transaction-iso.html)
- [PostgreSQL 18 — WAL settings](https://www.postgresql.org/docs/18/runtime-config-wal.html#RUNTIME-CONFIG-WAL-SETTINGS)
- [Psycopg — Transactions management](https://www.psycopg.org/psycopg3/docs/basic/transactions.html)
- [Psycopg — ConnectionInfo transaction status](https://www.psycopg.org/psycopg3/docs/api/objects.html#psycopg.ConnectionInfo.transaction_status)
- [Подробная модель S07](../learn/transaction-boundary-failure-windows.md)
