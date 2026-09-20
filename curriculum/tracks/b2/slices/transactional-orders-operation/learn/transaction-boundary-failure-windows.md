---
id: b2.learn.transaction-boundary-failure-windows
kind: learn
title: Граница транзакции и окна отказа подтверждения заказа
owner_track: b2
module: b2.module.transactional-persistence-integration
coverage:
  - target: b2.level-outcome.manage-application-transaction-boundaries-l1-use-defined-unit
    role: explain
  - target: b2.level-outcome.manage-application-transaction-boundaries-l2-design-operation-boundary
    role: explain
  - target: b2.level-outcome.manage-application-transaction-boundaries-l3-resolve-side-effect-consistency
    role: explain
  - target: b2.level-outcome.design-idempotent-service-operations-l2-implement-known-pattern
    role: explain
  - target: b2.level-outcome.design-idempotent-service-operations-l3-design-failure-safe-operation
    role: explain
status: accepted
updated: 2026-08-24
language: ru
last_verified: 2026-08-21
versions:
  postgresql: 18.6
  psycopg: 3.3.4
---

# Граница транзакции и окна отказа подтверждения заказа

Orders service принимает `POST /orders/{order_id}/confirm`. В памяти операция кажется последовательной: изменить заказ, выполнить commit, опубликовать `OrderConfirmed`, вернуть успех. В реальности процесс может остановиться между любыми двумя шагами, а database transaction не может атомарно включить произвольный внешний приёмник событий (`event sink`, далее sink).

Если сначала изменить заказ и затем вызвать sink, crash между действиями оставит заказ без события. Если вызвать sink до commit, rollback не отменит уже выполненный внешний эффект. Network call внутри transaction лишь дольше удерживает locks и соединение; он не делает две системы одной атомарной границей и не устраняет потерю ответа от sink.

## Три правила вместо «всё или ничего»

1. **Transaction invariant:** `orders.status=confirmed`, сохранённый result операции и `order_events` либо durable вместе, либо отсутствуют вместе.
2. **Recovery invariant:** после подтверждённого commit любой непомеченный event record обнаружим после рестарта и снова доступен publisher.
3. **Idempotency invariant:** один `Idempotency-Key` имеет определённые правила результата, конфликта и хранения; повтор с возвратом ранее сохранённого результата (`replay`) и конкурентный дубликат не создают второе подтверждение.

Первые два правила описывают согласованность database state и recovery path. Третье — контракт повторной command. Они связаны, но не доказываются одним и тем же тестом.

## Каноническая операция

Клиент отправляет UUID в `Idempotency-Key`: это идентификатор операции (`operation identity`). Отпечаток запроса (`request fingerprint`) равен паре `POST confirm + order_id`; тело request пустое. Успешный `200` содержит `operation_id`, `order_id` и `status="confirmed"`. Событие содержит `event_id`, `event_type="OrderConfirmed"`, `operation_id`, `order_id` и `confirmed_at`. Минимальные таблицы выражают не готовую схему, а нужные ограничения:

- `orders(id, status, confirmed_at)`; переход только `draft → confirmed`;
- `operation_results(operation_id PRIMARY KEY, request_fingerprint, order_id, http_status, response_body, completed_at, result_expires_at)`;
- `order_events(event_id PRIMARY KEY, operation_id UNIQUE, order_id, event_type, payload, publish_state, attempts, created_at, published_at)`.

При первом key service пытается создать `operation_results` внутри transaction. Уникальность сериализует concurrent duplicates: проигравший запрос ждёт завершения владельца key, затем воспроизводит committed result; если владелец откатился, следующий запрос может выполнить операцию. Совпавший key с другим fingerprint возвращает `409 idempotency_conflict`.

Конфликт уникальности требует явно выбранного пути продолжения. Если обычный `INSERT` завершается `unique violation`, текущая PostgreSQL transaction переходит в aborted-состояние: прежде чем читать уже сохранённый result, нужно выполнить rollback и начать чтение в следующей transaction. Вариант `INSERT ... ON CONFLICT DO NOTHING` может не создавать exception, но код всё равно должен определить последующее чтение result и поведение, пока конкурентная transaction ещё выполняет commit. Это два допустимых класса решения, а не универсальное предписание использовать `ON CONFLICT`.

В течение 24 часов одинаковые key и fingerprint возвращают тот же status/body. После срока хранения (`retention window`) полное тело можно удалить, но строка identity остаётся как маркер истёкшего key (`tombstone`): тот же key возвращает `409 idempotency_key_expired` и не запускает мутацию. Новый key для уже подтверждённого заказа возвращает `409 order_not_draft` и не создаёт новое событие.

## Где проходит transaction boundary

Psycopg-соединение открыто с `autocommit=True`, а command использует ровно один внешний `with conn.transaction():`. В блоке service:

1. закрепляет operation identity либо читает существующий result;
2. условно меняет `orders` из `draft` в `confirmed`;
3. вставляет `OrderConfirmed` с устойчивым `event_id`;
4. сохраняет HTTP result.

