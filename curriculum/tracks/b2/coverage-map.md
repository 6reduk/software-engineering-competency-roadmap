---
artifact: b2-coverage-blueprint
status: accepted
updated: 2026-09-08
language: ru
---

# Предварительная coverage map B2

Легенда: `L` learn/brief, `I` interview, `K` kata, `P` project-spec. Значок означает запланированное назначение, а не существующий artifact и не подтверждённый уровень.

| Capability | L | I | K | P | Primary scenarios |
|---|:---:|:---:|:---:|:---:|---|
| `b2.capability.trace-request-execution` | ✓ | ✓ | ✓ |  | S01, S12 |
| `b2.capability.manage-service-resource-lifecycle` | ✓ | ✓ | ✓ | ✓ | S02, S08 |
| `b2.capability.design-http-api-contracts` | ✓ | ✓ | ✓ | ✓ | S03, S04 |
| `b2.capability.evolve-api-contracts` | ✓ | ✓ | ✓ | ✓ | S03, S11 |
| `b2.capability.design-validation-error-contracts` | ✓ | ✓ | ✓ | ✓ | S03, S10 |
| `b2.capability.integrate-identity-access-control` | ✓ | ✓ | ✓ | ✓ | S05, S14 |
| `b2.capability.enforce-api-security-abuse-controls` | ✓ | ✓ | ✓ | ✓ | S14 |
| `b2.capability.design-service-architecture` | ✓ | ✓ | ✓ | ✓ | S06 |
| `b2.capability.manage-application-transaction-boundaries` | ✓ | ✓ | ✓ | ✓ | S07, S15 |
| `b2.capability.integrate-application-caching` | ✓ | ✓ | ✓ | ✓ | S15 |
| `b2.capability.design-idempotent-service-operations` | ✓ | ✓ | ✓ | ✓ | S04, S07, S09 |
| `b2.capability.integrate-external-services` | ✓ | ✓ | ✓ | ✓ | S08, S13 |
| `b2.capability.design-asynchronous-workflows` | ✓ | ✓ | ✓ | ✓ | S09 |
| `b2.capability.control-concurrency-cancellation` | ✓ | ✓ | ✓ | ✓ | S02, S08, S13 |
| `b2.capability.verify-service-behavior` | ✓ | ✓ | ✓ | ✓ | S06, S10 |
| `b2.capability.verify-contract-compatibility` | ✓ | ✓ | ✓ | ✓ | S03, S10, S11 |
| `b2.capability.deliver-service-changes-safely` | ✓ | ✓ | ✓ | ✓ | S11 |
| `b2.capability.diagnose-service-performance` | ✓ | ✓ | ✓ | ✓ | S12 |
| `b2.capability.control-service-load-resources` | ✓ | ✓ | ✓ | ✓ | S08, S13, S14, S15 |

## Первый slice: artifact set M1.5

| Artifact ID | Kind | Primary coverage |
|---|---|---|
| `b2.index.evolvable-api-contracts` | index | Module navigation и prerequisites |
| `b2.learn.http-contract-execution-boundary` | learn | `trace-request-execution`, `design-http-api-contracts`, `design-validation-error-contracts` |
| `b2.learn.compatible-api-change` | learn | `evolve-api-contracts`, `verify-contract-compatibility`, `deliver-service-changes-safely` |
| `b2.interview.api-contract-evolution` | interview | L2–L4 follow-ups по design/evolution/compatibility |
| `b2.kata.compatible-delivery-contract-change` | kata | S03 с legacy/new clients |
| `b2.project-spec.evolvable-orders-api` | project-spec | Интеграция первого slice; milestone без готовой реализации |

Первый slice ограничен двумя briefs. Request runtime раскрывается только в нужной contract boundary; глубокий runtime материал остаётся второму slice/module.

### Outcome-level coverage первого slice

