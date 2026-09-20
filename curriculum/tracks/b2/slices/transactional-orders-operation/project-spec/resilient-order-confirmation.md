---
id: b2.project-spec.resilient-order-confirmation
kind: project-spec
title: Проектная спецификация — восстанавливаемое подтверждение заказа
owner_track: b2
module: b2.module.transactional-persistence-integration
coverage:
  - target: b2.level-outcome.manage-application-transaction-boundaries-l3-resolve-side-effect-consistency
    role: integrate
  - target: b2.level-outcome.manage-application-transaction-boundaries-l3-resolve-side-effect-consistency
    role: assess
  - target: b2.level-outcome.design-idempotent-service-operations-l3-design-failure-safe-operation
    role: integrate
  - target: b2.level-outcome.design-idempotent-service-operations-l3-design-failure-safe-operation
    role: assess
status: accepted
updated: 2026-08-24
language: ru
last_verified: 2026-08-21
versions:
  postgresql: 18.6
  psycopg: 3.3.4
---

# Проектная спецификация: восстанавливаемое подтверждение заказа

## Рабочая ситуация

Orders service подтверждает заказ в PostgreSQL, а downstream получает `OrderConfirmed` через отдельный процесс публикации (`publisher`). Команда уже сталкивалась с двумя несовместимыми наблюдениями: заказ confirmed без события после restart и повторное событие после потери ответа приёмника событий (`event sink`, далее sink). Клиент также повторяет command после timeout и ожидает один определённый бизнес-результат.

В отдельном репозитории выполните один milestone: реализуйте одну confirmation operation на реальном PostgreSQL 18.6 с Psycopg 3.3.4, воспроизведите несколько fault points и раздельно подтвердите transaction/recovery и idempotency L3. Спецификация не диктует архитектуру, SQL, framework или готовый recovery algorithm.

## Неизменяемый предметный контракт

- HTTP command: `POST /orders/{order_id}/confirm` с пустым телом request.
- Заголовок `Idempotency-Key` содержит UUID — идентификатор операции (`operation identity`); отпечаток запроса (`request fingerprint`) — method и `order_id`.
- Draft order переходит в `confirmed`; первый успех возвращает `200` с `operation_id`, `order_id`, `status="confirmed"`.
- Одинаковые key/fingerprint в течение 24 часов выполняют повтор с возвратом ранее сохранённого результата (`replay`) и получают тот же status/body. Состояние retention оценивается отдельно для каждого запроса по авторитетному времени PostgreSQL внутри его transaction/read boundary. Запрос до границы может получить сохранённый result, а запрос после неё — `409 idempotency_key_expired`; разные ответы запросов по разные стороны границы не нарушают same-key invariant.
- Тело сохранённого результата и tombstone должны переходить между retention states согласованно. Полный cleanup subsystem проектировать в этом milestone не требуется.
- Тот же key с другим order возвращает `409 idempotency_conflict`.
- Новый key для уже подтверждённого заказа возвращает `409 order_not_draft` и не создаёт событие.
- Одна database transaction сохраняет order transition, operation result и `OrderConfirmed` event record с устойчивым `event_id`.
- Публикуемое событие содержит `event_id`, `event_type="OrderConfirmed"`, `operation_id`, `order_id` и `confirmed_at`.
- PostgreSQL использует `READ COMMITTED`, `fsync=on`, `synchronous_commit=on`; Psycopg — autocommit connection и явный внешний transaction context.
- Publisher обращается к управляемому event-sink adapter вне database transaction и после ack помечает event published.

Минимальная schema должна выражать `orders`, `operation_results` и `order_events`; точные columns/indexes выбирает участник. Unique constraints обязаны поддерживать operation identity и единственность event intent, а не служить декоративной копией названий.

## Один milestone и наблюдаемые deliverables

1. Работающий Orders service, реальный PostgreSQL и воспроизводимые команды запуска/restart.
2. Event-sink adapter с управляемыми timeout/lost-ack profiles и журналом полученных `event_id`.
3. Документированные transaction, recovery и idempotency invariants.
4. Детерминированные точки инъекции отказа (`fault hooks`) для четырёх точек ниже.
5. State observer, показывающий order, saved result, event publish state/attempts и sink deliveries.
6. Отдельный Transaction L3 experiment с результатами проверки recovery.
7. Отдельный Idempotency L3 experiment с результатами проверки concurrent duplicates и replay.
8. Measurement summary по заранее объявленному envelope.
9. Короткий decision record с альтернативами, ограничениями и остаточными рисками.

## Обязательные fault points

| ID | Точка | Что нельзя заранее предполагать |
|---|---|---|
| F0 | После начала DB transaction, до commit | Изменения могли остаться частичными |
| F1 | `COMMIT` отправлен, DB connection разорван до ответа | Exception не доказывает rollback; server outcome неизвестен текущему connection |
| F2 | Commit подтверждён, до первой публикации | In-memory queue переживёт restart |
| F3 | Sink принял event, publisher не получил/не сохранил ack | Повторный send не произойдёт |