Нормальный выход выполняет `COMMIT`, исключение — `ROLLBACK`. Publisher, event sink и формирование ответа по уже committed result находятся снаружи. При `READ COMMITTED` условный `UPDATE` после ожидания повторно проверяет `WHERE` на новой версии строки; свободные повторные `SELECT` не используются как защита от race. Dirty read исключён, а nonrepeatable/phantom/serialization anomalies в общем случае допустимы и не должны нарушать инвариант благодаря условной записи и unique constraints.

## Как именно расходятся commit и публикация

Вопрос схемы: в какой точке мы уже не можем просто сделать rollback, а должны продолжить или сверить состояние?

```mermaid
sequenceDiagram
    participant C as Client
    participant O as Orders service
    participant DB as PostgreSQL
    participant P as Publisher
    participant S as Event sink

    C->>O: POST /orders/{id}/confirm + Idempotency-Key
    O->>DB: BEGIN; order + result + event record
    alt ошибка до COMMIT
        O->>DB: ROLLBACK
        O-->>C: определённая ошибка
    else COMMIT отправлен
        O->>DB: COMMIT
        Note over O,DB: Потеря связи здесь = unknown commit result
        DB-->>O: COMMIT confirmed
        O-->>C: сохранённый result
        P->>DB: найти pending event record
        P->>S: publish OrderConfirmed(event_id)
        Note over P,S: Потеря ответа здесь = unknown publish result
        P->>DB: mark published
    end
```

Схема упрощает механизм взятия события в работу: экземпляр publisher временно помечает или блокирует pending event как обрабатываемый (`claim`), а ограниченная аренда (`lease`) позволяет другому экземпляру снова взять запись после сбоя владельца. Конкретный SQL и способ блокировки участник выбирает сам. Практический вывод: до commit можно отменить локальные записи; после confirmed commit нужно продолжить publication; после потери DB-связи во время commit нужно сверить result; после потери ответа sink нужно безопасно повторить стабильный `event_id`.

## Durability и неизвестный commit

Baseline использует PostgreSQL 18.6 с `fsync=on` и `synchronous_commit=on`. Успешный ответ `COMMIT` приходит после локального WAL flush; crash recovery может повторить изменения из WAL. Это утверждение относится к database transaction, не к event sink.

Если соединение потеряно после отправки `COMMIT`, но до ответа, Psycopg сообщает ошибку связи; connection может стать `BAD`, а transaction status — `UNKNOWN`. Ни этот status, ни exception не сообщают, обработал ли сервер commit. Broken connection выбрасывается. Service отвечает `503 operation_outcome_unknown` с указанием повторить запрос с тем же key либо сам открывает новое соединение и читает `operation_results`. Слепо начинать новую мутацию нельзя.

## Publisher и граница доставки

Publisher выбирает committed `publish_state=pending`, увеличивает attempts и отправляет `OrderConfirmed` вне долгой database transaction. После подтверждения sink он помечает запись `published`. Crash до первой отправки оставляет pending record. Crash после принятия sink, но до marking, приводит к повторной отправке.

Стабильный `event_id` позволяет sink дедуплицировать повтор либо позволяет потребителю заметить его. Однако механизм не обещает exactly-once: publisher может выполнить network send больше одного раза; sink может принять сообщение и потерять ответ; дальнейшая обработка имеет собственные границы. Здесь гарантируется обнаружимость намерения и повторяемость доставки, а не единственность внешнего эффекта во всех системах.

## Нормальные и ошибочные исходы

| Наблюдение | Database state | Что делает service |
|---|---|---|
| Success commit | order/result/event durable | возвращает сохранённый `200` result; publisher продолжает отдельно |
| Ошибка до commit | все три изменения отсутствуют | rollback; известную исправимую ошибку можно повторить по контракту команды |
| Потеря связи во время commit | outcome неизвестен текущему connection | discard connection; reconcile по key через новое соединение |
| Crash после commit до publish | event pending | restart publisher находит запись и отправляет |
| Потеря ack после publish | sink мог принять event | повтор с тем же `event_id`; downstream dedup — явное допущение |
| Concurrent same-key requests | один владелец key | один выполняет transition, остальные получают тот же result |
| Same key, another order | существующий fingerprint отличается | `409 idempotency_conflict` без мутации |

## Частые слабые решения

- **Считать return `commit()` доказательством publish.** Он подтверждает только границу database transaction.
- **Вызвать sink внутри transaction.** Rollback не отменяет network effect, а неизвестный publish остаётся.
- **Повторять command без identity.** После unknown commit можно создать новый бизнес-результат.
- **Назвать outbox и остановить reasoning.** Event record не задаёт operation result, concurrent duplicate, retention и sink dedup.
- **Повторно использовать broken connection.** Его transaction status уже не является надёжной основой решения.
- **Смешать unknown commit и unknown publish.** Первый сверяется по durable operation result; второй — по event identity и состоянию sink/publisher.
- **Обещать exactly-once.** Локальная атомарность не распространяется на весь путь события.