| Artifact | Exact targets | Coverage role |
|---|---|---|
| `b2.index.evolvable-api-contracts` | `b2.capability.design-http-api-contracts`, `b2.capability.evolve-api-contracts`, `b2.capability.design-validation-error-contracts`, `b2.capability.verify-contract-compatibility` | `reference` |
| `b2.learn.http-contract-execution-boundary` | `b2.level-outcome.trace-request-execution-l1-follow-known-path`, `b2.level-outcome.trace-request-execution-l2-diagnose-common-failure`, `b2.level-outcome.design-http-api-contracts-l1-implement-specified-contract`, `b2.level-outcome.design-http-api-contracts-l2-design-typical-resource`, `b2.level-outcome.design-validation-error-contracts-l1-follow-error-convention`, `b2.level-outcome.design-validation-error-contracts-l2-design-client-errors` | `explain` |
| `b2.learn.compatible-api-change` | `b2.level-outcome.evolve-api-contracts-l2-plan-compatible-change`, `b2.level-outcome.evolve-api-contracts-l3-own-service-migration`, `b2.level-outcome.verify-contract-compatibility-l2-detect-breaking-change`, `b2.level-outcome.verify-contract-compatibility-l3-build-consumer-evidence`, `b2.level-outcome.deliver-service-changes-safely-l2-plan-typical-rollout`, `b2.level-outcome.deliver-service-changes-safely-l3-own-risky-migration` | `explain` |
| `b2.interview.api-contract-evolution` | `b2.level-outcome.design-http-api-contracts-l2-design-typical-resource`, `b2.level-outcome.design-http-api-contracts-l3-resolve-ambiguous-requirements`, `b2.level-outcome.design-http-api-contracts-l4-establish-cross-team-conventions`, `b2.level-outcome.evolve-api-contracts-l2-plan-compatible-change`, `b2.level-outcome.evolve-api-contracts-l3-own-service-migration`, `b2.level-outcome.evolve-api-contracts-l4-lead-cross-team-migration`, `b2.level-outcome.verify-contract-compatibility-l2-detect-breaking-change`, `b2.level-outcome.verify-contract-compatibility-l3-build-consumer-evidence`, `b2.level-outcome.verify-contract-compatibility-l4-establish-compatibility-process` | `probe` |
| `b2.kata.compatible-delivery-contract-change` | `b2.level-outcome.design-http-api-contracts-l2-design-typical-resource`, `b2.level-outcome.evolve-api-contracts-l2-plan-compatible-change`, `b2.level-outcome.design-validation-error-contracts-l2-design-client-errors`, `b2.level-outcome.verify-contract-compatibility-l2-detect-breaking-change` | `practice`, `assess` |
| `b2.project-spec.evolvable-orders-api` | `b2.level-outcome.design-http-api-contracts-l3-resolve-ambiguous-requirements`, `b2.level-outcome.evolve-api-contracts-l3-own-service-migration`, `b2.level-outcome.design-validation-error-contracts-l3-unify-service-boundaries`, `b2.level-outcome.verify-contract-compatibility-l3-build-consumer-evidence`, `b2.level-outcome.deliver-service-changes-safely-l3-own-risky-migration` | `integrate`, `assess` |

Interview follow-up может probing-ом выявлять качество L4 reasoning, но без межкомандного execution evidence не доказывает proficiency L4.

## Контрастный slice: artifact set M1.7

| Artifact ID | Kind | Primary coverage |
|---|---|---|
| `b2.index.runtime-concurrency-lifecycle` | index | Module navigation, prerequisites и границы B1/B7/B6 |
| `b2.learn.cancellation-deadlines-resource-lifecycle` | learn | `manage-service-resource-lifecycle`, `control-concurrency-cancellation` |
| `b2.learn.bounded-concurrency-pool-saturation` | learn | `integrate-external-services`, `diagnose-service-performance`, `control-service-load-resources` |
| `b2.interview.runtime-resource-failure` | interview | Runtime/debugging/performance follow-ups |
| `b2.kata.stop-orphan-work-and-pool-exhaustion` | kata | S08 с tests, telemetry и recovery evidence |
| `b2.project-spec.resilient-fanout-service` | project-spec | Интеграция lifecycle/deadline/load решения в самостоятельном проекте |

### Outcome-level coverage контрастного slice

| Artifact | Exact targets | Coverage role |
|---|---|---|
| `b2.index.runtime-concurrency-lifecycle` | `b2.capability.manage-service-resource-lifecycle`, `b2.capability.integrate-external-services`, `b2.capability.control-concurrency-cancellation`, `b2.capability.diagnose-service-performance`, `b2.capability.control-service-load-resources` | `reference` |
| `b2.learn.cancellation-deadlines-resource-lifecycle` | `b2.level-outcome.manage-service-resource-lifecycle-l1-use-defined-scope`, `b2.level-outcome.manage-service-resource-lifecycle-l2-design-local-lifecycle`, `b2.level-outcome.manage-service-resource-lifecycle-l3-remediate-leak`, `b2.level-outcome.control-concurrency-cancellation-l1-preserve-cleanup`, `b2.level-outcome.control-concurrency-cancellation-l2-bound-local-work`, `b2.level-outcome.control-concurrency-cancellation-l3-remediate-runtime-failure` | `explain` |
| `b2.learn.bounded-concurrency-pool-saturation` | `b2.level-outcome.integrate-external-services-l1-use-defined-client`, `b2.level-outcome.integrate-external-services-l2-design-typical-client-boundary`, `b2.level-outcome.integrate-external-services-l3-own-degraded-dependency`, `b2.level-outcome.diagnose-service-performance-l2-localize-common-bottleneck`, `b2.level-outcome.diagnose-service-performance-l3-investigate-production-degradation`, `b2.level-outcome.control-service-load-resources-l2-configure-local-bounds`, `b2.level-outcome.control-service-load-resources-l3-design-graceful-overload` | `explain` |
| `b2.interview.runtime-resource-failure` | `b2.level-outcome.manage-service-resource-lifecycle-l2-design-local-lifecycle`, `b2.level-outcome.manage-service-resource-lifecycle-l3-remediate-leak`, `b2.level-outcome.manage-service-resource-lifecycle-l4-establish-service-policy`, `b2.level-outcome.integrate-external-services-l2-design-typical-client-boundary`, `b2.level-outcome.integrate-external-services-l3-own-degraded-dependency`, `b2.level-outcome.control-concurrency-cancellation-l2-bound-local-work`, `b2.level-outcome.control-concurrency-cancellation-l3-remediate-runtime-failure`, `b2.level-outcome.control-concurrency-cancellation-l4-establish-runtime-policy`, `b2.level-outcome.diagnose-service-performance-l2-localize-common-bottleneck`, `b2.level-outcome.diagnose-service-performance-l3-investigate-production-degradation`, `b2.level-outcome.diagnose-service-performance-l4-lead-cross-service-analysis`, `b2.level-outcome.control-service-load-resources-l2-configure-local-bounds`, `b2.level-outcome.control-service-load-resources-l3-design-graceful-overload`, `b2.level-outcome.control-service-load-resources-l4-align-capacity-boundaries`, `b2.level-outcome.trace-request-execution-l3-explain-production-path`, `b2.level-outcome.verify-service-behavior-l2-select-test-boundaries`, `b2.level-outcome.verify-service-behavior-l3-design-service-strategy` | `probe` |
| `b2.kata.stop-orphan-work-and-pool-exhaustion` | `b2.level-outcome.manage-service-resource-lifecycle-l2-design-local-lifecycle`, `b2.level-outcome.integrate-external-services-l2-design-typical-client-boundary`, `b2.level-outcome.control-concurrency-cancellation-l2-bound-local-work`, `b2.level-outcome.diagnose-service-performance-l2-localize-common-bottleneck`, `b2.level-outcome.control-service-load-resources-l2-configure-local-bounds`, `b2.level-outcome.verify-service-behavior-l2-select-test-boundaries` | `practice`, `assess` |
| `b2.project-spec.resilient-fanout-service` | `b2.level-outcome.manage-service-resource-lifecycle-l3-remediate-leak`, `b2.level-outcome.integrate-external-services-l3-own-degraded-dependency`, `b2.level-outcome.control-concurrency-cancellation-l3-remediate-runtime-failure`, `b2.level-outcome.diagnose-service-performance-l3-investigate-production-degradation`, `b2.level-outcome.control-service-load-resources-l3-design-graceful-overload`, `b2.level-outcome.trace-request-execution-l3-explain-production-path`, `b2.level-outcome.verify-service-behavior-l3-design-service-strategy` | `integrate`, `assess` |

