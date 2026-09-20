---
artifact: b2-level-outcome-blueprint
status: accepted
updated: 2026-08-15
language: ru
---

# LevelOutcomes B2

Каждый outcome использует aggregate metadata/defaults из `README.md`. Таблицы разделяют действие, контекст/автономность и evidence. Один artifact может поддерживать несколько outcomes, но один тест не доказывает уровень целиком.

## Общие evidence guardrails

- Любой заявленный bound, budget, capacity или amplification limit называет workload, длительность, dependency/failure behavior и измеримый acceptance threshold.
- Cleanup evidence действует только внутри указанной controllable lifecycle boundary; process kill, crash, uncancellable work и remote side effects рассматриваются отдельно.
- L4 policy/convention подтверждается не наличием документа, а применением несколькими командами: adoption или завершённым этапом migration, обработанными exceptions и наблюдаемым feedback loop.

## `b2.capability.trace-request-execution`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.trace-request-execution-l1-follow-known-path` | L1 | С поддержкой прослеживает заданный request path через router, dependencies/middleware и handler | Верно предсказывает порядок существенных шагов и находит место формирования response/error |
| `b2.level-outcome.trace-request-execution-l2-diagnose-common-failure` | L2 | Самостоятельно локализует типовой routing, validation или middleware failure | Воспроизводит проблему, подтверждает границу сбоя logs/test и исправляет без случайного обхода pipeline |
| `b2.level-outcome.trace-request-execution-l3-explain-production-path` | L3 | При неполной информации восстанавливает production request path через application components | Строит проверяемую гипотезу, добавляет минимальную instrumentation и объясняет state/resource consequences |

## `b2.capability.manage-service-resource-lifecycle`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.manage-service-resource-lifecycle-l1-use-defined-scope` | L1 | Использует заданный request/application scope и cleanup mechanism | В контролируемой boundary ресурс освобождается на success/error path; crash/process limits названы |
| `b2.level-outcome.manage-service-resource-lifecycle-l2-design-local-lifecycle` | L2 | Самостоятельно выбирает lifecycle для типовой dependency | Обосновывает scope, реализует bounded/deterministic cleanup и проверяет startup/shutdown/error paths |
| `b2.level-outcome.manage-service-resource-lifecycle-l3-remediate-leak` | L3 | Диагностирует нетипичную утечку или shutdown race в сервисе | Связывает symptom с lifecycle, устраняет причину и подтверждает bounded resource use |
| `b2.level-outcome.manage-service-resource-lifecycle-l4-establish-service-policy` | L4 | Согласует lifecycle/resource policy для нескольких сервисов или библиотек | Defaults применены минимум в двух контекстах; exceptions, migration и production feedback изменяют policy |

## `b2.capability.design-http-api-contracts`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.design-http-api-contracts-l1-implement-specified-contract` | L1 | Реализует локальный endpoint по заданному контракту и conventions | Status, headers, schema и error behavior соответствуют contract tests |
| `b2.level-outcome.design-http-api-contracts-l2-design-typical-resource` | L2 | Самостоятельно проектирует типовой resource/operation contract | Контракт однозначен для клиента, использует корректную HTTP semantics и покрывает invalid path |
| `b2.level-outcome.design-http-api-contracts-l3-resolve-ambiguous-requirements` | L3 | Проектирует service contract при неоднозначных требованиях и operational constraints | Фиксирует alternatives/trade-offs, client workflows, failure semantics и проверяемые NFR |
| `b2.level-outcome.design-http-api-contracts-l4-establish-cross-team-conventions` | L4 | Определяет технические API conventions для нескольких команд | Conventions решают повторяющиеся проблемы, имеют exceptions/versioning и adoption evidence |

