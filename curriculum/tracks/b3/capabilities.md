---
artifact: b3-capability-blueprint
status: accepted
updated: 2026-09-09
language: ru
---

# Профессиональные действия B3

## Reference: три действия при конкуренции транзакций

Некорректный общий результат, выбор защиты и зависшая операция требуют разных инженерных решений. Каталог разделяет их по тому, какой результат нужно получить, сохраняя одного владельца — B3. Записи используют [aggregate defaults](README.md#aggregate-catalog-notation); primary module описан в [каталоге модуля](modules.md#preserve-invariants).

| ID | Title | Primary cluster | Наблюдаемое действие | Primary module |
|---|---|---|---|---|
| `b3.capability.explain-transaction-anomalies` | Воспроизводить и объяснять аномалии транзакций | `b3.cluster.transactions-concurrency` | Восстанавливает фактический порядок операций (schedule), связывает чтения, записи и исходы транзакций с сигналами store и объясняет аномалию относительно заданного инварианта | `b3.module.preserve-concurrent-data-invariants` |
| `b3.capability.protect-store-invariants` | Выбирать и проверять защиту инвариантов хранилища | `b3.cluster.transactions-concurrency` | Выбирает ограниченный механизм управления конкурентным доступом для заданного правила, проверяет сохранение правила и допустимых операций, защищает компромиссы и область применимости | `b3.module.preserve-concurrent-data-invariants` |
| `b3.capability.diagnose-transaction-conflicts` | Локализовать конфликты и границу реакции транзакции | `b3.cluster.transactions-concurrency` | По порядку операций и диагностике store различает ожидание, цикл блокировок и иной transaction conflict, локализует участников и определяет допустимые завершение, rollback и новую попытку | `b3.module.preserve-concurrent-data-invariants` |

## Границы и потенциальные подтверждения

<a id="anomalies"></a>

### Объяснять аномалии

Вопрос способности — почему наблюдаемый результат не соответствует правилу. Подтверждение (evidence) должно связать значения чтений, порядок записей и terminal outcomes конкретных транзакций с конечным состоянием. Название аномалии и список уровней изоляции такой связи не дают. Защиту менять для этого действия необязательно: объяснение дефекта самостоятельно ценно Backend при диагностике, Architecture — при проверке допущений о данных. Выбор нового механизма относится к следующей способности. [Проявления L1–L3](level-outcomes.md#anomalies).

<a id="protection"></a>

### Проверять защиту

Вопрос — какая защита сохраняет заданный инвариант и какой ценой. Потенциальные подтверждения: сравнение исходной и изменённой защиты на различающих условиях, допустимая успешная операция, сохранённый инвариант, явно наблюдаемые отказы и ограничения. Полный запрет записей не считается успехом. Способность нужна Backend для локального изменения и Architecture для выбора договора доступа к store и межкомандного внедрения. Она не определяет API идемпотентности, внешний retry protocol или distributed transaction. [Проявления L1–L4](level-outcomes.md#protection).

<a id="conflicts"></a>

### Диагностировать конфликты

Вопрос — кто или что остановило транзакцию и в каком состоянии допустимо продолжение. Потенциальные подтверждения: наблюдения участников и ожиданий, различение технической ошибки и бизнес-отказа, подтверждённый исход завершения, новая попытка с отдельной идентичностью там, где она допустима. Для deadlock нужен цикл ожиданий, для другого конфликта — соответствующие ему сигналы; полный внутренний граф store не предполагается доступным. Backend использует это при расследовании; Architecture — чтобы согласовать технические обязательства вызывающей стороны. Систему повторов B2/B5, incident management B7 и администрирование платформы B6 эта способность не поглощает. [Проявления L1–L3](level-outcomes.md#conflicts).

## Почему в reference именно три

Объяснение причины может закончиться без смены механизма; проверка защиты заканчивается обоснованным изменением; диагностика конфликта может быть нужна при корректном инварианте. Это три независимых результата. Видимость snapshot, SQLSTATE и отдельные isolation levels — понятия или сигналы внутри действий, а не дополнительные capabilities. [Scenarios](scenarios.md) связывают их, [role requirements](role-requirements.md) задают разную глубину для двух ролей.

## Остальные десять кластеров — batch M1.9.2

Каждая строка — самостоятельное действие с одним primary cluster и module. Уровни и критерии заданы в [каталоге outcomes](level-outcomes.md#batch-outcomes); навигационные дома — в [modules](modules.md#остальные-десять-кластеров--batch-m192).

| ID | Title | Primary cluster | Наблюдаемое действие | Primary module |
|---|---|---|---|---|
| `b3.capability.model-relational-structure` | Проектировать структуру связанных данных | `b3.cluster.relational-model-schema` | Выделяет отношения, ключи и зависимости; выбирает нормализацию или обоснованное дублирование для заданных операций. | `b3.module.encode-relational-data-rules` |
| `b3.capability.enforce-relational-constraints` | Проверять ограничения допустимых состояний | `b3.cluster.relational-model-schema` | Выражает заданные правила через ключи, ссылочную целостность и ограничения значений; выявляет правила вне их гарантии. | `b3.module.encode-relational-data-rules` |
| `b3.capability.compose-relational-queries` | Составлять запросы с проверяемой семантикой | `b3.cluster.sql-querying` | Строит соединения, фильтрацию и подзапросы с явной гранулярностью результата и поведением NULL и дубликатов. | `b3.module.derive-correct-query-results` |
| `b3.capability.derive-grouped-window-results` | Вычислять агрегаты и окна без искажения данных | `b3.cluster.sql-querying` | Выбирает группировку, оконные вычисления и этапы композиции, сохраняя требуемую гранулярность. | `b3.module.derive-correct-query-results` |
| `b3.capability.explain-store-durability` | Объяснять путь записи к долговечному состоянию | `b3.cluster.storage-wal-recovery` | Связывает страницы, журнал предзаписи, подтверждение записи и checkpoint с границей сохранности данных. | `b3.module.reason-about-durable-store-state` |
| `b3.capability.diagnose-store-crash-recovery` | Диагностировать восстановление после остановки | `b3.cluster.storage-wal-recovery` | Локализует фазу и препятствие crash recovery по журналам, состоянию данных и зависимостям локального engine. | `b3.module.reason-about-durable-store-state` |
| `b3.capability.diagnose-query-plans` | Диагностировать работу запроса по плану | `b3.cluster.indexes-optimizer` | Связывает план, оценки кардинальности, статистику и фактическую работу с причиной затрат запроса. | `b3.module.improve-store-query-access` |
| `b3.capability.choose-query-indexes` | Выбирать и проверять индексы под workload | `b3.cluster.indexes-optimizer` | Сопоставляет структуры и состав индекса с предикатами, порядком и ценой поддержания при записи. | `b3.module.improve-store-query-access` |
| `b3.capability.plan-compatible-schema-transitions` | Планировать совместимые переходы схемы | `b3.cluster.schema-evolution` | Определяет промежуточные схемы и ограничения данных для сосуществующих readers/writers; согласует контракт store с B2. | `b3.module.evolve-store-schema-safely` |
| `b3.capability.validate-online-data-change` | Проводить и проверять ограниченное изменение данных | `b3.cluster.schema-evolution` | Проверяет DDL/backfill с текущей записью, локальными блокировками и сверкой полноты; задаёт безопасное продолжение. | `b3.module.evolve-store-schema-safely` |
| `b3.capability.assess-replica-data-guarantees` | Оценивать гарантии данных на репликах | `b3.cluster.replication-ha` | Соотносит режим подтверждения, доставку и применение изменений с видимостью чтений и возможной потерей при отказе. | `b3.module.preserve-store-guarantees-on-failover` |
| `b3.capability.validate-store-failover` | Проверять безопасную смену основного узла | `b3.cluster.replication-ha` | Оценивает готовность кандидата, исключение прежнего writer и проверку данных после promotion в одной store topology. | `b3.module.preserve-store-guarantees-on-failover` |
| `b3.capability.design-store-partitioning` | Выбирать разбиение данных под доступ и жизненный цикл | `b3.cluster.partitioning-scaling` | Выбирает ключ и гранулярность partitioning, оценивая pruning, перекос, ограничения и обслуживание данных. | `b3.module.scale-store-workload-within-limits` |
| `b3.capability.assess-store-scaling-limits` | Определять ограничения ёмкости и соединений store | `b3.cluster.partitioning-scaling` | Различает ограничения соединений, CPU, памяти, I/O и конкуренции; выбирает store-level изменение и границу масштабирования. | `b3.module.scale-store-workload-within-limits` |
| `b3.capability.design-store-backup-chain` | Проектировать проверяемую цепочку резервирования | `b3.cluster.backup-restore-dr` | Выбирает состав копий, журналов, метаданных и доступов для заданной цели восстановления одного store. | `b3.module.prove-store-data-recoverability` |
| `b3.capability.verify-store-point-in-time-restore` | Проверять восстановление данных в заданную точку | `b3.cluster.backup-restore-dr` | Выполняет изолированный restore/PITR, сверяет целостность и границу включённых изменений одного store. | `b3.module.prove-store-data-recoverability` |
| `b3.capability.enforce-store-access-boundaries` | Проверять минимальные права и аудит доступа store | `b3.cluster.security-operations` | Разделяет учётные роли и полномочия на объекты, проверяет разрешённые/запрещённые действия и наблюдаемость доступа. | `b3.module.operate-store-with-controlled-access` |
| `b3.capability.diagnose-store-maintenance-needs` | Диагностировать потребность в обслуживании store | `b3.cluster.security-operations` | По engine-specific сигналам различает накопление устаревших версий, устаревшую статистику, расход места и мешающие обслуживанию сессии. | `b3.module.operate-store-with-controlled-access` |
| `b3.capability.select-operational-store-model` | Выбирать модель operational store | `b3.cluster.operational-nonrelational-stores` | Сопоставляет relational, key-value, document, wide-column и search store с данными, запросами и эксплуатационными ограничениями. | `b3.module.choose-and-validate-operational-store` |
| `b3.capability.validate-nonrelational-store-contract` | Проверять контракт операций нереляционного store | `b3.cluster.operational-nonrelational-stores` | Проверяет ключи/документы, обновления, индексацию, expiry/eviction и чтения в заявленной границе конкретного store. | `b3.module.choose-and-validate-operational-store` |
