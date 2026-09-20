---
id: b3.index.transactions-concurrency-blueprint
kind: index
title: B3 — полный capability blueprint первого breadth-pass
owner_track: b3
status: accepted
updated: 2026-09-13
language: ru
---

# B3: проектировать и проверять operational data stores

Первый полный breadth-pass представляет все 11 кластеров [B3 skeleton](../catalog/b3-transactional-data.md): принятый transactions/concurrency reference и десять новых кластеров одним batch по [M1.9.2](../../../governance/work-packages/M1.9.2-b3-remaining-clusters-breadth-pass.md). Это карта профессиональных действий и ожидаемых результатов; учебные материалы и исполнение сценариев здесь не создавались.

[G22](../../../governance/reviews/M1.9.1-G22-b3-transactions-concurrency-blueprint-acceptance.md) закрепляет transactions/concurrency reference: его module, три capabilities, десять outcomes, TC01–TC03 и 11 role links.

## Семь файлов blueprint

[Фазовый итог первого прохода B3](phase-closeout.md): два маршрута, покрытие, долг и предложение следующего шага.

| Файл | Назначение |
|---|---|
| [README](README.md) | Карта всех кластеров |
| [Modules](modules.md) | 11 навигационных домов по профессиональному результату |
| [Capabilities](capabilities.md) | 23 различимых действия |
| [LevelOutcomes](level-outcomes.md) | 70 ожидаемых результатов |
| [Prerequisites](prerequisites.md) | Internal hard DAG, Related, внешняя подготовка и readiness questions |
| [Scenarios](scenarios.md) | 13 будущих рабочих входов |
| [Role requirements](role-requirements.md) | Две RoleViews и 79 конкретных связей |

## Карта batch

В таблице полные semantic IDs; сценарии имеют локальные метки. Строка reference сохраняет прежний контракт, остальные десять составляют принятый breadth-pass.