F1 реализуйте управляемым proxy/connection termination или иным способом, который действительно создаёт оба допустимых server outcomes в серии прогонов. Простое `raise` до `commit()` не является unknown commit. F3 должен различать «sink не принял» и «sink принял, ack потерян» хотя бы журналом sink.

## Evidence A — Transaction L3

Цель: доказать failure-window map и recovery mechanism независимо от idempotency race.

Для F0–F3 зафиксируйте ожидаемые и фактические состояния authoritative PostgreSQL и sink. Обязательные acceptance criteria:

- после F0 нет confirmed order без result/event и нет event без confirmed order;
- после любого confirmed commit order/result/event durable вместе;
- после F2 restart без повторной HTTP command находит pending event и выполняет send attempt того же `event_id`;
- после F3 recovery повторяет тот же `event_id`, а duplicate behavior sink явно наблюдаем;
- F1 не приводит к использованию broken connection; reconciliation через новое соединение находит сохранённый result либо безопасно сохраняет исходный key для ограниченного retry;
- database commit, unknown commit, external publish и unknown publish представлены разными state transitions и logs.

Эти результаты подтверждают transaction/recovery invariant. Они не засчитываются как Idempotency L3, пока не проверены правила operation identity и concurrent commands.

## Evidence B — Idempotency L3

Цель: отдельно доказать поведение command при неизвестном клиенту результате и race.

Обязательные cases:

1. два concurrent requests с одним key/fingerprint на draft order;
2. два одновременно освобождённых запроса с разными UUID `Idempotency-Key` подтверждают один draft order; fingerprint каждого запроса соответствует одной и той же паре method + `order_id`;
3. retry с тем же key после F1, когда клиент не получил исходный result;
4. тот же key с другим `order_id`;
5. новый key для уже подтверждённого заказа;
6. граница 24-hour retention: после expiry тело результата удалено, tombstone сохранён и возвращает `409 idempotency_key_expired`; ждать сутки не требуется — допустим управляемый clock.

Во втором case ожидаются ровно один переход `draft → confirmed`, один `OrderConfirmed` event record и один успешный business result. Проигравший запрос получает определённый `409 order_not_draft` без второго event. В результаты проверки входят authoritative PostgreSQL state, оба HTTP results и identities всех найденных events: так исполнение условного `UPDATE`, а не только описание схемы, становится частью Idempotency L3 evidence.

Acceptance criteria:

- один key имеет ровно один committed result, а все same-fingerprint responses при одинаковом retention state семантически совпадают;
- same-key race создаёт не более одного `draft → confirmed` transition и одного event record/event_id;
- different-key race даёт ровно один успешный result и один `409 order_not_draft`, ровно один transition и один event record/event_id;
- fingerprint conflict всегда даёт `409` без мутации;
- F1 retry не создаёт второй business result независимо от того, успел исходный commit или нет;
- expiry каждого запроса определяется авторитетным временем PostgreSQL в его transaction/read boundary; запросы по разные стороны границы могут получить соответственно сохранённый result и `409 idempotency_key_expired`;
- tombstone и удаление тела результата переходят согласованно, а второй business transition/event после retention невозможен;
- результаты не выводятся только из количества HTTP `200`: проверяются authoritative rows и event identities.

Эти отдельные результаты подтверждают identity/result/conflict/retention и race. Один publisher restart не удовлетворяет этим критериям.

## Measurement envelope

До прогонов зафиксируйте machine/runtime baseline, exact dependency versions, команды и seed. Выполните минимум:

- по 10 прогонов F0, F2 и F3;
- 20 прогонов F1, чтобы наблюдать и reconcile каждый реально полученный server outcome; если harness создаёт только один исход, зафиксируйте ограничение и дополните управляемым профилем второго;
- 20 same-key concurrent duplicate trials, каждый с двумя одновременно освобождёнными requests;
- 20 отдельных different-key trials, каждый с двумя одновременно освобождёнными requests к одному draft order и разными UUID `Idempotency-Key`;
- по 5 прогонов conflict, нового key для уже подтверждённого заказа и retention-with-controlled-clock cases.

Точки наблюдения: primary PostgreSQL после quiescence, sink log, service/publisher logs и фактические HTTP results. Threshold: 0 нарушений transaction invariant; 0 вторых business transitions/event records; 100% F2 events обнаружены после restart; каждый F3 повторяет исходный `event_id`; все same-key replay/conflict outcomes соответствуют contract. Во всех 20 different-key trials должны наблюдаться ровно один `200`, один `409 order_not_draft`, один переход `draft → confirmed` и один `OrderConfirmed` event record/event_id. Это experiment threshold данного проекта, не production SLO.

Разделяйте три профиля: fault reproduction до recovery, контрольный прогон без fault и состояние после recovery/quiescence. Raw counts и каждый violation сохраняются, а не заменяются фразой «тесты зелёные».

