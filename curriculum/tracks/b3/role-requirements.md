---
artifact: b3-role-requirement-blueprint
status: accepted
updated: 2026-09-09
language: ru
---

# Ролевые требования B3

## Reference: транзакции и конкурентность

Backend-инженер расследует некорректный результат и зависшие операции. Архитектор с B3 specialization выбирает обязательства доступа к данным и согласует их применение. Поэтому глубина отдельных действий различается, хотя обе [RoleViews](../../roles/role-summary.md) обозначают B3 как depth с навигационным L4.

Этот каталог задаёт конкретную authoritative projection **в пределах полного blueprint**. Именно перечисленные LevelOutcome links определяют требования этого кластера; отсутствующая связь не возникает из общего уровня трека автоматически. Routes не редактируются. Формат строк задан в [README](README.md#aggregate-catalog-notation), определения — в [LevelOutcomes](level-outcomes.md).

- **Required baseline** — обязательное поведение роли в этой специализации.
- **Deepening** — дополнительное углубление под более сложные задачи, не скрытая часть baseline.
- **Conditional specialization** — требование включается только при прямо названной ответственности за внедрение. L4 не назначается за чтение документа или участие в лаборатории.

<a id="backend"></a>

## Backend / Distributed Systems

Route: [backend-distributed-systems](../../roles/backend-distributed-systems.md). Роль должна самостоятельно расследовать неоднозначные симптомы своего store; выбор общего договора для множества writers и межкомандное внедрение выделены отдельно.

| Категория | LevelOutcome | Почему нужен роли / условие |
|---|---|---|
| Required baseline | `b3.level-outcome.explain-transaction-anomalies-l3-resolve-ambiguous-history` | [Anomalies L3](level-outcomes.md#anomalies): владелец backend должен проверять конкурирующие причины некорректных данных при неполном следе |
| Required baseline | `b3.level-outcome.protect-store-invariants-l2-select-bounded-control` | [Protection L2](level-outcomes.md#protection): самостоятельно выбрать и проверить защиту типовой операции, сохранив полезный успех |
| Required baseline | `b3.level-outcome.diagnose-transaction-conflicts-l3-resolve-uncertain-conflict` | [Conflicts L3](level-outcomes.md#conflicts): определить безопасную границу реакции на неоднозначный конфликт, не скрыть его произвольным retry |
| Deepening | `b3.level-outcome.protect-store-invariants-l3-defend-store-contract` | [Protection L3](level-outcomes.md#protection): при ответственности за несколько путей записи требуется защитить полный договор owned store boundary |
| Conditional specialization | `b3.level-outcome.protect-store-invariants-l4-adopt-cross-team-policy` | [Protection L4](level-outcomes.md#protection): только если инженер отвечает за фактическое внедрение правил доступа несколькими командами с разными workloads |

Это три обязательные связи, одна deepening и одна conditional. Backend не получает обязанности владельца production database platform, backup/HA или общесистемного incident management.

<a id="architecture"></a>

## Architecture / Technical Leadership — B3 specialization

Route: [architecture-technical-leadership](../../roles/architecture-technical-leadership.md). Здесь B3 рассматривается как выбранная техническая глубина. Архитектор должен уметь самостоятельно проверить локальное воспроизведение и типовой конфликт, а основной L3 нужен для защиты договора данных при неоднозначных требованиях.

| Категория | LevelOutcome | Почему нужен роли / условие |
|---|---|---|
| Required baseline | `b3.level-outcome.explain-transaction-anomalies-l2-reproduce-anomaly` | [Anomalies L2](level-outcomes.md#anomalies): отличить проверяемую причину дефекта от правдоподобного объяснения при выборе гарантии |
| Required baseline | `b3.level-outcome.protect-store-invariants-l3-defend-store-contract` | [Protection L3](level-outcomes.md#protection): системный выбор требует учесть все существенные writers, допущения и цену защиты |
| Required baseline | `b3.level-outcome.diagnose-transaction-conflicts-l2-localize-known-conflict` | [Conflicts L2](level-outcomes.md#conflicts): самостоятельно проверить типовой конфликт, чтобы согласовать выполнимые обязательства вызывающей стороны |
| Deepening | `b3.level-outcome.explain-transaction-anomalies-l3-resolve-ambiguous-history` | [Anomalies L3](level-outcomes.md#anomalies): требуется как углубление при личном ведении расследований по неполным данным |
| Deepening | `b3.level-outcome.diagnose-transaction-conflicts-l3-resolve-uncertain-conflict` | [Conflicts L3](level-outcomes.md#conflicts): углубление при личной ответственности за сложную диагностику owned store |
| Conditional specialization | `b3.level-outcome.protect-store-invariants-l4-adopt-cross-team-policy` | [Protection L4](level-outcomes.md#protection): включается при ответственности за внедрение общего store-level договора несколькими командами; технические последствия должны быть наблюдаемы |

Это три обязательные связи, две deepening и одна conditional. Роль не становится DBA: ежедневное администрирование, query tuning, HA/backup и platform operation не следуют из этих требований. Организационное лидерство остаётся C1; здесь оцениваются технические правила конкурентного доступа и последствия их применения.

## Интерпретация и пределы

В reference две ролевые проекции и 11 явных связей с outcomes: 6 required, 3 deepening, 2 conditional. Higher-level requirement подразумевает применимое поведение нижних уровней той же capability, но каждый outcome сформулирован самодостаточно; отдельные L1-строки не нужны как дублирование baseline. Отсутствующее требование означает «не задано», а не нулевую способность.

Условный L5 не назначается: [каталог уровней](level-outcomes.md#применимость-уровней) не определяет независимый организационный результат данного кластера. Track-level L4 не наследуется всем capabilities. Один сценарий может дать разные наблюдения, но не подтверждает несколько уровней автоматически; TC01 со сменой изоляции по готовому условию не заменяет самостоятельный выбор механизма и межкомандное применение. Учебного coverage и вывода hiring-grade эти списки не создают.

## Проекции остальных десяти кластеров

В новых строках категории записаны канонически: `required`, `deepening`, `conditional`; они соответствуют Required baseline, Deepening и Conditional specialization reference. Более высокий outcome подразумевает применимое поведение нижних уровней той же capability, поэтому таблицы не дублируют все L1–L3. Conditional применяется только при названной ответственности; отсутствие роли DBA не отменяет базового понимания последствий store operations.

### Backend / Distributed Systems — batch

RoleView: [backend](../../roles/backend-distributed-systems.md).

| Категория | LevelOutcome | Почему нужен роли / условие |
|---|---|---|
| required | `b3.level-outcome.model-relational-structure-l2-perform-bounded-action` | Схема должна поддерживать операции backend. |
| deepening | `b3.level-outcome.model-relational-structure-l3-defend-uncertain-decision` | При противоречивых чтениях и записях сервиса выбирает степень нормализации и способ сопровождения копий; это углубление за пределами построения типовой схемы. |
| required | `b3.level-outcome.enforce-relational-constraints-l2-perform-bounded-action` | Проверяет целостность типовой записи. |
| deepening | `b3.level-outcome.enforce-relational-constraints-l3-defend-uncertain-decision` | Для неоднозначных правил данных определяет защиту NULL, удаления связей и обходных путей записи; это углубление относительно проверки ограничений небольшой схемы. |
| required | `b3.level-outcome.compose-relational-queries-l3-defend-uncertain-decision` | Отвечает за смысл сложных запросов приложения. |
| required | `b3.level-outcome.derive-grouped-window-results-l2-perform-bounded-action` | Получает корректные сводки operational данных. |
| deepening | `b3.level-outcome.derive-grouped-window-results-l3-defend-uncertain-decision` | В сложной сводке сервиса находит этап искажения гранулярности и перестраивает вычисления; это углубляет обязательное получение типовых агрегатов и ранжирования. |
| required | `b3.level-outcome.explain-store-durability-l2-perform-bounded-action` | Разбирает обещание сохранности записи. |
| deepening | `b3.level-outcome.explain-store-durability-l3-defend-uncertain-decision` | При исчезновении видимых ранее данных различает неподтверждённую запись, допущения сохранности и иной источник чтения; расследование неполной истории углубляет разбор записи при заданной конфигурации. |
| required | `b3.level-outcome.diagnose-store-crash-recovery-l1-explain-observed-behavior` | Распознаёт recovery и предел самостоятельного вмешательства. |
| conditional | `b3.level-outcome.diagnose-store-crash-recovery-l2-perform-bounded-action` | При назначенной ответственности за диагностику восстановления хранилища после остановки исследует незавершённое восстановление в выделенной среде и проверяет допустимое действие и доступность данных. |
| required | `b3.level-outcome.diagnose-query-plans-l3-defend-uncertain-decision` | Локализует нетипичные причины затрат запроса. |
| required | `b3.level-outcome.choose-query-indexes-l2-perform-bounded-action` | Выбирает индекс для запросов сервиса. |
| deepening | `b3.level-outcome.choose-query-indexes-l3-defend-uncertain-decision` | При конкуренции чтений и записей сервиса выбирает набор индексов с учётом перекоса данных и стоимости записи и обслуживания; это углубление относительно индекса для ограниченного набора запросов. |
| required | `b3.level-outcome.plan-compatible-schema-transitions-l2-perform-bounded-action` | Планирует совместимость схемы своего сервиса. |
| deepening | `b3.level-outcome.plan-compatible-schema-transitions-l3-defend-uncertain-decision` | Для схемы с неизвестными потребителями выбирает промежуточные состояния и допустимые необратимые шаги; это углубление за пределами типового перехода с известными путями доступа. |
| conditional | `b3.level-outcome.validate-online-data-change-l2-perform-bounded-action` | При личной ответственности за DDL/backfill в выделенном store. |
| conditional | `b3.level-outcome.validate-online-data-change-l3-defend-uncertain-decision` | При личном владении нетипичным online change и его безопасным продолжением. |
| required | `b3.level-outcome.assess-replica-data-guarantees-l2-perform-bounded-action` | Проверяет читаемые данные и подтверждения. |
| deepening | `b3.level-outcome.assess-replica-data-guarantees-l3-defend-uncertain-decision` | При конфликте требований сервиса к свежести, задержке и доступности выбирает режим чтения и подтверждения; это углубление относительно проверки заданного профиля репликации. |
| required | `b3.level-outcome.validate-store-failover-l1-explain-observed-behavior` | Распознаёт условия допустимой смены узла. |
| conditional | `b3.level-outcome.validate-store-failover-l2-perform-bounded-action` | При назначенной ответственности за проверку смены основного узла в выделенной топологии подтверждает единственный допустимый путь записи, состояние данных и условия возврата прежнего узла. |
| required | `b3.level-outcome.design-store-partitioning-l2-perform-bounded-action` | Самостоятельно проектирует разбиение данных своего сервиса и проверяет чтения, записи, границы разделов, целостность и удаление старых данных; это часть обязательного проектирования данных backend-сервиса. |
| deepening | `b3.level-outcome.design-store-partitioning-l3-defend-uncertain-decision` | При конфликтующих запросах и перекосе данных защищает разбиение либо отказ от него с учётом роста числа разделов и обслуживания; это углубление относительно проектирования типовых разделов своего сервиса. |
| required | `b3.level-outcome.assess-store-scaling-limits-l2-perform-bounded-action` | Проверяет ограничения ресурсов и соединений. |
| deepening | `b3.level-outcome.assess-store-scaling-limits-l3-defend-uncertain-decision` | При меняющейся нагрузке сервиса сравнивает допуск соединений, вертикальный рост и предел переноса данных; выбор масштабирования углубляет проверку заданного ресурсного ограничения. |
| required | `b3.level-outcome.design-store-backup-chain-l1-explain-observed-behavior` | Может распознать неполную цепочку копий. |
| conditional | `b3.level-outcome.design-store-backup-chain-l2-perform-bounded-action` | При назначенной ответственности за подготовку цепочки резервирования хранилища своего сервиса составляет и проверяет её компоненты и зависимости под заданную цель восстановления. |
| required | `b3.level-outcome.verify-store-point-in-time-restore-l1-explain-observed-behavior` | Отличает поднятый engine от восстановленных данных. |
| conditional | `b3.level-outcome.verify-store-point-in-time-restore-l2-perform-bounded-action` | При назначенной ответственности за проверку восстановления данных своего сервиса восстанавливает копию в изолированное назначение и сверяет целевую точку, согласованность и права доступа. |
| required | `b3.level-outcome.enforce-store-access-boundaries-l2-perform-bounded-action` | Проверяет минимальные права своего приложения. |
| deepening | `b3.level-outcome.enforce-store-access-boundaries-l3-defend-uncertain-decision` | При конфликте диагностики и изоляции выбирает привилегии, полноту аудита и условия отзыва временного доступа; это углубление относительно задания минимальных прав приложения. |
| required | `b3.level-outcome.diagnose-store-maintenance-needs-l1-explain-observed-behavior` | Распознаёт потребность в обслуживании и передаёт наблюдения. |
| conditional | `b3.level-outcome.diagnose-store-maintenance-needs-l2-perform-bounded-action` | При назначенной ответственности за обслуживание хранилища своего сервиса подтверждает типовую причину деградации несколькими сигналами и проверяет эффект и стоимость выбранного действия. |
| required | `b3.level-outcome.select-operational-store-model-l2-perform-bounded-action` | Сравнивает store для ограниченного workload. |
| deepening | `b3.level-outcome.select-operational-store-model-l3-defend-uncertain-decision` | При неопределённых требованиях сервиса защищает выбор хранилища, цену смены модели и условие пересмотра; это углубление относительно сравнения кандидатов для заданной нагрузки. |
| conditional | `b3.level-outcome.validate-nonrelational-store-contract-l2-perform-bounded-action` | При назначенной ответственности за принятие и проверку технического контракта нереляционного хранилища своего сервиса проверяет допустимые обновления, чтения и применимые правила хранения и обновления индекса. |
| conditional | `b3.level-outcome.validate-nonrelational-store-contract-l3-defend-uncertain-decision` | При личной ответственности за диагностику неоднозначного поведения выбранного store. |

### Architecture / Technical Leadership — batch

RoleView: [architecture](../../roles/architecture-technical-leadership.md).

| Категория | LevelOutcome | Почему нужен роли / условие |
|---|---|---|
| required | `b3.level-outcome.model-relational-structure-l3-defend-uncertain-decision` | Архитектор защищает модель и цену дублирования. |
| required | `b3.level-outcome.enforce-relational-constraints-l3-defend-uncertain-decision` | Выбирает границу гарантии среди всех writers. |
| required | `b3.level-outcome.compose-relational-queries-l2-perform-bounded-action` | Самостоятельно проверяет типовой контракт чтения. |
| deepening | `b3.level-outcome.compose-relational-queries-l3-defend-uncertain-decision` | При личном проектировании сложного контракта чтения разрешает разные трактовки соединений, фильтров и подзапросов; это углубление относительно обязательной проверки типового запроса. |
| required | `b3.level-outcome.derive-grouped-window-results-l1-explain-observed-behavior` | Должен распознать изменение гранулярности; углубление нужно при личном проектировании запросов. |
| deepening | `b3.level-outcome.derive-grouped-window-results-l3-defend-uncertain-decision` | При личном разборе сложных сводок локализует искажение гранулярности и защищает порядок вычислений; это углубление относительно понимания строк, объединяемых агрегатом и сохраняемых окном. |
| required | `b3.level-outcome.explain-store-durability-l3-defend-uncertain-decision` | Оценивает неопределённость гарантий при проектировании store. |
| required | `b3.level-outcome.diagnose-store-crash-recovery-l1-explain-observed-behavior` | Понимает сигналы и границу локального восстановления. |
| conditional | `b3.level-outcome.diagnose-store-crash-recovery-l3-defend-uncertain-decision` | При назначенной технической ответственности за продолжение восстановления после неоднозначной остановки различает медленный прогресс, недоступный журнал и повреждение, выбирает безопасную диагностику и предел вмешательства. |
| required | `b3.level-outcome.diagnose-query-plans-l1-explain-observed-behavior` | Читает план для проверки аргументов специалистов. |
| deepening | `b3.level-outcome.diagnose-query-plans-l3-defend-uncertain-decision` | При личном расследовании нестабильной производительности различает влияние распределения данных, параметров и альтернатив плана; это углубление относительно чтения плана для проверки аргументов специалистов. |
| required | `b3.level-outcome.choose-query-indexes-l1-explain-observed-behavior` | Понимает цену индекса; лично проектирует его только при нужной глубине. |
| deepening | `b3.level-outcome.choose-query-indexes-l3-defend-uncertain-decision` | При личном проектировании путей доступа защищает набор индексов и цену его записи и обслуживания; это углубление относительно понимания применимости отдельного индекса. |
| required | `b3.level-outcome.plan-compatible-schema-transitions-l3-defend-uncertain-decision` | Выбирает переход при неизвестных потребителях. |
| required | `b3.level-outcome.validate-online-data-change-l1-explain-observed-behavior` | Понимает признаки неполноты и блокировки без обязанности выполнять все migrations. |
| conditional | `b3.level-outcome.validate-online-data-change-l3-defend-uncertain-decision` | При личном владении нетипичным online change и его безопасным продолжением. |
| required | `b3.level-outcome.assess-replica-data-guarantees-l3-defend-uncertain-decision` | Защищает store guarantees при trade-offs latency/доступности. |
| required | `b3.level-outcome.validate-store-failover-l1-explain-observed-behavior` | Понимает границу безопасности promotion. |
| conditional | `b3.level-outcome.validate-store-failover-l3-defend-uncertain-decision` | При назначенной технической ответственности за решение о смене основного узла по неполным сигналам выбирает продолжение либо остановку, сопоставляя риск двух источников записи и потери подтверждённых данных. |
| required | `b3.level-outcome.design-store-partitioning-l3-defend-uncertain-decision` | Выбирает разбиение с учётом паттернов и срока жизни данных. |
| required | `b3.level-outcome.assess-store-scaling-limits-l3-defend-uncertain-decision` | Защищает пределы роста и переход к другой схеме. |
| required | `b3.level-outcome.design-store-backup-chain-l1-explain-observed-behavior` | Понимает зависимости восстановления и проверяет обещания. |
| conditional | `b3.level-outcome.design-store-backup-chain-l3-defend-uncertain-decision` | При назначенной технической ответственности за схему резервирования выбирает глубину истории и зависимости копий с учётом хранения и риска разрыва цепочки; цели RTO/RPO получает от B7. |
| required | `b3.level-outcome.verify-store-point-in-time-restore-l1-explain-observed-behavior` | Понимает достижимость целевой точки. |
| conditional | `b3.level-outcome.verify-store-point-in-time-restore-l3-defend-uncertain-decision` | При назначенной технической ответственности за выбор точки восстановления из неполной цепочки обосновывает достижимые данные либо невозможность восстановления и передаёт границу потери владельцу межсистемного восстановления. |
| required | `b3.level-outcome.enforce-store-access-boundaries-l3-defend-uncertain-decision` | Выбирает границу доступа и аудита с учётом обходов. |
| required | `b3.level-outcome.diagnose-store-maintenance-needs-l1-explain-observed-behavior` | Понимает ограничения обслуживания без обязательства ежедневной эксплуатации. |
| conditional | `b3.level-outcome.diagnose-store-maintenance-needs-l3-defend-uncertain-decision` | При назначенной технической ответственности за выбор обслуживания при неоднозначной деградации различает рост данных, задержку очищения и неудачный план, определяет безопасное действие и условия остановки. |
| required | `b3.level-outcome.select-operational-store-model-l3-defend-uncertain-decision` | Защищает выбор модели при неопределённых требованиях. |
| conditional | `b3.level-outcome.validate-nonrelational-store-contract-l3-defend-uncertain-decision` | При ответственности за технический контракт выбранного нереляционного store. |

Итого в двух RoleViews: 79 явных role links (43 required, 18 deepening, 18 conditional), включая 11 сохранённых reference links. Backend: 43 связи (21 required, 12 deepening, 10 conditional); Architecture: 36 связей (22 required, 6 deepening, 8 conditional). Новые операционные conditional не передают B3 platform automation, incident leadership или организационную policy. Единственный L4 остаётся reference-внедрением правил конкурентного доступа; новые L4/L5 не выводятся из track-level targets.