Как и в первом slice, interview получает роль `probe`: он выявляет reasoning, а L4 требует отдельного multi-team adoption/execution evidence.

## Service Architecture slice: artifact set M1.8.1

| Artifact ID | Kind | Primary coverage |
|---|---|---|
| `b2.index.service-architecture-boundaries` | index | Навигация по capability, prerequisites и границам S06 |
| `b2.learn.change-isolation-service-boundaries` | learn | Architecture L1–L3 и verification L1–L2 |
| `b2.interview.service-boundary-change` | interview | Диагностика, boundary choice, migration и evidence probes L1–L3 |
| `b2.kata.extract-order-cancellation-policy` | kata | Практика типовой feature и проверяемая заменяемость adapter |
| `b2.project-spec.order-cancellation-policy-service` | project-spec | Интеграция реальных adapters, decision record и повторное policy change |

### Outcome-level coverage M1.8.1

| Artifact | Exact targets | Coverage role |
|---|---|---|
| `b2.index.service-architecture-boundaries` | `b2.capability.design-service-architecture`, `b2.capability.verify-service-behavior` | `reference` |
| `b2.learn.change-isolation-service-boundaries` | `b2.level-outcome.design-service-architecture-l1-follow-existing-boundaries`, `b2.level-outcome.design-service-architecture-l2-structure-typical-feature`, `b2.level-outcome.design-service-architecture-l3-reshape-changing-service`, `b2.level-outcome.verify-service-behavior-l1-test-local-behavior`, `b2.level-outcome.verify-service-behavior-l2-select-test-boundaries` | `explain` |
| `b2.interview.service-boundary-change` | `b2.level-outcome.design-service-architecture-l1-follow-existing-boundaries`, `b2.level-outcome.design-service-architecture-l2-structure-typical-feature`, `b2.level-outcome.design-service-architecture-l3-reshape-changing-service`, `b2.level-outcome.verify-service-behavior-l1-test-local-behavior`, `b2.level-outcome.verify-service-behavior-l2-select-test-boundaries` | `probe` |
| `b2.kata.extract-order-cancellation-policy` | `b2.level-outcome.design-service-architecture-l1-follow-existing-boundaries`, `b2.level-outcome.design-service-architecture-l2-structure-typical-feature`, `b2.level-outcome.verify-service-behavior-l1-test-local-behavior`, `b2.level-outcome.verify-service-behavior-l2-select-test-boundaries` | `practice`, `assess` |
| `b2.project-spec.order-cancellation-policy-service` | `b2.level-outcome.design-service-architecture-l2-structure-typical-feature`, `b2.level-outcome.design-service-architecture-l3-reshape-changing-service`, `b2.level-outcome.verify-service-behavior-l2-select-test-boundaries` | `integrate`, `assess` |

`integrate-external-services` не получает новой relationship: M1.8.1 ссылается на принятые R2/R4 и использует Carrier только как заменяемый adapter. Verification L3 и architecture L4 также не заявлены без соответствующего service-wide или multi-team evidence.

## Service Verification slice: artifact set M1.8.3