## `b2.capability.evolve-api-contracts`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.evolve-api-contracts-l1-apply-additive-change` | L1 | С поддержкой выполняет заданное additive изменение | Старые contract tests проходят, новое поведение явно проверено |
| `b2.level-outcome.evolve-api-contracts-l2-plan-compatible-change` | L2 | Самостоятельно классифицирует и реализует типовое изменение | Обнаруживает breaking aspects, выбирает compatible shape и добавляет regression/consumer checks |
| `b2.level-outcome.evolve-api-contracts-l3-own-service-migration` | L3 | Владеет миграцией контракта сервиса при сосуществовании клиентов | Есть inventory consumers, rollout/deprecation plan, telemetry и критерии завершения/отката |
| `b2.level-outcome.evolve-api-contracts-l4-lead-cross-team-migration` | L4 | Проводит межкомандную миграцию нескольких producers/consumers | Согласованы sequencing и ownership; migration достигает цели без незапланированного нарушения клиентов |

## `b2.capability.design-validation-error-contracts`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.design-validation-error-contracts-l1-follow-error-convention` | L1 | Реализует заданные validation и error conventions | Ошибки стабильны, не раскрывают лишние детали и покрыты negative tests |
| `b2.level-outcome.design-validation-error-contracts-l2-design-client-errors` | L2 | Проектирует validation/error behavior типовой операции | Клиент может различить retry/correction/failure; serialization edge cases проверены |
| `b2.level-outcome.design-validation-error-contracts-l3-unify-service-boundaries` | L3 | Устраняет противоречивые error boundaries внутри сервиса | Сохраняет совместимость либо планирует миграцию; diagnostics и client semantics разделены |
| `b2.level-outcome.design-validation-error-contracts-l4-establish-shared-convention` | L4 | Определяет переиспользуемый error convention для нескольких команд | Convention применён несколькими consumers/producers; taxonomy, security limits, exceptions и feedback проверены миграцией |

## `b2.capability.integrate-identity-access-control`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.integrate-identity-access-control-l1-enforce-defined-rule` | L1 | Применяет заданное auth rule на endpoint/resource boundary | Positive/negative tests различают unauthenticated, forbidden и allowed paths без утечки данных |
| `b2.level-outcome.integrate-identity-access-control-l2-propagate-context` | L2 | Проводит subject/tenant context через типовой service flow | Enforcement не зависит от client-supplied identity; audit context сохраняется |
| `b2.level-outcome.integrate-identity-access-control-l3-design-service-enforcement` | L3 | Проектирует enforcement points сервиса при сложных resource relationships | Threat cases и bypass paths рассмотрены; authorization остаётся проверяемой и deny-by-default |
| `b2.level-outcome.integrate-identity-access-control-l4-align-cross-service-policy` | L4 | Согласует техническую access-control integration для нескольких сервисов | Завершён проверяемый этап migration; trust boundaries, propagation, exceptions и audit feedback проверены с security/platform owners |

## `b2.capability.enforce-api-security-abuse-controls`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.enforce-api-security-abuse-controls-l1-apply-defined-controls` | L1 | Применяет заданные field/body/operation limits и безопасную binding convention | Negative tests блокируют oversized/unknown/forbidden input без раскрытия чувствительных данных |
| `b2.level-outcome.enforce-api-security-abuse-controls-l2-protect-typical-endpoint` | L2 | Самостоятельно определяет abuse controls типового endpoint | Request/cost bounds, field exposure, quota/rate и untrusted target rules связаны с threat cases и тестами |
| `b2.level-outcome.enforce-api-security-abuse-controls-l3-design-service-abuse-boundary` | L3 | Проектирует защиту сервиса при multi-tenant/adversarial workload и неоднозначной стоимости операции | Abuse paths воспроизведены; controls сохраняют legitimate use, tenant isolation и bounded resource envelope |
| `b2.level-outcome.enforce-api-security-abuse-controls-l4-establish-cross-service-controls` | L4 | Внедряет переиспользуемые API security/abuse defaults для нескольких команд | Defaults применены в нескольких сервисах; exceptions, false positives, bypass attempts и operational feedback отслеживаются |