## Диагностика по наблюдениям

Для transaction/recovery проверяйте вместе `orders`, `operation_results` и `order_events`: после любого завершённого прогона первые два бизнес-факта и event intent не расходятся. Для idempotency отдельно запускайте два concurrent requests с одним key, тот же key после имитированной потери ответа и тот же key с другим `order_id`; сравнивайте HTTP results и число business transitions.

Publisher наблюдается отдельно: число send attempts может быть больше единицы, но event сохраняет один `event_id`. Если event pending после рестарта не находится, нарушен recovery invariant. Если один key создаёт два transitions, нарушен idempotency invariant. Эти сигналы локализуют разные механизмы.

## Самопроверка

### Почему network call внутри transaction не даёт атомарности?

<details>
<summary>Ответ и объяснение</summary>

PostgreSQL не управляет commit внешнего sink. Если sink принял событие, а database transaction откатилась, rollback не отменит событие. Если ответ sink потерялся, transaction всё равно не знает внешний исход. Дополнительно вызов удерживает locks и connection во время network latency.

</details>

### Что делать после ошибки связи из `commit()`?

<details>
<summary>Ответ и объяснение</summary>

Не считать ни commit, ни rollback доказанными и не переиспользовать broken connection. Открыть новое соединение и сверить `operation_results` по исходному `Idempotency-Key`; retry обязан сохранить тот же key и fingerprint. Отсутствие записи после мгновенной проверки может требовать ограниченного повторного reconciliation, а не новой identity.

</details>

### Почему recovery и idempotency требуют разных tests?

<details>
<summary>Ответ и объяснение</summary>

Recovery test доказывает, что committed pending event обнаруживается и отправляется после restart. Idempotency test доказывает identity/result/conflict/retention и race двух commands. Первый может пройти при двух business transitions, второй — при потерянной publication, поэтому один сигнал не заменяет другой.

</details>

### Где exactly-once всё ещё не доказан?

<details>
<summary>Ответ и объяснение</summary>

Между отправкой и marking publisher может упасть, поэтому send повторится. Стабильный `event_id` помогает deduplication, но не делает все downstream side effects атомарными с PostgreSQL. Механизм обещает at-least-once attempt для обнаружимого intent и отдельно оговорённую дедупликацию, а не exactly-once end to end.

</details>

## Словарь

| Термин | Значение в этом срезе |
|---|---|
| Application operation | Одна command подтверждения заказа от HTTP-границы до сохранённого result |
| Transaction boundary | Набор изменений PostgreSQL, завершаемых одним commit/rollback |
| Unknown commit result | Клиент DB потерял связь после отправки commit и не знает server outcome |
| Transactional event record | Намерение публикации, сохранённое атомарно с бизнес-изменением |
| Recovery | Продолжение обнаружимой незавершённой публикации после restart |
| Operation identity | UUID из `Idempotency-Key`, связывающий retries одной command |
| Request fingerprint | Method и `order_id`, для которых key был впервые использован |
| Unknown publish result | Publisher не знает, принял ли sink событие до потери ответа |
| Reconciliation | Сверка durable result/event state через новое соединение или sink |
| Retention | 24 часа полного result; после этого identity tombstone запрещает повторное использование key |
| Replay | Повтор команды с тем же key и fingerprint, который возвращает ранее сохранённый status/body без новой мутации |
| Claim/lease | Временная отметка или блокировка pending event одним publisher; ограниченная аренда позволяет вернуть запись в обработку после сбоя владельца |

## Первичные источники и связанный контекст

- [PostgreSQL 18 — Transaction Isolation](https://www.postgresql.org/docs/18/transaction-iso.html)
- [PostgreSQL 18 — WAL settings](https://www.postgresql.org/docs/18/runtime-config-wal.html#RUNTIME-CONFIG-WAL-SETTINGS)
- [PostgreSQL 18 — Write-Ahead Logging](https://www.postgresql.org/docs/18/wal-intro.html)
- [Psycopg — Transactions management](https://www.psycopg.org/psycopg3/docs/basic/transactions.html)
- [Psycopg — connection and transaction status](https://www.psycopg.org/psycopg3/docs/api/objects.html#psycopg.ConnectionInfo.transaction_status)
- [PostgreSQL — Versioning Policy](https://www.postgresql.org/support/versioning/)
- [Psycopg — Release notes](https://www.psycopg.org/psycopg3/docs/news.html)
- [S04: повтор command после timeout](../../../scenarios.md)
- [S06: application operation и adapters](../../service-architecture-boundaries/learn/change-isolation-service-boundaries.md)
- [S10: риск, механизм и правдивая test boundary](../../risk-based-service-verification/learn/truthful-test-boundaries.md)

Версии и утверждения проверены 2026-08-21. PostgreSQL 18.6 и Psycopg 3.3.4 — текущие стабильные выпуски по официальным реестрам на эту дату; PostgreSQL 18 поддерживается до 2030-11-14.