| Artifact ID | Kind | Primary coverage |
|---|---|---|
| `b2.index.risk-based-service-verification` | index | Навигация по Verification и Compatibility capabilities |
| `b2.learn.truthful-test-boundaries` | learn | Verification L1–L3 и Compatibility L1–L2 |
| `b2.interview.green-tests-broken-contract` | interview | Risk/mechanism/boundary probes Verification и Compatibility L1–L3 |
| `b2.kata.detect-orders-error-contract-regression` | kata | Обнаружение и локализация одного S10 handler defect |
| `b2.project-spec.orders-verification-portfolio` | project-spec | Service-level portfolio и evidence двух consumers |

### Outcome-level coverage M1.8.3

| Artifact | Exact targets | Coverage role |
|---|---|---|
| `b2.index.risk-based-service-verification` | `b2.capability.verify-service-behavior`, `b2.capability.verify-contract-compatibility` | `reference` |
| `b2.learn.truthful-test-boundaries` | `b2.level-outcome.verify-service-behavior-l1-test-local-behavior`, `b2.level-outcome.verify-service-behavior-l2-select-test-boundaries`, `b2.level-outcome.verify-service-behavior-l3-design-service-strategy`, `b2.level-outcome.verify-contract-compatibility-l1-maintain-contract-check`, `b2.level-outcome.verify-contract-compatibility-l2-detect-breaking-change` | `explain` |
| `b2.interview.green-tests-broken-contract` | `b2.level-outcome.verify-service-behavior-l1-test-local-behavior`, `b2.level-outcome.verify-service-behavior-l2-select-test-boundaries`, `b2.level-outcome.verify-service-behavior-l3-design-service-strategy`, `b2.level-outcome.verify-contract-compatibility-l1-maintain-contract-check`, `b2.level-outcome.verify-contract-compatibility-l2-detect-breaking-change`, `b2.level-outcome.verify-contract-compatibility-l3-build-consumer-evidence` | `probe` |
| `b2.kata.detect-orders-error-contract-regression` | `b2.level-outcome.verify-service-behavior-l1-test-local-behavior`, `b2.level-outcome.verify-service-behavior-l2-select-test-boundaries`, `b2.level-outcome.verify-contract-compatibility-l1-maintain-contract-check`, `b2.level-outcome.verify-contract-compatibility-l2-detect-breaking-change` | `practice`, `assess` |
| `b2.project-spec.orders-verification-portfolio` | `b2.level-outcome.verify-service-behavior-l3-design-service-strategy`, `b2.level-outcome.verify-contract-compatibility-l3-build-consumer-evidence` | `integrate`, `assess` |

Compatibility L1 получает первую relationship в M1.8.3. Verification L1–L3 и Compatibility L2/L3 уже имели accepted relationships из других modules; этот slice создаёт для них собственный Service Verification flow. L4 relationships не заявлены.

## ImplementationReference

`implementation-reference` появляется только после самостоятельной реализации project spec. M1.8.1 и M1.8.3 проверяют metadata/registration contract, но не создают фиктивную ссылку или эталонный код.

## Transactional Persistence slice: artifact set M1.8.5

| Artifact ID | Kind | Primary coverage |
|---|---|---|
| `b2.index.transactional-orders-operation` | index | Навигация по Transaction Boundaries и Idempotent Operations capabilities |
| `b2.learn.transaction-boundary-failure-windows` | learn | Transaction L1–L3 и Idempotency L2–L3 |
| `b2.interview.commit-succeeded-event-unknown` | interview | Failure-window, recovery и idempotency probes L1–L3 |
| `b2.kata.recover-order-confirmation` | kata | Практика Transaction L1/L2 и Idempotency L2 на одном crash window |
| `b2.project-spec.resilient-order-confirmation` | project-spec | Раздельное evidence Transaction L3 и Idempotency L3 |

### Outcome-level coverage M1.8.5

| Artifact | Exact targets | Coverage role |
|---|---|---|
| `b2.index.transactional-orders-operation` | `b2.capability.manage-application-transaction-boundaries`, `b2.capability.design-idempotent-service-operations` | `reference` |
| `b2.learn.transaction-boundary-failure-windows` | `b2.level-outcome.manage-application-transaction-boundaries-l1-use-defined-unit`, `b2.level-outcome.manage-application-transaction-boundaries-l2-design-operation-boundary`, `b2.level-outcome.manage-application-transaction-boundaries-l3-resolve-side-effect-consistency`, `b2.level-outcome.design-idempotent-service-operations-l2-implement-known-pattern`, `b2.level-outcome.design-idempotent-service-operations-l3-design-failure-safe-operation` | `explain` |
| `b2.interview.commit-succeeded-event-unknown` | `b2.level-outcome.manage-application-transaction-boundaries-l1-use-defined-unit`, `b2.level-outcome.manage-application-transaction-boundaries-l2-design-operation-boundary`, `b2.level-outcome.manage-application-transaction-boundaries-l3-resolve-side-effect-consistency`, `b2.level-outcome.design-idempotent-service-operations-l2-implement-known-pattern`, `b2.level-outcome.design-idempotent-service-operations-l3-design-failure-safe-operation` | `probe` |
| `b2.kata.recover-order-confirmation` | `b2.level-outcome.manage-application-transaction-boundaries-l1-use-defined-unit`, `b2.level-outcome.manage-application-transaction-boundaries-l2-design-operation-boundary`, `b2.level-outcome.design-idempotent-service-operations-l2-implement-known-pattern` | `practice`, `assess` |
| `b2.project-spec.resilient-order-confirmation` | `b2.level-outcome.manage-application-transaction-boundaries-l3-resolve-side-effect-consistency`, `b2.level-outcome.design-idempotent-service-operations-l3-design-failure-safe-operation` | `integrate`, `assess` |

