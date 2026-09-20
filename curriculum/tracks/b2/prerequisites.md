---
artifact: b2-prerequisite-blueprint
status: accepted
updated: 2026-08-15
language: ru
---

# Prerequisites B2

## Правило детализации

Точные `Capability requires Capability` edges задаются только между уже существующими semantic IDs. Для соседних треков пока существуют только track/cluster skeletons, поэтому внешние зависимости временно фиксируются как baseline/conditional specifications. После blueprint соответствующего owner-track они заменяются ссылками на реальные capability IDs, а не выдуманными placeholder IDs.

## Internal hard-prerequisite DAG

| Capability | Requires | Почему hard |
|---|---|---|
| `b2.capability.evolve-api-contracts` | `b2.capability.design-http-api-contracts` | Эволюция требует явной исходной semantics |
| `b2.capability.design-validation-error-contracts` | `b2.capability.design-http-api-contracts` | Validation/error является частью внешнего контракта |
| `b2.capability.integrate-identity-access-control` | `b2.capability.design-http-api-contracts` | Enforcement должен быть привязан к operation/resource boundary |
| `b2.capability.manage-application-transaction-boundaries` | `b2.capability.design-service-architecture` | Application transaction определяется вокруг application operation |
| `b2.capability.design-idempotent-service-operations` | `b2.capability.design-http-api-contracts` | Identity и повторный result являются contract semantics |
| `b2.capability.integrate-external-services` | `b2.capability.manage-service-resource-lifecycle` | Client/pool/deadline имеют lifecycle и cleanup boundary |
| `b2.capability.control-concurrency-cancellation` | `b2.capability.manage-service-resource-lifecycle` | Cancellation должна учитывать lifecycle/cleanup управляемой работы и ресурсов |
| `b2.capability.verify-contract-compatibility` | `b2.capability.design-http-api-contracts` | Совместимость проверяется относительно явного контракта |
| `b2.capability.deliver-service-changes-safely` | `b2.capability.evolve-api-contracts`, `b2.capability.verify-service-behavior`, `b2.capability.verify-contract-compatibility` | Rollout опирается на классификацию изменения и evidence поведения/совместимости |
| `b2.capability.diagnose-service-performance` | `b2.capability.trace-request-execution` | Bottleneck локализуется вдоль известного service path |
| `b2.capability.control-service-load-resources` | `b2.capability.manage-service-resource-lifecycle` | Limits управляют конкретными resource scopes/pools |

Capabilities без internal hard prerequisite:

- `b2.capability.trace-request-execution`;
- `b2.capability.manage-service-resource-lifecycle`;
- `b2.capability.design-http-api-contracts`;
- `b2.capability.design-service-architecture`;
- `b2.capability.enforce-api-security-abuse-controls`;
- `b2.capability.integrate-application-caching`;
- `b2.capability.design-asynchronous-workflows`;
- `b2.capability.verify-service-behavior`.

## Internal related, но не hard

| Capability | Related | Причина отсутствия hard edge |
|---|---|---|
| `b2.capability.manage-service-resource-lifecycle` | `b2.capability.trace-request-execution` | Lifecycle существует также у application/job/worker ресурсов вне HTTP request path |
| `b2.capability.design-idempotent-service-operations` | `b2.capability.manage-application-transaction-boundaries` | Idempotency возможна без relational transaction; механизм зависит от storage/workflow |
| `b2.capability.integrate-application-caching` | `b2.capability.manage-application-transaction-boundaries`, `b2.capability.control-service-load-resources` | Cache может быть read-only/derived; transaction/load mechanisms зависят от выбранной стратегии |
| `b2.capability.design-asynchronous-workflows` | `b2.capability.integrate-external-services`, `b2.capability.design-idempotent-service-operations` | Workflow может быть локальным или осознанно non-replayable; duplicate/recovery semantics выбираются, а не всегда требуют idempotency заранее |
| `b2.capability.control-concurrency-cancellation` | `b2.capability.integrate-external-services` | Cancellation применима также к локальным jobs/task groups без downstream service |
| `b2.capability.control-service-load-resources` | `b2.capability.diagnose-service-performance`, `b2.capability.control-concurrency-cancellation` | Defaults можно задать заранее; диагностика нужна для калибровки, но не для первого применения |
| `b2.capability.enforce-api-security-abuse-controls` | `b2.capability.control-service-load-resources`, `b2.capability.integrate-identity-access-control` | Abuse controls используют identity/load context, но обязаны защищать и public/anonymous boundaries |
| `b2.capability.verify-service-behavior` | все implementation capabilities | Verification применима параллельно, а не является последним линейным шагом |

## External baseline and conditional specifications

| Owner | Тип | Требуемый slice | B2 consumers |
|---|---|---|---|
| B1 Python Engineering | hard baseline | Functions/errors/resource protocols, typing/interfaces | Все Python implementation outcomes |
| B1 Python Engineering | conditional | Async/concurrency/cancellation semantics | HTTP runtime, external/background integration и performance/resource modules |
| A3 Networks, Linux & Security | hard baseline | HTTP/network behavior, TLS/trust baseline, threat/identity/security boundaries | Request tracing, API contracts, identity integration, API abuse controls и downstream failures |
| A2 Software Engineering Practice | reference/baseline по уровню | Test design, change discipline, code review и ADR | Service architecture, verification, delivery |
| B3 Transactional & Operational Data Systems | conditional | Transaction/isolation, driver/store и cache-store behavior | Transaction boundaries, storage-backed idempotency и application caching |
| B5 Distributed Systems & System Design | conditional advanced | Partial failure, delivery guarantees, consistency и coordination trade-offs | Idempotency, async workflows, multi-service migrations |
| B6 Platform, Cloud & Infrastructure Engineering | delivery context | Runtime/deployment mechanics, secret/IAM/network-policy integration, rollout primitives | Identity/API security integration, delivery и resource configuration |
| B7 Reliability, Observability & Production Engineering | conditional advanced | Telemetry, SLI/SLO, load/capacity и incident evidence | Delivery, abuse/overload signals, performance diagnosis и load control |
| C1 Engineering Leadership & Architecture | role context L4+ | Cross-team decision, governance и migration leadership | L4 outcomes; не technical prerequisite самой capability |

## Cycle policy

Hard graph строится только по колонке `Requires`; `related` и external context не участвуют в topological order. После появления external capability IDs новая hard edge принимается только после проверки глобального DAG.
