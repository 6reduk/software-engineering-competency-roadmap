---
artifact: b2-scenario-blueprint
status: accepted
updated: 2026-08-15
language: ru
---

# Рабочие и interview-сценарии B2

Сценарий проверяет несколько capabilities, но не становится новой competency entity. Метки `S01`–`S15` локальны для blueprint и не являются semantic IDs.

| ID | Module | Рабочий сценарий | Interview probe | Основные capabilities |
|---|---|---|---|---|
| `S01` | `b2.module.http-service-runtime` | Endpoint иногда возвращает неверный error после middleware/dependency refactor; нужно восстановить execution path | «В каком порядке исполняются middleware, dependencies, handler и cleanup; где вы это проверите?» | `b2.capability.trace-request-execution`, `b2.capability.manage-service-resource-lifecycle` |
| `S02` | `b2.module.http-service-runtime` | При graceful shutdown остаются tasks/connections и pod не завершается в budget | Debugging follow-up про lifespan, cancellation, cleanup и evidence отсутствия утечки | `b2.capability.manage-service-resource-lifecycle`, `b2.capability.control-concurrency-cancellation` |
| `S03` | `b2.module.evolvable-api-contracts` | Добавить условно обязательные delivery fields и новый error contract при сосуществовании legacy/new clients | Классифицировать breaking/additive change, предложить migration и consumer evidence | `b2.capability.design-http-api-contracts`, `b2.capability.evolve-api-contracts`, `b2.capability.design-validation-error-contracts`, `b2.capability.verify-contract-compatibility` |
| `S04` | `b2.module.evolvable-api-contracts` | Клиент повторяет create/charge command после timeout; concurrent duplicates дают разные результаты | Спроектировать idempotency identity/result/conflict/retention и разобрать race | `b2.capability.design-idempotent-service-operations`, `b2.capability.design-http-api-contracts` |
| `S05` | `b2.module.identity-aware-boundaries` | Object ID из другого tenant проходит через endpoint с валидным token | Найти trust/enforcement boundary и отличить authentication от object-level authorization | `b2.capability.integrate-identity-access-control`, `b2.capability.design-http-api-contracts` |
| `S06` | `b2.module.service-architecture` | Изменение policy требует правок router, ORM model, client и tests | Предложить boundaries без framework-for-framework's-sake; назвать migration evidence | `b2.capability.design-service-architecture`, `b2.capability.verify-service-behavior` |
| `S07` | `b2.module.transactional-persistence-integration` | DB commit успешен, публикация события/вызов dependency неизвестны после crash | Перечислить failure windows и выбрать recovery/idempotency boundary | `b2.capability.manage-application-transaction-boundaries`, `b2.capability.design-idempotent-service-operations` |
| `S08` | `b2.module.external-service-integration` | Fan-out к медленной dependency игнорирует disconnect/deadline и исчерпывает pool | Диагностировать amplification; провести cancellation и bounded concurrency | `b2.capability.integrate-external-services`, `b2.capability.control-concurrency-cancellation`, `b2.capability.control-service-load-resources` |
| `S09` | `b2.module.background-message-workflows` | Worker падает между side effect и acknowledgement, сообщение приходит повторно | Определить invariant, ack/retry/dedup/recovery и observability | `b2.capability.design-asynchronous-workflows`, `b2.capability.design-idempotent-service-operations` |
| `S10` | `b2.module.service-verification` | Unit tests зелёные, но production serializer/error mapping нарушает клиента | Выбрать минимальный набор test boundaries и объяснить оставшиеся риски | `b2.capability.verify-service-behavior`, `b2.capability.verify-contract-compatibility` |
| `S11` | `b2.module.safe-service-evolution` | Ограниченно обратимое изменение должно сосуществовать с несколькими версиями клиентов | Классифицировать обратимость; построить order, stop conditions, rollback/compensation/roll-forward и telemetry plan | `b2.capability.deliver-service-changes-safely`, `b2.capability.evolve-api-contracts`, `b2.capability.verify-contract-compatibility` |
| `S12` | `b2.module.performance-resource-control` | Median стабилен, p99 растёт нелинейно с concurrency | Построить гипотезы, measurements и experiment, не начиная с random tuning | `b2.capability.diagnose-service-performance`, `b2.capability.trace-request-execution` |
| `S13` | `b2.module.performance-resource-control` | Unbounded queue/pool создаёт timeouts и retry storm | Выбрать admission, bounds, backpressure/degradation и recovery evidence | `b2.capability.control-service-load-resources`, `b2.capability.control-concurrency-cancellation`, `b2.capability.integrate-external-services` |
| `S14` | `b2.module.identity-aware-boundaries` | Bulk-export endpoint принимает дорогой unbounded request и произвольный callback URL | Ограничить operation cost/quota и SSRF target boundary, сохранив legitimate multi-tenant use | `b2.capability.enforce-api-security-abuse-controls`, `b2.capability.control-service-load-resources`, `b2.capability.integrate-identity-access-control` |
| `S15` | `b2.module.transactional-persistence-integration` | Concurrent cache misses создают stampede; invalidation race возвращает stale либо чужой tenant result | Определить key scope, freshness invariant, coalescing/invalidation/fallback и измеримый failure envelope | `b2.capability.integrate-application-caching`, `b2.capability.manage-application-transaction-boundaries`, `b2.capability.control-service-load-resources` |

## Проверка первых slices

### Slice 1 — contract evolution

Primary scenario: `S03`; contrast support: `S10`, `S11`.

Central action остаётся единым: провести совместимое изменение API. Request path, validation, testing и rollout используются только как evidence этой операции.

### Slice 2 — runtime failure

Primary scenario: `S08`; support: `S02`, `S13`.

Central action остаётся единым: диагностировать и устранить cancellation/resource amplification. Общая capacity discipline и platform autoscaling не включаются.