| Cluster | Module | Capabilities | Outcomes | Scenarios |
|---|---|---|---:|---|
| `b3.cluster.transactions-concurrency` | `b3.module.preserve-concurrent-data-invariants` | `b3.capability.explain-transaction-anomalies`, `b3.capability.protect-store-invariants`, `b3.capability.diagnose-transaction-conflicts` | 10 | [TC01](scenarios.md#tc01), [TC02](scenarios.md#tc02), [TC03](scenarios.md#tc03) |
| `b3.cluster.relational-model-schema` | `b3.module.encode-relational-data-rules` | `b3.capability.model-relational-structure`, `b3.capability.enforce-relational-constraints` | 6 | [RM01](scenarios.md#rm01) |
| `b3.cluster.sql-querying` | `b3.module.derive-correct-query-results` | `b3.capability.compose-relational-queries`, `b3.capability.derive-grouped-window-results` | 6 | [SQ01](scenarios.md#sq01) |
| `b3.cluster.storage-wal-recovery` | `b3.module.reason-about-durable-store-state` | `b3.capability.explain-store-durability`, `b3.capability.diagnose-store-crash-recovery` | 6 | [WR01](scenarios.md#wr01) |
| `b3.cluster.indexes-optimizer` | `b3.module.improve-store-query-access` | `b3.capability.diagnose-query-plans`, `b3.capability.choose-query-indexes` | 6 | [IO01](scenarios.md#io01) |
| `b3.cluster.schema-evolution` | `b3.module.evolve-store-schema-safely` | `b3.capability.plan-compatible-schema-transitions`, `b3.capability.validate-online-data-change` | 6 | [SE01](scenarios.md#se01) |
| `b3.cluster.replication-ha` | `b3.module.preserve-store-guarantees-on-failover` | `b3.capability.assess-replica-data-guarantees`, `b3.capability.validate-store-failover` | 6 | [RH01](scenarios.md#rh01) |
| `b3.cluster.partitioning-scaling` | `b3.module.scale-store-workload-within-limits` | `b3.capability.design-store-partitioning`, `b3.capability.assess-store-scaling-limits` | 6 | [PS01](scenarios.md#ps01) |
| `b3.cluster.backup-restore-dr` | `b3.module.prove-store-data-recoverability` | `b3.capability.design-store-backup-chain`, `b3.capability.verify-store-point-in-time-restore` | 6 | [BR01](scenarios.md#br01) |
| `b3.cluster.security-operations` | `b3.module.operate-store-with-controlled-access` | `b3.capability.enforce-store-access-boundaries`, `b3.capability.diagnose-store-maintenance-needs` | 6 | [SO01](scenarios.md#so01) |
| `b3.cluster.operational-nonrelational-stores` | `b3.module.choose-and-validate-operational-store` | `b3.capability.select-operational-store-model`, `b3.capability.validate-nonrelational-store-contract` | 6 | [ON01](scenarios.md#on01) |

Итого: 11 modules, 23 capabilities, 70 outcomes (23 L1, 23 L2, 23 L3, один L4), 13 scenarios, 79 role links (43 required, 18 deepening, 18 conditional). Новая часть: 10 modules, 20 capabilities, 60 outcomes, 10 scenarios, 68 role links.

## Как читать модель

Cluster классифицирует область и не получает уровень. Module даёт устойчивый навигационный дом. Capability — наблюдаемое профессиональное действие; LevelOutcome уточняет самостоятельность, неопределённость и критерии результата. Scenario — будущая рабочая точка входа, не готовое задание. Ни наличие сущностей, ни принятие blueprint не доказывают proficiency и не создают учебного coverage.

## Ownership и пределы zoom

Имя этого anchor сохранено для входящих ссылок reference; текущий scope — весь B3 breadth-pass.

B3 владеет моделью и поведением operational store, SQL, engine internals, путями доступа, локальными изменениями схемы, репликацией конкретного store, partitioning, восстановлением его данных, доступом и обслуживанием. Один store может иметь несколько узлов; это не присвоение общей distributed theory.

| Владелец | Граница, сохраняемая в batch |
|---|---|
| [B1](../catalog/b1-python-engineering.md) | Язык/runtime и Python-оснастка |
| [B2](../catalog/b2-backend-api.md) | Application persistence, API, ORM, идемпотентность, cache integration и контракт потребителей при миграции |
| [B4](../catalog/b4-data-engineering.md) | Analytical pipelines и warehouses; operational SQL не становится ETL |
| [B5](../catalog/b5-distributed-systems.md) | Общие consistency, replication/sharding algorithms и cross-system coordination |
| [B6](../catalog/b6-platform-cloud.md) | Provisioning, platform IAM, rollout и failover automation |
| [B7](../catalog/b7-reliability-production.md) | SLO, incident process, cross-system RTO/RPO, continuity и DR exercises; B3 проверяет данные одного store |
| [B10](../catalog/b10-llm-applications.md) | Vector retrieval, RAG и application retrieval evaluation |
| [C1](../catalog/c1-leadership-architecture.md) | Организационная архитектурная policy; B3 даёт технические последствия локальных решений |

Локальные non-goals указаны у каждого модуля; [внешние prerequisites](prerequisites.md#внешняя-подготовка-и-границы) сформулированы словами и ссылками на реальные tracks. A3 baseline нужен условно для эксплуатации, Python — только для соответствующей оснастки. Runtime readiness не является hard edge.

## Aggregate catalog notation

Применяется компактная запись [B2](../b2/README.md) в рамках [метаданных](../../../governance/architecture/metamodel/metadata.md), [сущностей](../../../governance/architecture/metamodel/entities.md) и [инвариантов](../../../governance/architecture/metamodel/relationships-and-invariants.md). Это способ сериализации, а не новый semantic kind.

- README имеет собственный index ID. Шесть остальных файлов — governance-каталоги с уникальным полем `artifact`; они не создают content Artifact. Их frontmatter описывает состояние каталога.
- File-level defaults записей: `owner_track: b3`, `language: ru`; значения `status` и `updated` наследуются из front matter соответствующего каталога. Defaults применяются ко всем records; состояние записи не переопределяется неявно.
- Module: heading задаёт полный `id` и `title`, подразумеваемый `kind: module`; тело задаёт scope, develops, non-goals. Проверенный runtime baseline отсутствует, поэтому `versions` и `verified_baseline` не заполняются.
- Capability: строка основной таблицы задаёт `id`, `title`, `primary_cluster`, наблюдаемое действие и primary module; подразумеваемый `kind: capability`.
- LevelOutcome: раздел задаёт ровно одну `capability`, строка — `id`, `level`, действие, контекст/самостоятельность и evidence criteria; подразумеваемый `kind: level-outcome`. Действия и критерии остаются в теле, как требует метамодель.
- `Develops`, `Requires` и `Related` содержат полные semantic IDs; `Related` раскрывается как `relates-to`. Направление `Requires`: зависимая capability → prerequisite. Сценарные метки локальны; HTML anchors — только адреса навигации.
- Раздел RoleView адресуется существующим route path/role slug. Строка ролевой таблицы — одна связь с одним LevelOutcome, условием и причиной, без нового requirement ID. Required baseline обязателен, deepening — дополнительная глубина, conditional — требование только при названной ответственности.
- При переносе в track repository defaults разворачиваются без смены [semantic IDs](../../../governance/architecture/metamodel/identifiers.md). [Registry](../../../governance/registry/repositories.yaml) пока считает repository `b3` planned; URL и несуществующие пути не выдумываются.

## Кандидаты на углубление

Рекомендуемый порядок: SQ01 → SE01 → BR01.

- **SQ01, корректность SQL-композиции:** частая ошибка с кратностью строк, компактный наблюдаемый результат и ценность для повседневной backend-работы.
- **SE01, совместимый переход схемы и backfill:** связывает данные и одновременно работающие пути записи; требует проверки конкретной семантики DDL и блокировок.
- **BR01, проверяемое восстановление в заданную точку (PITR):** позволяет отличить успешное создание копии от восстановленных данных; требует выделенной среды и пригодной цепочки резервирования.


## Учебный slice SQ01

[M1.9.3 — корректность результата SQL](slices/sql-result-correctness/README.md) развивает составление запросов и агрегаты/окна вокруг размножения строк Orders report: index, learn, interview, kata и project-spec. Материалы и их [coverage map](coverage-map.md) приняты после G24. Это принятие подтверждает качество и назначение учебного slice, но не означает выполнения заданий, proficiency участника или появления ImplementationReference.


## Учебный slice SE01

[M1.9.5 — совместимое изменение суммы Orders](slices/compatible-orders-amount-migration/README.md) связывает пять состояний схемы, старые/новые пути доступа, текущие записи, backfill, сверку и блокировки. После подтверждённого локального Gate 0, G26 и correction-pass M1.9.5a приняты index, learn, interview, kata и project-spec. В [coverage map](coverage-map.md#se01-planned-map-и-фактическая-принятая-регистрация) зарегистрированы 30 accepted-отношений SE01 и сохранены 30 accepted-отношений SQ01. Это не означает proficiency, выполнения заданий, ImplementationReference или завершения B3; BR01 не запущен.