## `b2.capability.design-service-architecture`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.design-service-architecture-l1-follow-existing-boundaries` | L1 | Добавляет локальную функцию, сохраняя заданные boundaries | Изменение не вводит обратную dependency и тестируется на принятой границе |
| `b2.level-outcome.design-service-architecture-l2-structure-typical-feature` | L2 | Самостоятельно размещает типовую feature между application/domain/adapters | Dependency direction объяснено; business behavior тестируется без ненужного I/O |
| `b2.level-outcome.design-service-architecture-l3-reshape-changing-service` | L3 | Перестраивает service boundaries под неопределённые требования и накопленный coupling | Есть evidence pain, альтернативы, incremental plan и измеримое снижение change risk |
| `b2.level-outcome.design-service-architecture-l4-establish-reusable-boundaries` | L4 | Формирует применимые architecture conventions для нескольких сервисов | Conventions не превращаются в обязательный framework, допускают exceptions и подтверждены несколькими use cases |

## `b2.capability.manage-application-transaction-boundaries`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.manage-application-transaction-boundaries-l1-use-defined-unit` | L1 | Выполняет изменение данных в заданной transaction/unit-of-work boundary | Success commit и failure rollback подтверждены integration test |
| `b2.level-outcome.manage-application-transaction-boundaries-l2-design-operation-boundary` | L2 | Самостоятельно выбирает boundary для типовой application operation | Не удерживает transaction через ненужный I/O; error/retry behavior определено |
| `b2.level-outcome.manage-application-transaction-boundaries-l3-resolve-side-effect-consistency` | L3 | Проектирует operation с database state и внешними side effects | Failure windows перечислены; выбран механизм recovery/idempotency с проверяемыми invariants |

## `b2.capability.integrate-application-caching`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.integrate-application-caching-l2-apply-known-cache-pattern` | L2 | Интегрирует cache для типового read path по выбранной strategy | Key/tenant scope, TTL/miss/stale/failure behavior определены; tests доказывают отсутствие cross-tenant leakage |
| `b2.level-outcome.integrate-application-caching-l3-design-consistency-failure-behavior` | L3 | Проектирует caching при concurrent miss, invalidation races, commit ordering и cache failure | Freshness invariant и failure windows объяснены; stampede/stale/recovery проверены в измеримом workload envelope |
| `b2.level-outcome.integrate-application-caching-l4-coordinate-cache-migration` | L4 | Проводит изменение shared cache/key/invalidation convention между несколькими сервисами | Завершён migration stage; mixed-version behavior, load shift, rollback/flush risk и production feedback проверены |

## `b2.capability.design-idempotent-service-operations`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.design-idempotent-service-operations-l2-implement-known-pattern` | L2 | Реализует idempotency для типовой create/command operation | Duplicate/concurrent requests дают определённый результат; key scope и retention заданы |
| `b2.level-outcome.design-idempotent-service-operations-l3-design-failure-safe-operation` | L3 | Выбирает idempotency semantics при retries, partial failures и concurrency | Invariants и failure windows объяснены; tests воспроизводят duplicates/races/recovery |
| `b2.level-outcome.design-idempotent-service-operations-l4-align-operation-contracts` | L4 | Согласует idempotency convention между несколькими producers/consumers | Identity/result/conflict/expiry semantics совместимы и имеют migration/adoption plan |

## `b2.capability.integrate-external-services`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.integrate-external-services-l1-use-defined-client` | L1 | Использует заданный client adapter и обрабатывает известные outcomes | Timeout/error paths не маскируются, resource cleanup проверен |
| `b2.level-outcome.integrate-external-services-l2-design-typical-client-boundary` | L2 | Самостоятельно интегрирует типовую dependency | Timeout, error mapping, pool lifecycle и safe retry decision определены и протестированы |
| `b2.level-outcome.integrate-external-services-l3-own-degraded-dependency` | L3 | Проектирует поведение сервиса при медленной/частично доступной dependency | Deadline budget, degradation и observability подтверждены failure injection |
| `b2.level-outcome.integrate-external-services-l4-align-integration-policy` | L4 | Определяет технические integration defaults для нескольких команд | Defaults имеют evidence, exceptions и migration plan; не скрывают domain-specific failure semantics |