M1.8.5 использует Verification L2/L3 как принятый способ строить evidence, но не добавляет к ним relationship: центральное наблюдаемое действие остаётся transaction/recovery и idempotency одной Orders operation. Cache outcomes, Idempotency L4 и B3/B5 outcomes не заявлены.

## Background & Message-driven Workflows slice: artifact set M1.8.7

| Artifact ID | Kind | Primary coverage |
|---|---|---|
| `b2.index.recoverable-order-confirmed-consumer` | index | Навигация по Asynchronous Workflows capability и S09 |
| `b2.learn.acknowledgement-redelivery-recovery-boundary` | learn | Workflow L2/L3 |
| `b2.interview.side-effect-committed-message-unacked` | interview | Ack/retry/recovery probes Workflow L2/L3 |
| `b2.kata.recover-order-confirmed-consumer` | kata | Практика Workflow L2 на одном crash window |
| `b2.project-spec.resilient-fulfillment-consumer` | project-spec | Интеграция и раздельное evidence Workflow L2/L3 |

### Outcome-level coverage M1.8.7

| Artifact | Exact targets | Coverage role |
|---|---|---|
| `b2.index.recoverable-order-confirmed-consumer` | `b2.capability.design-asynchronous-workflows` | `reference` |
| `b2.learn.acknowledgement-redelivery-recovery-boundary` | `b2.level-outcome.design-asynchronous-workflows-l2-implement-background-flow`, `b2.level-outcome.design-asynchronous-workflows-l3-design-recoverable-workflow` | `explain` |
| `b2.interview.side-effect-committed-message-unacked` | `b2.level-outcome.design-asynchronous-workflows-l2-implement-background-flow`, `b2.level-outcome.design-asynchronous-workflows-l3-design-recoverable-workflow` | `probe` |
| `b2.kata.recover-order-confirmed-consumer` | `b2.level-outcome.design-asynchronous-workflows-l2-implement-background-flow` | `practice`, `assess` |
| `b2.project-spec.resilient-fulfillment-consumer` | `b2.level-outcome.design-asynchronous-workflows-l2-implement-background-flow`, `b2.level-outcome.design-asynchronous-workflows-l3-design-recoverable-workflow` | `integrate`, `assess` |

M1.8.7 переиспользует принятые S07 event identity/idempotency, R1 cancellation context и V1 verification method без новых Idempotency, Cancellation или Verification relationships. Workflow L4 и B5 outcome IDs не заявляются; RabbitMQ semantics остаётся readiness/context.

## Identity-aware Boundaries slice: artifact set M1.8.9

| Artifact ID | Kind | Primary coverage |
|---|---|---|
| `b2.index.tenant-scoped-orders-authorization` | index | Навигация по Identity and Access Control capability и S05 |
| `b2.learn.trusted-context-object-authorization-boundary` | learn | Identity L1–L3: rule, trusted context и enforcement placement |
| `b2.interview.valid-token-cross-tenant-order` | interview | Probes от заданного object rule до threat/bypass reasoning L1–L3 |
| `b2.kata.block-cross-tenant-order-read` | kata | Практика Identity L1/L2 на одном cross-tenant bypass |
| `b2.project-spec.tenant-safe-orders-read-api` | project-spec | Интеграция и раздельное evidence Identity L2/L3 по нескольким paths |

### Outcome-level coverage M1.8.9

| Artifact | Exact targets | Coverage role |
|---|---|---|
| `b2.index.tenant-scoped-orders-authorization` | `b2.capability.integrate-identity-access-control` | `reference` |
| `b2.learn.trusted-context-object-authorization-boundary` | `b2.level-outcome.integrate-identity-access-control-l1-enforce-defined-rule`, `b2.level-outcome.integrate-identity-access-control-l2-propagate-context`, `b2.level-outcome.integrate-identity-access-control-l3-design-service-enforcement` | `explain` |
| `b2.interview.valid-token-cross-tenant-order` | `b2.level-outcome.integrate-identity-access-control-l1-enforce-defined-rule`, `b2.level-outcome.integrate-identity-access-control-l2-propagate-context`, `b2.level-outcome.integrate-identity-access-control-l3-design-service-enforcement` | `probe` |
| `b2.kata.block-cross-tenant-order-read` | `b2.level-outcome.integrate-identity-access-control-l1-enforce-defined-rule`, `b2.level-outcome.integrate-identity-access-control-l2-propagate-context` | `practice`, `assess` |
| `b2.project-spec.tenant-safe-orders-read-api` | `b2.level-outcome.integrate-identity-access-control-l2-propagate-context`, `b2.level-outcome.integrate-identity-access-control-l3-design-service-enforcement` | `integrate`, `assess` |