## Decision record

Зафиксируйте:

- выбранную transaction boundary и connection lifecycle;
- минимум две альтернативы согласования side effect, например direct publish после commit, transactional event record + polling publisher, DB-native notification только как wake-up;
- почему выбранный механизм сохраняет durable intent, но не обещает exactly-once;
- как publisher временно помечает или блокирует pending event как взятый в работу и как ограниченная аренда (`lease`) позволяет другому экземпляру вернуть запись в обработку после сбоя владельца; конкретный SQL/locking algorithm выберите и обоснуйте самостоятельно;
- operation identity, fingerprint, result, conflict и retention decisions;
- способ reconciliation unknown commit и критерий discard connection;
- допущение sink о повторной доставке и ущерб, если оно не выполняется;
- стоимость tables/polling/cleanup и trigger пересмотра;
- остаточные риски за пределами одного service/event sink.

DB-native notification допустима только как оптимизация пробуждения: authoritative recovery остаётся в durable event records. Готовый универсальный outbox recipe не требуется.

## Review criteria

- [ ] Один Orders service, одна confirmation operation и один `OrderConfirmed` согласованы во всех deliverables.
- [ ] PostgreSQL/Psycopg baseline и runtime settings проверены при запуске.
- [ ] Network I/O отсутствует внутри database transaction.
- [ ] F0–F3 воспроизводимы в названных точках; F1 не имитируется исключением до commit.
- [ ] Transaction L3 evidence удовлетворяет отдельным recovery criteria.
- [ ] Idempotency L3 evidence удовлетворяет отдельным race/replay/conflict/retention criteria.
- [ ] Broken connection после unknown commit не переиспользуется.
- [ ] Unknown commit и unknown publish не смешаны.
- [ ] Publisher может повторить send, сохраняя `event_id`; exactly-once не заявлен.
- [ ] Measurement population, profiles, points and thresholds объявлены до результатов.
- [ ] Raw summary позволяет независимо пересчитать violations и recovery rate.
- [ ] Decision record рассматривает alternatives, costs, limits и trigger пересмотра.
- [ ] Нет caching/S15, S09 worker course, 2PC/consensus/saga taxonomy или B3 internals.
- [ ] ImplementationReference отсутствует до самостоятельного выполнения и review.

## Вопросы защиты

### Какие два наблюдения независимо подтверждают L3 outcomes?

<details>
<summary>Ориентиры ответа</summary>

Transaction L3: state matrix F0–F3 и restart recovery подтверждают atomic order/result/event intent и обнаружимость публикации. Idempotency L3: concurrent same-key trials и F1 replay подтверждают identity/result/conflict/retention и единственность business transition. Они могут использовать общую систему, но имеют разные faults, observations и acceptance criteria.

</details>

### Почему F1 нельзя заменить exception до commit?

<details>
<summary>Ориентиры ответа</summary>

До отправки commit outcome известен: transaction можно abort/rollback. Неопределённость появляется, когда server мог durable применить commit, а client потерял ответ. Harness должен разрывать связь в этом protocol window и проверять результат через новое connection.

</details>

### Почему стабильный event_id не равен exactly-once?

<details>
<summary>Ориентиры ответа</summary>

Он позволяет распознать duplicate, но publisher всё равно может выполнить send несколько раз, а downstream side effects не входят в PostgreSQL transaction. Exactly-once потребовал бы более сильного end-to-end контракта всех участников, которого этот проект не задаёт.

</details>

### Какой риск остаётся после всех зелёных прогонов?

<details>
<summary>Ориентиры ответа</summary>

Envelope не доказывает все timing combinations, production topology, storage corruption, реальный broker behavior или downstream business dedup. Сильный ответ связывает существенный residual risk с будущей проверкой/решением и не расширяет локальный experiment до универсальной гарантии.

</details>

## Non-goals

- эталонная архитектура, scaffold или solution code;
- выбор СУБД, MVCC/lock manager/WAL internals и полный isolation course;
- distributed commit, consensus, saga taxonomy и общая delivery theory;
- caching/S15, background workflow/S09 и production rollout;
- multi-team L4 adoption и performance SLO.

## ImplementationReference

Отсутствует до самостоятельного выполнения проекта и независимого review. Эта спецификация задаёт наблюдаемый milestone, а не готовое решение.

## Связанный контекст

- [Ментальная модель S07](../learn/transaction-boundary-failure-windows.md)
- [S04: повтор command после timeout](../../../scenarios.md)
- [S06: application operation и adapters](../../service-architecture-boundaries/learn/change-isolation-service-boundaries.md)
- [S10: правдивые границы проверок](../../risk-based-service-verification/learn/truthful-test-boundaries.md)
- [Официальные допущения substrate](../../../../../../governance/work-packages/M1.8.5-transactional-persistence-s07-slice.md#b3-readiness-record)
