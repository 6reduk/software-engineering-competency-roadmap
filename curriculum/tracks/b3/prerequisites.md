---
artifact: b3-prerequisite-blueprint
status: accepted
updated: 2026-09-09
language: ru
---

# Входные умения и зависимости B3

Для проверки конкурентных транзакций нужно уметь читать состояние и различать действия участников. При этом установка сервера и выбор библиотеки не являются профессиональными способностями, предшествующими каждому действию B3. Каталог отделяет необходимые умения от полезного порядка обучения и подготовки конкретной среды. Формат записей определён в [README](README.md#aggregate-catalog-notation).

## Internal hard-prerequisite DAG

Ниже — сохранённый reference-подграф; полный batch-граф дан в конце каталога.

Жёсткая связь (`Requires`) означает, что зависимое действие опирается на способность объяснить наблюдаемый исход. Это не требование заранее завершить весь модуль или все уровни prerequisite.

| Capability | Requires | Почему hard |
|---|---|---|
| `b3.capability.protect-store-invariants` | `b3.capability.explain-transaction-anomalies` | Проверка защиты требует отличить исходную аномалию от неверно построенного расписания и объяснить, что именно изменилось. Без этой способности зелёный результат не обосновывает защиту |

Оба ID разрешаются в [каталоге capabilities](capabilities.md). Вектор записи направлен от зависимой способности к prerequisite. Порядок изучения обратный: сначала объяснение аномалий, затем защита. Узлы `b3.capability.explain-transaction-anomalies` и `b3.capability.diagnose-transaction-conflicts` не имеют internal hard prerequisites.

Один из допустимых топологических порядков: `b3.capability.explain-transaction-anomalies`, `b3.capability.diagnose-transaction-conflicts`, `b3.capability.protect-store-invariants`. Capability `diagnose-transaction-conflicts` не связана hard-рёбрами с двумя другими узлами и может стоять до, между или после них. Единственное обязательное ограничение порядка изучения: `explain-transaction-anomalies` должно предшествовать `protect-store-invariants`. В графе три узла и одно ребро; конечный узел ребра не имеет исходящих Requires, поэтому возврат к исходному узлу невозможен. Этот вывод относится только к internal hard graph, не к будущему глобальному графу треков.

## Related: полезные связи без обязательного порядка

| Capability | Related | Почему не hard |
|---|---|---|
| `b3.capability.explain-transaction-anomalies` | `b3.capability.diagnose-transaction-conflicts` | Сигналы конфликта помогают объяснять результат, но аномалия может проявиться при успешных commit без блокирующего ожидания; диагностику ожидания можно учить по заданному следу |
| `b3.capability.protect-store-invariants` | `b3.capability.diagnose-transaction-conflicts` | Диагностика помогает оценить цену защиты, но первое применение заданного механизма может использовать уже определённые исходы; самостоятельное расследование всех конфликтов не обязательно |

`Related` раскрывается как направленная навигационная связь `relates-to`, а не дополнительное ребро DAG. Обратные строки не обязательны. Отсутствие hard edge не отрицает полезной последовательности: перед самостоятельной защитой разумно познакомиться с типовыми конфликтами, особенно если выбранный механизм их создаёт.

## Минимальная relational/SQL подготовка

Для всех трёх действий требуется прочитать небольшую таблицу, выделить строки ключом и условием, понять простой подсчёт строк и выполнить ограниченное изменение. Инженер должен отличать результат запроса от сохранённого состояния, connection от transaction, commit от rollback, и уметь записать бизнес-правило через состояние данных. В истории дежурных это означает проверить, остаётся ли хотя бы один дежурный, и понимать, какую строку меняет каждый участник.

Эта входная спецификация reference не требует освоения всех новых capabilities relational-model-schema или sql-querying и не меняет пустой track-wide hard baseline [B3 skeleton](../catalog/b3-transactional-data.md). Нормализация, сложные joins/windows, оптимизатор и полный SQL-курс для этого входа не требуются. Базовое знакомство с инструментом достаточно подтвердить ограниченным действием; прохождение всех будущих модулей B3 не подразумевается.

## External baseline и conditional context

Таблица задаёт требования словами и ссылками на существующих владельцев, без placeholder capability IDs. Ни одна строка не входит в internal DAG.

| Owner/context | Тип и условие | Минимально нужное умение | Потребители B3 |
|---|---|---|---|
| [B1 Python](../catalog/b1-python-engineering.md) | Conditional implementation baseline, только если оснастка написана на Python | Исключения, освобождение ресурсов, независимые соединения и сигналы координации двух участников | Воспроизведение и диагностика; Python не обязателен для technology-neutral capabilities |
| [B2 Backend](../catalog/b2-backend-api.md) | Conditional application context, если операции вызываются из сервиса | Понимать заданную границу операции и внешние эффекты; различать технический отказ транзакции и результат API | Проверка защиты и граница реакции; проектировать operation заново не требуется |
| [B5 Distributed systems](../catalog/b5-distributed-systems.md) | Conditional integration context при выходе наблюдений к нескольким системам | Различать гарантию одного store и межсистемную гарантию, назвать владельца внешнего повтора/эффекта | Защита L3/L4 и передача ограничений; consensus/saga не prerequisite локального опыта |
| [B6 Platform](../catalog/b6-platform-cloud.md) | Conditional environment context, если нужны контейнеры или иные platform primitives | Запустить выделенную среду, получить ограниченный диагностический доступ, понимать границы выделенных ресурсов | Подготовка будущего опыта; не B6 implementation внутри blueprint |
| [B7 Reliability](../catalog/b7-reliability-production.md) | Conditional production context при использовании результатов в реальных workloads | Отличать локальный conflict от incident/SLO и согласовать передачу последствий владельцу надёжности | Диагностика L3, защита L4; on-call/DR не локальные prerequisites |

Для эксплуатационных модулей сохраняется указанная skeleton условная A3 Linux/network/security подготовка. Для новых эксплуатационных модулей baseline применяется условно, без нового обязательного gate.

## Среда не становится capability edge

Точный server build, driver, настройки, барьеры, доступность диагностики, лимиты ожиданий и очистка выделенных данных принадлежат readiness конкретного будущего content package. Они остаются неподтверждёнными по [intake](../../../governance/planning/intakes/b3-transaction-isolation-boundary.md). Readiness S07/S15 не переносится. Когда у внешнего владельца появится подходящая capability, возможная hard edge потребует отдельного решения и проверки глобального DAG; сейчас такой связи нет.

## Зависимости полного batch

Reference-подграф выше сохранён: `diagnose-transaction-conflicts` по-прежнему свободна от hard-рёбер, а единственное ограничение внутри reference — объяснение аномалий перед защитой. В полном графе 23 узла и 8 рёбер, включая reference-ребро. Направление Requires: зависимая capability → prerequisite. Все не перечисленные в таблице зависимыми узлы не имеют internal hard prerequisites.

| Capability | Requires | Почему hard |
|---|---|---|
| `b3.capability.enforce-relational-constraints` | `b3.capability.model-relational-structure` | Чтобы ограничить допустимые состояния, нужно определить идентичность, связи и зависимости данных. |
| `b3.capability.derive-grouped-window-results` | `b3.capability.compose-relational-queries` | Группировка и окна опираются на корректно сформированный набор строк; иначе сверяется результат над неверным входом. |
| `b3.capability.diagnose-store-crash-recovery` | `b3.capability.explain-store-durability` | Диагноз recovery требует связать журнал и страницы с ожидаемым сохранённым состоянием. |
| `b3.capability.choose-query-indexes` | `b3.capability.diagnose-query-plans` | Проверяемый выбор индекса требует определить, как фактически изменился путь доступа и работа запроса. |
| `b3.capability.validate-online-data-change` | `b3.capability.plan-compatible-schema-transitions` | Backfill с текущими writers допустим только при определённых совместимых промежуточных состояниях. |
| `b3.capability.validate-store-failover` | `b3.capability.assess-replica-data-guarantees` | Выбор кандидата и сверка после promotion требуют оценить подтверждённые и применённые данные. |
| `b3.capability.verify-store-point-in-time-restore` | `b3.capability.design-store-backup-chain` | Проверяемый restore требует установить пригодность всей цепочки, а не только наличие одного файла. |

Каждое из восьми рёбер ведёт к узлу без собственных Requires; следовательно, цикла нет. Один из допустимых порядков изучения: сначала в любом порядке все 15 узлов без Requires, затем в любом порядке восемь зависимых узлов из обеих таблиц. Это не единственный порядок: каждую зависимую capability можно изучать сразу после её prerequisite. Сравнивается необходимое умение, не завершение всего prerequisite module и всех его уровней.

| Capability | Related | Почему не hard |
|---|---|---|
| `b3.capability.diagnose-query-plans` | `b3.capability.compose-relational-queries` | Смысл запроса помогает диагностике, но план можно исследовать по уже заданному контракту результата. |
| `b3.capability.plan-compatible-schema-transitions` | `b3.capability.model-relational-structure` | Схема может быть задана другим владельцем; перепроектировать модель до анализа перехода необязательно. |
| `b3.capability.validate-online-data-change` | `b3.capability.diagnose-transaction-conflicts` | Диагностика конфликтов полезна для online change; первый bounded action может использовать готовые сигналы и условия остановки. |
| `b3.capability.assess-replica-data-guarantees` | `b3.capability.explain-store-durability` | Путь журнала помогает углублению, но гарантии реплики можно проверить по заданному контракту подтверждений. |
| `b3.capability.design-store-backup-chain` | `b3.capability.explain-store-durability` | Внутренний путь записи помогает объяснить цепочку, но пригодность готового формата можно проверять по его контракту. |
| `b3.capability.design-store-partitioning` | `b3.capability.choose-query-indexes` | Индексы и partitioning взаимодействуют; выбор разбиения возможен с уже заданными путями доступа. |
| `b3.capability.assess-store-scaling-limits` | `b3.capability.diagnose-query-plans` | План помогает отделить неэффективный запрос от нехватки ресурсов; диагностика ресурса не всегда требует анализа SQL. |
| `b3.capability.diagnose-store-maintenance-needs` | `b3.capability.diagnose-query-plans` | Статистика связывает обслуживание с планом; обслуживание места можно диагностировать независимо. |
| `b3.capability.validate-nonrelational-store-contract` | `b3.capability.select-operational-store-model` | Store может быть выбран заранее; независимая проверка его контракта не требует заново выбирать семейство. |
| `b3.capability.enforce-store-access-boundaries` | `b3.capability.diagnose-store-maintenance-needs` | Права диагностики помогают обслуживанию, но проверка доступа не требует навыка обслуживания engine. |

### Внешняя подготовка и границы

Все внешние требования задаются словами, без новых capability IDs и без глобальных hard edges. Для чтения таблиц и ключей достаточно входных умений reference: новые relational/SQL capabilities не становятся обязательным барьером перед TC01–TC03.

| Контекст | Необходимая подготовка / передача владельцу |
|---|---|
| [A3 foundations](../catalog/a3-networks-linux-security.md) | Для эксплуатационных действий: процессы, файловая система, сеть, аутентификация и безопасный доступ к выделенной среде; условный baseline skeleton |
| [B1](../catalog/b1-python-engineering.md) | Только для Python-оснастки: ресурсы, исключения и соединения; язык не является prerequisite всей вертикали |
| [B2](../catalog/b2-backend-api.md) | Заданные операции, writers/readers и контракт приложения для схемы, SQL, migration и nonrelational store; API, ORM, cache integration и rollout приложения остаются B2 |
| [B4](../catalog/b4-data-engineering.md) | При analytical потребителе понимать границу operational source; pipelines и warehouses не входят в SQL или store selection B3 |
| [B5](../catalog/b5-distributed-systems.md) | При выходе за engine topology различать локальную гарантию и distributed coordination; общие replication/sharding/consistency algorithms остаются B5 |
| [B6](../catalog/b6-platform-cloud.md) | Получить выделенные ресурсы, platform permissions и назначение восстановления; IaC, orchestration, IAM и автоматизация failover не создаются в B3 |
| [B7](../catalog/b7-reliability-production.md) | Получить требования доступности и допустимой потери, условия вмешательства; передать пределы store restore/failover и наблюдения, не объявлять cross-system continuity |
| [B10](../catalog/b10-llm-applications.md) | При retrieval-сценарии отделить operational search от vector retrieval, RAG и оценки качества поиска приложения |
| [C1](../catalog/c1-leadership-architecture.md) | Согласованные ограничения и владельцы решения; выбор локального store не становится организационной архитектурной policy |

### Future readiness questions

Для будущего технически зависимого slice отдельно установить: точный engine/build и driver; семантику DDL, блокировок и возобновления backfill; доступность планов/статистики и безопасный способ наблюдения; режимы подтверждения репликации, исключения старого writer и повторного присоединения; совместимость копий, непрерывность журнала, ключи и достижимую PITR-точку; доступность аудита и полномочия обслуживания; фактические atomicity, index refresh, expiry/eviction выбранного nonrelational store. Эти вопросы не являются hard capability edges и не имеют ответа runtime в этом batch.