M1.8.9 добавляет 15 relationships: одну capability-level `reference` и 14 outcome-level relationships к Identity L1–L3. Identity L4, Abuse Controls, A3, HTTP, Architecture и Verification relationships не заявляются. Принятые C1/A1/V1 используются только как linked context; Gate 0 подтверждает technical readiness, но не proficiency A3.

## Identity-aware Boundaries operation-cost slice: artifact set M1.8.11

| Artifact ID | Kind | Primary coverage |
|---|---|---|
| `b2.index.cost-bounded-orders-export` | index | Навигация по API Security and Abuse Controls capability и operation-cost половине S14 |
| `b2.learn.server-owned-cost-admission-boundary` | learn | Abuse L1–L3: заданные limits, applicability matrix и adversarial boundary |
| `b2.interview.valid-tenant-expensive-export` | interview | Probes от одного cost bypass до L3 threat/cost reasoning |
| `b2.kata.block-bulk-export-cost-bypass` | kata | Практика и assessment Abuse L1 на одном row-only bypass |
| `b2.project-spec.cost-bounded-orders-export-api` | project-spec | Интеграция и раздельное evidence Abuse L2/L3 |

### Outcome-level coverage M1.8.11

| Artifact | Exact targets | Coverage role |
|---|---|---|
| `b2.index.cost-bounded-orders-export` | `b2.capability.enforce-api-security-abuse-controls` | `reference` |
| `b2.learn.server-owned-cost-admission-boundary` | `b2.level-outcome.enforce-api-security-abuse-controls-l1-apply-defined-controls`, `b2.level-outcome.enforce-api-security-abuse-controls-l2-protect-typical-endpoint`, `b2.level-outcome.enforce-api-security-abuse-controls-l3-design-service-abuse-boundary` | `explain` |
| `b2.interview.valid-tenant-expensive-export` | `b2.level-outcome.enforce-api-security-abuse-controls-l1-apply-defined-controls`, `b2.level-outcome.enforce-api-security-abuse-controls-l2-protect-typical-endpoint`, `b2.level-outcome.enforce-api-security-abuse-controls-l3-design-service-abuse-boundary` | `probe` |
| `b2.kata.block-bulk-export-cost-bypass` | `b2.level-outcome.enforce-api-security-abuse-controls-l1-apply-defined-controls` | `practice`, `assess` |
| `b2.project-spec.cost-bounded-orders-export-api` | `b2.level-outcome.enforce-api-security-abuse-controls-l2-protect-typical-endpoint`, `b2.level-outcome.enforce-api-security-abuse-controls-l3-design-service-abuse-boundary` | `integrate`, `assess` |

M1.8.11 заявляет 13 relationships: одну capability-level и 12 outcome-level relationships к Abuse L1–L3. Abuse L4, Identity, Load Control, HTTP, Verification, A3, B3, B5 и B7 relationships не добавляются. Quota/rate и untrusted-target строки получили честную `not applicable` диспозицию с residual risks; callback/SSRF остаётся отдельным долгом.

## Application Caching slice: artifact set M1.8.13 (`accepted`)

| Artifact ID | Kind | Primary coverage |
|---|---|---|
| `b2.index.tenant-scoped-orders-cache` | index | Навигация по Application Caching capability, Gate 0 и S15 |
| `b2.learn.cache-aside-freshness-coalescing` | learn | Cache L2/L3: tenant-safe cache-aside, freshness, coalescing и failure boundary |
| `b2.interview.concurrent-miss-stale-order-summary` | interview | Probes от заданного L2 pattern к L3 race/failure/measurement design |
| `b2.kata.stop-orders-cache-stampede` | kata | Практика и assessment Cache L2 на одном concurrent-miss defect |
| `b2.project-spec.resilient-orders-summary-cache` | project-spec | Интеграция и раздельное evidence Cache L2/L3 |

### Outcome-level coverage M1.8.13

| Artifact | Exact targets | Coverage role |
|---|---|---|
| `b2.index.tenant-scoped-orders-cache` | `b2.capability.integrate-application-caching` | `reference` |
| `b2.learn.cache-aside-freshness-coalescing` | `b2.level-outcome.integrate-application-caching-l2-apply-known-cache-pattern`, `b2.level-outcome.integrate-application-caching-l3-design-consistency-failure-behavior` | `explain` |
| `b2.interview.concurrent-miss-stale-order-summary` | `b2.level-outcome.integrate-application-caching-l2-apply-known-cache-pattern`, `b2.level-outcome.integrate-application-caching-l3-design-consistency-failure-behavior` | `probe` |
| `b2.kata.stop-orders-cache-stampede` | `b2.level-outcome.integrate-application-caching-l2-apply-known-cache-pattern` | `practice`, `assess` |
| `b2.project-spec.resilient-orders-summary-cache` | `b2.level-outcome.integrate-application-caching-l2-apply-known-cache-pattern`, `b2.level-outcome.integrate-application-caching-l3-design-consistency-failure-behavior` | `integrate`, `assess` |

