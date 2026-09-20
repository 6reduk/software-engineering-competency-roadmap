---
artifact: b2-role-requirement-blueprint
status: accepted
updated: 2026-08-15
language: ru
---

# Предварительные role requirements B2

После G3 эти списки становятся authoritative B2 detail для первых двух RoleView. Track-level `L4` остаётся навигационным summary и не назначается каждой capability автоматически.

## Backend / Distributed Systems

System-owner baseline L3 по request/runtime, service design, data/external integration, verification и performance; L4 — по ключевым межкомандным миграциям.

### Required outcomes

- `b2.level-outcome.trace-request-execution-l3-explain-production-path`
- `b2.level-outcome.manage-service-resource-lifecycle-l3-remediate-leak`
- `b2.level-outcome.design-http-api-contracts-l3-resolve-ambiguous-requirements`
- `b2.level-outcome.evolve-api-contracts-l4-lead-cross-team-migration`
- `b2.level-outcome.design-validation-error-contracts-l3-unify-service-boundaries`
- `b2.level-outcome.integrate-identity-access-control-l3-design-service-enforcement`
- `b2.level-outcome.enforce-api-security-abuse-controls-l3-design-service-abuse-boundary`
- `b2.level-outcome.design-service-architecture-l3-reshape-changing-service`
- `b2.level-outcome.manage-application-transaction-boundaries-l3-resolve-side-effect-consistency`
- `b2.level-outcome.integrate-application-caching-l3-design-consistency-failure-behavior`
- `b2.level-outcome.design-idempotent-service-operations-l3-design-failure-safe-operation`
- `b2.level-outcome.integrate-external-services-l3-own-degraded-dependency`
- `b2.level-outcome.design-asynchronous-workflows-l3-design-recoverable-workflow`
- `b2.level-outcome.control-concurrency-cancellation-l3-remediate-runtime-failure`
- `b2.level-outcome.verify-service-behavior-l3-design-service-strategy`
- `b2.level-outcome.verify-contract-compatibility-l3-build-consumer-evidence`
- `b2.level-outcome.deliver-service-changes-safely-l4-coordinate-cross-team-change`
- `b2.level-outcome.diagnose-service-performance-l3-investigate-production-degradation`
- `b2.level-outcome.control-service-load-resources-l3-design-graceful-overload`

## Architecture / Technical Leadership — backend specialization

Требование не превращает архитектора в автора каждого endpoint. Общий B2 baseline остаётся L3. Обязательный L4 назначается только интегрирующим механизмам, которые практически неизбежны для backend-oriented Architecture role; остальные L4 outcomes становятся conditional specialization.

### Required outcomes

- `b2.level-outcome.trace-request-execution-l3-explain-production-path`
- `b2.level-outcome.manage-service-resource-lifecycle-l3-remediate-leak`
- `b2.level-outcome.design-http-api-contracts-l4-establish-cross-team-conventions`
- `b2.level-outcome.evolve-api-contracts-l4-lead-cross-team-migration`
- `b2.level-outcome.design-validation-error-contracts-l3-unify-service-boundaries`
- `b2.level-outcome.integrate-identity-access-control-l3-design-service-enforcement`
- `b2.level-outcome.enforce-api-security-abuse-controls-l3-design-service-abuse-boundary`
- `b2.level-outcome.design-service-architecture-l4-establish-reusable-boundaries`
- `b2.level-outcome.manage-application-transaction-boundaries-l3-resolve-side-effect-consistency`
- `b2.level-outcome.integrate-application-caching-l3-design-consistency-failure-behavior`
- `b2.level-outcome.design-idempotent-service-operations-l3-design-failure-safe-operation`
- `b2.level-outcome.integrate-external-services-l3-own-degraded-dependency`
- `b2.level-outcome.design-asynchronous-workflows-l3-design-recoverable-workflow`
- `b2.level-outcome.control-concurrency-cancellation-l3-remediate-runtime-failure`
- `b2.level-outcome.verify-service-behavior-l3-design-service-strategy`
- `b2.level-outcome.verify-contract-compatibility-l4-establish-compatibility-process`
- `b2.level-outcome.deliver-service-changes-safely-l4-coordinate-cross-team-change`
- `b2.level-outcome.diagnose-service-performance-l3-investigate-production-degradation`
- `b2.level-outcome.control-service-load-resources-l3-design-graceful-overload`

### Conditional L4 specializations

| Scope | Conditional outcomes |
|---|---|
| Runtime/platform | `b2.level-outcome.manage-service-resource-lifecycle-l4-establish-service-policy`, `b2.level-outcome.integrate-external-services-l4-align-integration-policy`, `b2.level-outcome.control-concurrency-cancellation-l4-establish-runtime-policy`, `b2.level-outcome.diagnose-service-performance-l4-lead-cross-service-analysis`, `b2.level-outcome.control-service-load-resources-l4-align-capacity-boundaries` |
| API security | `b2.level-outcome.integrate-identity-access-control-l4-align-cross-service-policy`, `b2.level-outcome.enforce-api-security-abuse-controls-l4-establish-cross-service-controls` |
| Data/integration | `b2.level-outcome.integrate-application-caching-l4-coordinate-cache-migration`, `b2.level-outcome.design-idempotent-service-operations-l4-align-operation-contracts`, `b2.level-outcome.design-asynchronous-workflows-l4-coordinate-workflow-migration` |
| Quality enablement | `b2.level-outcome.design-validation-error-contracts-l4-establish-shared-convention`, `b2.level-outcome.verify-service-behavior-l4-align-cross-team-evidence` |

Conditional specialization выбирается по фактической зоне ответственности; она не является скрытым требованием выполнить все L4 outcomes B2.

## Interpretive guardrails

- Required outcome означает требуемое поведение, а не обязательное чтение всех artifacts.
- Required L4 outcome включает способность демонстрировать соответствующее L3-поведение той же capability; отдельная L3-строка может быть опущена только как заведомо избыточная, а не как разрешение пропустить system-owner baseline.
- Один проект может дать evidence нескольким outcomes, но решение о proficiency требует разных наблюдений и объяснения trade-offs.
- C1 остаётся владельцем organizational alignment/leadership; B2 outcome оценивает технический механизм и последствия.
- Списки не используются для автоматического вычисления hiring-grade.