## `b2.capability.design-asynchronous-workflows`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.design-asynchronous-workflows-l2-implement-background-flow` | L2 | Реализует заданный background/message flow | Ack/retry/error ownership определены; duplicate и poison path проверены |
| `b2.level-outcome.design-asynchronous-workflows-l3-design-recoverable-workflow` | L3 | Проектирует workflow при partial failures и повторной доставке | State transitions/invariants наблюдаемы; replay/recovery не нарушают бизнес-результат |
| `b2.level-outcome.design-asynchronous-workflows-l4-coordinate-workflow-migration` | L4 | Проводит изменение workflow между несколькими командами | Завершён migration stage; producer/consumer sequencing, compatibility и recovery проверены, feedback учтён |

## `b2.capability.control-concurrency-cancellation`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.control-concurrency-cancellation-l1-preserve-cleanup` | L1 | Следует заданному cancellation/cleanup pattern | В контролируемой boundary cancellation test не оставляет running task/ресурс; crash и uncancellable limits названы |
| `b2.level-outcome.control-concurrency-cancellation-l2-bound-local-work` | L2 | Ограничивает конкурентную работу типового endpoint/job | Limit и deadline обоснованы; overload/cancel path предсказуем и протестирован |
| `b2.level-outcome.control-concurrency-cancellation-l3-remediate-runtime-failure` | L3 | Диагностирует starvation, orphan work или cancellation leak под нагрузкой | Root cause подтверждён telemetry/experiment; исправление ограничивает amplification |
| `b2.level-outcome.control-concurrency-cancellation-l4-establish-runtime-policy` | L4 | Согласует deadline/cancellation/concurrency policy нескольких сервисов | End-to-end budgets и ownership непротиворечивы; rollout не создаёт каскадных отказов |

## `b2.capability.verify-service-behavior`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.verify-service-behavior-l1-test-local-behavior` | L1 | Добавляет test для локального success/error behavior по заданному подходу | Test обнаруживает целевую регрессию и не зависит от несущественных деталей |
| `b2.level-outcome.verify-service-behavior-l2-select-test-boundaries` | L2 | Самостоятельно выбирает unit/integration/E2E boundaries типовой feature | Набор даёт нужную confidence с контролируемой стоимостью и failure localization |
| `b2.level-outcome.verify-service-behavior-l3-design-service-strategy` | L3 | Перестраивает verification strategy сервиса по рискам и production failures | Critical paths/failure modes покрыты; flaky/slow duplication сокращено измеримо |
| `b2.level-outcome.verify-service-behavior-l4-align-cross-team-evidence` | L4 | Определяет общие service verification expectations нескольких команд | Expectations risk-based, допускают stack-specific реализацию и используются в release decisions |

## `b2.capability.verify-contract-compatibility`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.verify-contract-compatibility-l1-maintain-contract-check` | L1 | Обновляет заданную contract check вместе с additive change | Старый consumer case сохраняется, новый behavior проверен |
| `b2.level-outcome.verify-contract-compatibility-l2-detect-breaking-change` | L2 | Самостоятельно проверяет типовое producer change | Schema/semantic incompatibility обнаружена до rollout; false confidence limitations объяснены |
| `b2.level-outcome.verify-contract-compatibility-l3-build-consumer-evidence` | L3 | Организует compatibility evidence для сервиса с несколькими consumers | Consumer inventory/versions и semantic checks связаны с migration decision |
| `b2.level-outcome.verify-contract-compatibility-l4-establish-compatibility-process` | L4 | Внедряет межкомандный механизм обнаружения breaking changes | Ownership, exceptions, stale consumers и enforcement path определены; escape rate отслеживается |