M1.8.13 заявляет 11 relationships: одну capability-level `reference` и 10 outcome-level relationships к Cache L2/L3. Transaction, Load Control, Identity, Verification, B3 и B5 используются только как связанный контекст/readiness и не получают coverage. Cache L4 не заявляется; one-process coalescing не выдаётся за cross-worker или distributed guarantee.

## Safe Service Evolution slice: artifact set M1.8.15 (`accepted`)

[Safe Orders service rollout](slices/safe-orders-service-rollout/README.md) использует неизменный контракт S03 и проверки S10 для другого инженерного действия: измерить поэтапный выпуск, запретить продвижение и восстановить обслуживание с сохранением принятых обязательств. Gate 0 подтверждён на disposable-стенде, который удалён; G14 принят после закрытия C-1–C-9.

| Artifact ID | Kind | Primary coverage |
|---|---|---|
| `b2.index.safe-orders-service-rollout` | index | Навигация по Delivery, S11 и лабораторной модели |
| `b2.learn.staged-rollout-stop-recovery` | learn | Delivery L1–L3: стадии, условия, остановка, обратимость |
| `b2.interview.limited-reversibility-orders-change` | interview | Рассуждение от заданного checklist до сохранения обязательств |
| `b2.kata.stop-unsafe-orders-rollout` | kata | Выполнение checklist и остановка на одном нарушенном условии L1 |
| `b2.project-spec.evidence-driven-orders-rollout` | project-spec | Самостоятельный план L2 и ограниченно обратимый rollout L3 |

### Outcome-level coverage M1.8.15

| Artifact | Exact targets | Coverage role |
|---|---|---|
| `b2.index.safe-orders-service-rollout` | `b2.capability.deliver-service-changes-safely` | `reference` |
| `b2.learn.staged-rollout-stop-recovery` | `b2.level-outcome.deliver-service-changes-safely-l1-follow-rollout-checklist`, `b2.level-outcome.deliver-service-changes-safely-l2-plan-typical-rollout`, `b2.level-outcome.deliver-service-changes-safely-l3-own-risky-migration` | `explain` |
| `b2.interview.limited-reversibility-orders-change` | `b2.level-outcome.deliver-service-changes-safely-l1-follow-rollout-checklist`, `b2.level-outcome.deliver-service-changes-safely-l2-plan-typical-rollout`, `b2.level-outcome.deliver-service-changes-safely-l3-own-risky-migration` | `probe` |
| `b2.kata.stop-unsafe-orders-rollout` | `b2.level-outcome.deliver-service-changes-safely-l1-follow-rollout-checklist` | `practice`, `assess` |
| `b2.project-spec.evidence-driven-orders-rollout` | `b2.level-outcome.deliver-service-changes-safely-l2-plan-typical-rollout`, `b2.level-outcome.deliver-service-changes-safely-l3-own-risky-migration` | `integrate`, `assess` |

Фактический YAML пяти материалов содержит 13 relationships: одну capability-level `reference` и 12 outcome-level. Все пять материалов имеют `status: accepted` и входят в accepted totals после G14; эти relationships не доказывают proficiency участника. Delivery L1 — новое уникальное покрытие относительно принятого набора; L2/L3 уже имели supporting relationships C2/C5. Собственное evidence S11 различает исполнение заданного checklist L1, самостоятельное планирование и возврат до scheduled L2, подготовку incident path и восстановление после принятых scheduled-заказов L3. Evolution, Compatibility, Verification, B6/B7 и Delivery L4 relationships отсутствуют; S03/S10 используются только как связанный контекст.

## External Integration slice: artifact set M1.8.17 (`accepted`)

[Правдивая граница клиента Pricing](slices/truthful-pricing-client-boundary/README.md) использует Quote/Pricing контекст S08 для одного outbound response action: сохранить valid empty и отличить его от технической невозможности получить/разобрать ответ. Gate 0 подтверждён локальным HTTP-опытом до authoring. Канонический fan-out/slow-dependency S08 не объявляется завершённым; runtime R2–R5 и verification S10 остаются контекстом.

| Artifact ID | Kind | Фактический материал / действие |
|---|---|---|
| `b2.index.truthful-pricing-client-boundary` | index | [Маршрут](slices/truthful-pricing-client-boundary/README.md), prerequisites и границы |
| `b2.learn.response-to-domain-outcome` | learn | [Причинная модель](slices/truthful-pricing-client-boundary/learn/response-to-domain-outcome.md): HTTP response → предметный результат |
| `b2.interview.pricing-client-decisions` | interview | [Рассуждение L1/L2](slices/truthful-pricing-client-boundary/interview/pricing-client-decisions.md), без заявления proficiency |
| `b2.kata.stop-failure-to-empty-collapse` | kata | [Применение заданного договора L1](slices/truthful-pricing-client-boundary/kata/stop-failure-to-empty-collapse.md), один defect |
| `b2.project-spec.integrate-one-pricing-operation` | project-spec | [Самостоятельная интеграция L2](slices/truthful-pricing-client-boundary/project-spec/integrate-one-pricing-operation.md), выбор внутренних типов и evidence |

### Exact relationships M1.8.17

