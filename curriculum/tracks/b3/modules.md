---
artifact: b3-module-blueprint
status: accepted
updated: 2026-09-09
language: ru
---

# Модули B3 по профессиональному результату

## Reference: общий результат конкурентных операций

Когда отдельно корректные операции портят общее состояние данных, инженеру нужно связать наблюдения с механизмом хранилища и проверить исправление. Один модуль объединяет этот законченный путь и диагностику конфликтов, возникающих на той же границе. Правила записи и B3 defaults заданы в [README](README.md#aggregate-catalog-notation).

<a id="preserve-invariants"></a>

## `b3.module.preserve-concurrent-data-invariants` — Сохранять инварианты в конкурентных транзакциях

- **Scope:** transaction isolation и concurrency control одного operational store при заданных прикладных операциях. Инвариант — правило, обязательное для завершённых операций. Модуль связывает порядок чтений/записей, видимость данных, выбор защиты и локальную реакцию на конфликт.
- **Develops:** `b3.capability.explain-transaction-anomalies`, `b3.capability.protect-store-invariants`, `b3.capability.diagnose-transaction-conflicts` — [действия и их границы](capabilities.md).
- **Non-goals:** полный SQL/PostgreSQL-курс; проектирование relational schema как самостоятельное действие; optimizer, WAL, HA, backup/restore; выбор семейства СУБД; готовая реализация или обязательство выпустить все сценарии одним content package.

Модуль отвечает за сохранение общего правила средствами store, а не за весь жизненный цикл сервиса. **B2** задаёт состав application transaction и договор повторной операции с внешними эффектами. **B5** решает distributed consistency между системами. **B6** поставляет платформу. **B7** задаёт production reliability и межсистемное восстановление. При взаимодействии с этими владельцами B3 передаёт ограничения и наблюдения своего store; см. [карту ownership](README.md#ownership-и-пределы-zoom).

## Вместимость без обязательства общего выпуска

| Ситуация | Завершённое действие внутри модуля | Решение intake |
|---|---|---|
| [TC01: дежурные](scenarios.md#tc01) | Объяснить нарушение общего правила и проверить принятую смену изоляции | Выбран первый action |
| [TC02: конфликт доступа](scenarios.md#tc02) | Локализовать ожидание/цикл и проверить допустимую локальную реакцию | Deadlock-кандидат отклонён для первого action, сохранён как соседний сценарий |
| [TC03: видимость чтения](scenarios.md#tc03) | Различить снимок прочитанных данных и блокирующее ожидание | Snapshot-кандидат отклонён для первого action, сохранён как соседний сценарий |

У этих действий общий предмет — поведение транзакций одного хранилища. Они могут потребовать разных будущих пакетов и разных наблюдений. Наличие модуля не означает готовность среды, существование учебных материалов или завершение обучения. [Outcomes](level-outcomes.md) задают критерии будущей деятельности, [prerequisites](prerequisites.md) — входные умения.

## Остальные десять кластеров — batch M1.9.2

Каждый модуль ниже имеет отдельный законченный результат: схема, результат запроса, объяснение сохранности, путь доступа, переход схемы, смена узла, предел масштаба, восстановленные данные, контролируемая эксплуатация или выбор store. Поэтому в этом batch выбран один навигационный дом на кластер. Это не десять отдельных пакетов выпуска.

<a id="relational-model-schema"></a>

## `b3.module.encode-relational-data-rules` — Выражать правила данных реляционной схемой

- **Scope:** `b3.cluster.relational-model-schema`; Выделяет отношения, ключи и зависимости; выбирает нормализацию или обоснованное дублирование для заданных операций. Выражает заданные правила через ключи, ссылочную целостность и ограничения значений; выявляет правила вне их гарантии.
- **Develops:** `b3.capability.model-relational-structure`, `b3.capability.enforce-relational-constraints`.
- **Non-goals:** application persistence architecture B2 и конкурентная защита reference-модуля.

<a id="sql-querying"></a>

## `b3.module.derive-correct-query-results` — Получать корректный результат запроса

- **Scope:** `b3.cluster.sql-querying`; Строит соединения, фильтрацию и подзапросы с явной гранулярностью результата и поведением NULL и дубликатов. Выбирает группировку, оконные вычисления и этапы композиции, сохраняя требуемую гранулярность.
- **Develops:** `b3.capability.compose-relational-queries`, `b3.capability.derive-grouped-window-results`.
- **Non-goals:** аналитические pipelines B4 и tuning планов соседнего модуля.

<a id="storage-wal-recovery"></a>

## `b3.module.reason-about-durable-store-state` — Объяснять сохранность и восстановление состояния store

- **Scope:** `b3.cluster.storage-wal-recovery`; Связывает страницы, журнал предзаписи, подтверждение записи и checkpoint с границей сохранности данных. Локализует фазу и препятствие crash recovery по журналам, состоянию данных и зависимостям локального engine.
- **Develops:** `b3.capability.explain-store-durability`, `b3.capability.diagnose-store-crash-recovery`.
- **Non-goals:** backup/PITR из копий и межсистемная continuity B7.

<a id="indexes-optimizer"></a>

## `b3.module.improve-store-query-access` — Улучшать доступ к данным по плану запроса

- **Scope:** `b3.cluster.indexes-optimizer`; Связывает план, оценки кардинальности, статистику и фактическую работу с причиной затрат запроса. Сопоставляет структуры и состав индекса с предикатами, порядком и ценой поддержания при записи.
- **Develops:** `b3.capability.diagnose-query-plans`, `b3.capability.choose-query-indexes`.
- **Non-goals:** семантическое перепроектирование SQL, общий capacity planning B7.

<a id="schema-evolution"></a>

## `b3.module.evolve-store-schema-safely` — Изменять схему с сохранением совместимости данных

- **Scope:** `b3.cluster.schema-evolution`; Определяет промежуточные схемы и ограничения данных для сосуществующих readers/writers; согласует контракт store с B2. Проверяет DDL/backfill с текущей записью, локальными блокировками и сверкой полноты; задаёт безопасное продолжение.
- **Develops:** `b3.capability.plan-compatible-schema-transitions`, `b3.capability.validate-online-data-change`.
- **Non-goals:** API evolution B2, rollout automation B6 и release-risk gates B7.

<a id="replication-ha"></a>

## `b3.module.preserve-store-guarantees-on-failover` — Сохранять гарантии store при смене узла

- **Scope:** `b3.cluster.replication-ha`; Соотносит режим подтверждения, доставку и применение изменений с видимостью чтений и возможной потерей при отказе. Оценивает готовность кандидата, исключение прежнего writer и проверку данных после promotion в одной store topology.
- **Develops:** `b3.capability.assess-replica-data-guarantees`, `b3.capability.validate-store-failover`.
- **Non-goals:** распределённые алгоритмы B5, platform automation B6 и cross-system recovery B7.

<a id="partitioning-scaling"></a>

## `b3.module.scale-store-workload-within-limits` — Масштабировать workload в пределах гарантий store

- **Scope:** `b3.cluster.partitioning-scaling`; Выбирает ключ и гранулярность partitioning, оценивая pruning, перекос, ограничения и обслуживание данных. Различает ограничения соединений, CPU, памяти, I/O и конкуренции; выбирает store-level изменение и границу масштабирования.
- **Develops:** `b3.capability.design-store-partitioning`, `b3.capability.assess-store-scaling-limits`.
- **Non-goals:** общие sharding/routing algorithms B5, provisioning B6 и системный capacity planning B7.

<a id="backup-restore-dr"></a>

## `b3.module.prove-store-data-recoverability` — Проверять восстанавливаемость данных store

- **Scope:** `b3.cluster.backup-restore-dr`; Выбирает состав копий, журналов, метаданных и доступов для заданной цели восстановления одного store. Выполняет изолированный restore/PITR, сверяет целостность и границу включённых изменений одного store.
- **Develops:** `b3.capability.design-store-backup-chain`, `b3.capability.verify-store-point-in-time-restore`.
- **Non-goals:** crash recovery действующего engine, cross-system RTO/RPO и DR exercises B7.

<a id="security-operations"></a>

## `b3.module.operate-store-with-controlled-access` — Поддерживать работоспособность и контролируемый доступ store

- **Scope:** `b3.cluster.security-operations`; Разделяет учётные роли и полномочия на объекты, проверяет разрешённые/запрещённые действия и наблюдаемость доступа. По engine-specific сигналам различает накопление устаревших версий, устаревшую статистику, расход места и мешающие обслуживанию сессии.
- **Develops:** `b3.capability.enforce-store-access-boundaries`, `b3.capability.diagnose-store-maintenance-needs`.
- **Non-goals:** Python runtime B1, application authorization B2, platform IAM B6, incident management B7.

<a id="operational-nonrelational-stores"></a>

## `b3.module.choose-and-validate-operational-store` — Выбирать и проверять operational store под задачу

- **Scope:** `b3.cluster.operational-nonrelational-stores`; Сопоставляет relational, key-value, document, wide-column и search store с данными, запросами и эксплуатационными ограничениями. Проверяет ключи/документы, обновления, индексацию, expiry/eviction и чтения в заявленной границе конкретного store.
- **Develops:** `b3.capability.select-operational-store-model`, `b3.capability.validate-nonrelational-store-contract`.
- **Non-goals:** прикладной cache B2, общая consistency B5, analytical storage B4, vector retrieval B10 и организационная policy C1.