## `b2.capability.deliver-service-changes-safely`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.deliver-service-changes-safely-l1-follow-rollout-checklist` | L1 | Выполняет локальный change по заданному rollout/rollback checklist | Проверяет pre/post conditions и корректно останавливается при нарушении |
| `b2.level-outcome.deliver-service-changes-safely-l2-plan-typical-rollout` | L2 | Самостоятельно планирует rollout типовой совместимой service change | Order, verification, rollback/roll-forward и ownership явны |
| `b2.level-outcome.deliver-service-changes-safely-l3-own-risky-migration` | L3 | Проводит рискованное изменение сервиса при ограниченной обратимости | Risk reduction, observability, staged exposure и incident path подтверждены до rollout |
| `b2.level-outcome.deliver-service-changes-safely-l4-coordinate-cross-team-change` | L4 | Координирует технический rollout нескольких сервисов/команд | Dependencies, stop conditions, communication и recovery отрепетированы и выполнены |

## `b2.capability.diagnose-service-performance`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.diagnose-service-performance-l2-localize-common-bottleneck` | L2 | Самостоятельно локализует типовой latency/throughput bottleneck | Использует measurement/profile, отличает symptom от cause и подтверждает improvement |
| `b2.level-outcome.diagnose-service-performance-l3-investigate-production-degradation` | L3 | Исследует нелинейную или intermittent деградацию production-сервиса | Correlates resource/saturation/request evidence, воспроизводит либо фальсифицирует гипотезы |
| `b2.level-outcome.diagnose-service-performance-l4-lead-cross-service-analysis` | L4 | Ведёт анализ bottleneck через несколько сервисов и команд | Общая measurement model локализует constraint; решения учитывают shifting bottleneck и cost |

## `b2.capability.control-service-load-resources`

| ID | Уровень | Действие, контекст и автономность | Evidence criteria |
|---|---:|---|---|
| `b2.level-outcome.control-service-load-resources-l2-configure-local-bounds` | L2 | Выбирает bounded pool/concurrency/queue для типового сервиса | Bounds связаны с dependency capacity; overload path проверен нагрузкой |
| `b2.level-outcome.control-service-load-resources-l3-design-graceful-overload` | L3 | Проектирует service behavior при saturation и burst traffic | Admission/backpressure/degradation сохраняют критические invariants и recovery |
| `b2.level-outcome.control-service-load-resources-l4-align-capacity-boundaries` | L4 | Согласует resource/load boundaries цепочки сервисов | Limits и timeout budgets не усиливают overload; ownership и capacity evidence определены |

## Почему некоторые capabilities начинаются с L2 или заканчиваются на L3

- `integrate-application-caching`, `design-idempotent-service-operations`, `design-asynchronous-workflows`, `diagnose-service-performance` и `control-service-load-resources` не получают искусственный L1: их самостоятельное наблюдаемое действие начинается с выбора failure/consistency/measurement boundary. Выполнение заданного локального шага уже покрывается базовыми service capabilities и не доказывает эти способности отдельно.
- `trace-request-execution` заканчивается на L3: межкомандные tracing/observability conventions принадлежат B7, а B2 сохраняет service-level применение.
- `manage-application-transaction-boundaries` заканчивается на L3: cross-service consistency и distributed transaction mechanisms принадлежат B5, store-level semantics — B3. B2 не создаёт дублирующий L4 outcome только ради полноты таблицы.

## Почему нет L5 outcomes

B2 имеет естественный диапазон L1–L4. На текущем zoom не найдено самостоятельного B2-owned L5-действия, которое не превращается в organizational architecture/reliability governance C1/B7. Это допустимый результат метамодели, а не пробел для искусственного заполнения.