| Artifact | Exact target | Role |
|---|---|---|
| `b2.index.truthful-pricing-client-boundary` | `b2.capability.integrate-external-services` | `reference` |
| `b2.learn.response-to-domain-outcome` | `b2.level-outcome.integrate-external-services-l1-use-defined-client` | `explain` |
| `b2.learn.response-to-domain-outcome` | `b2.level-outcome.integrate-external-services-l2-design-typical-client-boundary` | `explain` |
| `b2.interview.pricing-client-decisions` | `b2.level-outcome.integrate-external-services-l1-use-defined-client` | `probe` |
| `b2.interview.pricing-client-decisions` | `b2.level-outcome.integrate-external-services-l2-design-typical-client-boundary` | `probe` |
| `b2.kata.stop-failure-to-empty-collapse` | `b2.level-outcome.integrate-external-services-l1-use-defined-client` | `practice` |
| `b2.kata.stop-failure-to-empty-collapse` | `b2.level-outcome.integrate-external-services-l1-use-defined-client` | `assess` |
| `b2.project-spec.integrate-one-pricing-operation` | `b2.level-outcome.integrate-external-services-l2-design-typical-client-boundary` | `integrate` |
| `b2.project-spec.integrate-one-pricing-operation` | `b2.level-outcome.integrate-external-services-l2-design-typical-client-boundary` | `assess` |

Фактический YAML пяти accepted-материалов содержит 9 relationships к трём targets: одну capability reference и восемь outcome-level связей к External L1/L2. Они входят в accepted totals после G16; новых уникальных outcomes относительно предыдущего принятого набора — 0. Kata требует исполнить известные исходы, project — самостоятельно выбрать внутреннее представление и интегрировать настоящий HTTP-client path. Материалы задают проверку деятельности, но не доказывают, что участник уже выполнил её.

External L3/L4, Cancellation, Load Control, Verification и A3/B5 relationships отсутствуют. Trusted target, read-only semantics, отсутствие retries и resource cleanup — readiness/context этого integration action. G16 принят; module-gate decision отдельно не принимался.

## HTTP Runtime/S01: artifact set M1.8.20 (`accepted`)

[Локализация потери request context](slices/request-context-loss-diagnosis/README.md) добавляет четыре собственных жанра HTTP Runtime. Learn-переходы переиспользуют C1/R1 без новых relationships этих материалов. Gate 0 независимо воспроизведён профилем A; G19 принят как явное однопрофильное исключение, module gate не принят.

| Artifact ID | Kind | Фактический материал / действие |
|---|---|---|
| `b2.index.request-context-loss-diagnosis` | index | [Маршрут](slices/request-context-loss-diagnosis/README.md): рабочая ситуация, prerequisites и reuse |
| `b2.interview.reconstruct-context-path` | interview | [Восстановление пути](slices/request-context-loss-diagnosis/interview/reconstruct-context-path.md): L1/L2 и production follow-up L3 |
| `b2.kata.localize-context-loss` | kata | [Первая потеря](slices/request-context-loss-diagnosis/kata/localize-context-loss.md): заданный путь L1, локализация и регрессия L2 |
| `b2.project-spec.preserve-context-through-refactor` | project-spec | [Собственный refactor](slices/request-context-loss-diagnosis/project-spec/preserve-context-through-refactor.md): выбор concern/границы и доказательства L2 |

### Exact relationships M1.8.20

| Artifact | Exact target | Role |
|---|---|---|
| `b2.index.request-context-loss-diagnosis` | `b2.capability.trace-request-execution` | `reference` |
| `b2.interview.reconstruct-context-path` | `b2.level-outcome.trace-request-execution-l1-follow-known-path` | `probe` |
| `b2.interview.reconstruct-context-path` | `b2.level-outcome.trace-request-execution-l2-diagnose-common-failure` | `probe` |
| `b2.interview.reconstruct-context-path` | `b2.level-outcome.trace-request-execution-l3-explain-production-path` | `probe` |
| `b2.kata.localize-context-loss` | `b2.level-outcome.trace-request-execution-l1-follow-known-path` | `practice` |
| `b2.kata.localize-context-loss` | `b2.level-outcome.trace-request-execution-l1-follow-known-path` | `assess` |
| `b2.kata.localize-context-loss` | `b2.level-outcome.trace-request-execution-l2-diagnose-common-failure` | `practice` |
| `b2.kata.localize-context-loss` | `b2.level-outcome.trace-request-execution-l2-diagnose-common-failure` | `assess` |
| `b2.project-spec.preserve-context-through-refactor` | `b2.level-outcome.trace-request-execution-l2-diagnose-common-failure` | `integrate` |
| `b2.project-spec.preserve-context-through-refactor` | `b2.level-outcome.trace-request-execution-l2-diagnose-common-failure` | `assess` |

Фактический YAML четырёх accepted-материалов содержит 10 relationships к четырём targets: 1 reference + 3 probe + 2 practice + 3 assess + 1 integrate. Они входят в accepted totals после G19. L3 ограничен interview probe; лаборатория не доказывает production reconstruction или proficiency участника. Lifecycle, Cancellation, Verification, HTTP Contract, B1/A3/B7 — контекст/readiness, coverage по ним не добавлено. G19 закрывает content-action D19/D20, но не заменяет исполнение проекта участником и отдельное решение module gate.
