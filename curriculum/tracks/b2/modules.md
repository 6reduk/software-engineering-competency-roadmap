---
artifact: b2-module-blueprint
status: accepted
updated: 2026-09-20
language: ru
---

# Modules B2

Modules — 10 стабильных единиц навигации и выпуска, не синонимы clusters. Общие metadata/defaults определены в `README.md` blueprint.

<a id="http-service-runtime"></a>

## `b2.module.http-service-runtime` — HTTP service runtime

- Scope: путь запроса через ASGI application, middleware/dependencies, request context, lifespan и resource scopes.
- Develops: `b2.capability.trace-request-execution`, `b2.capability.manage-service-resource-lifecycle`, `b2.capability.control-concurrency-cancellation`.
- Non-goals: устройство Python runtime (B1), сеть ниже прикладного HTTP baseline (A3), общая observability discipline (B7).

<a id="evolvable-api-contracts"></a>

## `b2.module.evolvable-api-contracts` — Evolvable API contracts

- Scope: HTTP/resource semantics, schemas, validation/error contracts, compatibility, idempotency, versioning и deprecation.
- Develops: `b2.capability.design-http-api-contracts`, `b2.capability.evolve-api-contracts`, `b2.capability.design-validation-error-contracts`, `b2.capability.design-idempotent-service-operations`, `b2.capability.verify-contract-compatibility`.
- Non-goals: полный справочник HTTP/FastAPI/Pydantic, distributed consistency theory (B5), delivery platform (B6).

<a id="identity-aware-boundaries"></a>

## `b2.module.identity-aware-boundaries` — Identity and API security boundaries

- Scope: интеграция authentication/authorization, subject/resource/tenant context, API abuse controls, untrusted input/target boundaries и безопасные error boundaries.
- Develops: `b2.capability.integrate-identity-access-control`, `b2.capability.enforce-api-security-abuse-controls`, `b2.capability.design-http-api-contracts`, `b2.capability.design-service-architecture`.
- Non-goals: криптографические протоколы и IAM infrastructure (A3/B6), организация security program (C1).

<a id="service-architecture"></a>

## `b2.module.service-architecture` — Service architecture

- Scope: application/domain/adapters boundaries, dependency direction, modularity, change isolation и service-level decision records.
- Develops: `b2.capability.design-service-architecture`, `b2.capability.integrate-external-services`, `b2.capability.verify-service-behavior`.
- Non-goals: универсальный каталог design patterns, межсервисная декомпозиция всей системы (B5/C1).

<a id="transactional-persistence-integration"></a>

## `b2.module.transactional-persistence-integration` — Transactional persistence integration

- Scope: application transaction boundary, unit of work, repository/driver lifecycle, retry boundary и согласование side effects.
- Develops: `b2.capability.manage-application-transaction-boundaries`, `b2.capability.integrate-application-caching`, `b2.capability.design-idempotent-service-operations`, `b2.capability.verify-service-behavior`.
- Non-goals: SQL, MVCC, query optimization и store selection как таковые (B3).

<a id="external-service-integration"></a>

## `b2.module.external-service-integration` — External service integration

- Scope: outbound calls, client/pool lifecycle, deadlines/cancellation, failure mapping, retry и graceful degradation на service boundary.
- Develops: `b2.capability.integrate-external-services`, `b2.capability.control-concurrency-cancellation`, `b2.capability.control-service-load-resources`.
- Non-goals: Python async semantics (B1), general resilience discipline (B7), service mesh/platform mechanics (B6).

<a id="background-message-workflows"></a>

## `b2.module.background-message-workflows` — Background and message workflows

- Scope: background jobs, messaging adapters, acknowledgement/retry/deduplication boundaries, replay/recovery и graceful worker shutdown.
- Develops: `b2.capability.design-asynchronous-workflows`, `b2.capability.design-idempotent-service-operations`, `b2.capability.control-concurrency-cancellation`.
- Non-goals: broker internals и общая delivery/consistency theory (B5), orchestration infrastructure (B6).

<a id="service-verification"></a>

## `b2.module.service-verification` — Service verification

- Scope: unit/integration/contract/E2E strategy, consumer compatibility и risk-based service evidence.
- Develops: `b2.capability.verify-service-behavior`, `b2.capability.verify-contract-compatibility`, `b2.capability.design-service-architecture`.
- Non-goals: общая test engineering discipline (A2), organization-wide quality governance (C1).

<a id="safe-service-evolution"></a>

## `b2.module.safe-service-evolution` — Safe service evolution

- Scope: migration sequencing, rollout/deprecation, rollback/roll-forward/compensation и service-specific release evidence.
- Develops: `b2.capability.deliver-service-changes-safely`, `b2.capability.evolve-api-contracts`, `b2.capability.verify-contract-compatibility`.
- Non-goals: CI/CD platform implementation (B6), общая production readiness discipline (B7), organization-wide change governance (C1).

<a id="performance-resource-control"></a>

## `b2.module.performance-resource-control` — Performance and resource control

- Scope: latency/throughput evidence, profiling service path, pools, concurrency limits, queueing boundaries, overload и backpressure на уровне сервиса.
- Develops: `b2.capability.diagnose-service-performance`, `b2.capability.control-service-load-resources`, `b2.capability.manage-service-resource-lifecycle`, `b2.capability.control-concurrency-cancellation`.
- Non-goals: capacity management discipline (B7), autoscaling/platform mechanics (B6), Python micro-optimization (B1).

## Навигационные входы clusters

Таблица задаёт module, с которого обычно начинается навигация по cluster. Это не ownership-инвариант: primary module отдельной capability определяется в `capabilities.md` и может отличаться, если capability лучше раскрывается в другом завершённом учебном пакете.

| Cluster | Entry/default module |
|---|---|
| `b2.cluster.request-runtime` | `b2.module.http-service-runtime` |
| `b2.cluster.api-contracts` | `b2.module.evolvable-api-contracts` |
| `b2.cluster.validation-serialization-errors` | `b2.module.evolvable-api-contracts` |
| `b2.cluster.identity-access-boundaries` | `b2.module.identity-aware-boundaries` |
| `b2.cluster.service-architecture` | `b2.module.service-architecture` |
| `b2.cluster.persistence-transactions` | `b2.module.transactional-persistence-integration` |
| `b2.cluster.async-background-integration` | `b2.module.background-message-workflows` |
| `b2.cluster.testing-contracts` | `b2.module.service-verification` |
| `b2.cluster.performance-resource-control` | `b2.module.performance-resource-control` |
| `b2.cluster.evolution-delivery` | `b2.module.safe-service-evolution` |
