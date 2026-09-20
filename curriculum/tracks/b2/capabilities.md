---
artifact: b2-capability-blueprint
status: accepted
updated: 2026-08-15
language: ru
---

# Capabilities B2

Все записи используют aggregate metadata/defaults из `README.md`. Формулировка action задаёт границу capability; темы и framework API появятся только в artifacts.

| ID | Title | Primary cluster | Наблюдаемое действие | Primary module |
|---|---|---|---|---|
| `b2.capability.trace-request-execution` | Трассировка выполнения запроса | `b2.cluster.request-runtime` | Прослеживает выполнение запроса через service pipeline, локализует границу изменения состояния и объясняет итоговый response/failure | `b2.module.http-service-runtime` |
| `b2.capability.manage-service-resource-lifecycle` | Управление lifecycle ресурсов сервиса | `b2.cluster.request-runtime` | Задаёт и проверяет lifecycle request/application ресурсов, включая acquire, reuse, bounded/deterministic cleanup в контролируемой boundary и shutdown | `b2.module.http-service-runtime` |
| `b2.capability.design-http-api-contracts` | Проектирование HTTP API-контрактов | `b2.cluster.api-contracts` | Проектирует HTTP API-контракт из требований клиента, явно определяя semantics, schemas, errors и operational constraints | `b2.module.evolvable-api-contracts` |
| `b2.capability.evolve-api-contracts` | Эволюция API-контрактов | `b2.cluster.evolution-delivery` | Проводит изменение API при сосуществовании клиентов, сохраняя требуемую совместимость и управляя deprecation | `b2.module.evolvable-api-contracts` |
| `b2.capability.design-validation-error-contracts` | Validation и error contracts | `b2.cluster.validation-serialization-errors` | Проектирует границы validation/serialization и стабильный error contract, пригодный для клиента и диагностики | `b2.module.evolvable-api-contracts` |
| `b2.capability.integrate-identity-access-control` | Интеграция identity и access control | `b2.cluster.identity-access-boundaries` | Проводит identity/tenant context через сервис и размещает authn/authz enforcement на корректных границах | `b2.module.identity-aware-boundaries` |
| `b2.capability.enforce-api-security-abuse-controls` | API security и abuse controls | `b2.cluster.identity-access-boundaries` | Размещает endpoint/service controls для untrusted input/targets, field exposure, request/operation cost, quota/rate и adversarial resource consumption | `b2.module.identity-aware-boundaries` |
| `b2.capability.design-service-architecture` | Архитектура backend-сервиса | `b2.cluster.service-architecture` | Разделяет service code и зависимости так, чтобы бизнес-правила, adapters и delivery concerns изменялись и тестировались контролируемо | `b2.module.service-architecture` |
| `b2.capability.manage-application-transaction-boundaries` | Application transaction boundaries | `b2.cluster.persistence-transactions` | Согласует application operation с database transaction и side effects, определяя commit, rollback и retry boundaries | `b2.module.transactional-persistence-integration` |
| `b2.capability.integrate-application-caching` | Интеграция application caching | `b2.cluster.persistence-transactions` | Интегрирует cache с явными key/tenant scope, freshness/invalidation, miss/stale/failure и concurrency semantics | `b2.module.transactional-persistence-integration` |
| `b2.capability.design-idempotent-service-operations` | Идемпотентные service operations | `b2.cluster.api-contracts` | Проектирует повторяемую service operation с явной identity, result semantics, concurrency behavior и retention policy | `b2.module.evolvable-api-contracts` |
| `b2.capability.integrate-external-services` | Интеграция внешних сервисов | `b2.cluster.async-background-integration` | Интегрирует downstream dependency с явными timeout/deadline, failure mapping, resource и retry boundaries | `b2.module.external-service-integration` |
| `b2.capability.design-asynchronous-workflows` | Асинхронные и message workflows | `b2.cluster.async-background-integration` | Проектирует переход от request к background/message processing с явными acknowledgement, retry, duplicate/recovery и observability boundaries | `b2.module.background-message-workflows` |
| `b2.capability.control-concurrency-cancellation` | Concurrency и cancellation | `b2.cluster.async-background-integration` | Ограничивает конкурентную работу, проводит cancellation/deadline и обеспечивает bounded cleanup в контролируемых lifecycle boundaries | `b2.module.external-service-integration` |
| `b2.capability.verify-service-behavior` | Проверка поведения сервиса | `b2.cluster.testing-contracts` | Строит набор проверок на подходящих границах, доказывающий service behavior и ключевые failure paths без хрупкой привязки к реализации | `b2.module.service-verification` |
| `b2.capability.verify-contract-compatibility` | Проверка совместимости контрактов | `b2.cluster.testing-contracts` | Проверяет совместимость producer/consumer contracts и обнаруживает breaking change до опасного rollout | `b2.module.service-verification` |
| `b2.capability.deliver-service-changes-safely` | Безопасная поставка изменений сервиса | `b2.cluster.evolution-delivery` | Планирует и проводит service change с migration order, обратимостью/компенсацией, roll-forward и наблюдаемыми условиями остановки | `b2.module.safe-service-evolution` |
| `b2.capability.diagnose-service-performance` | Диагностика производительности сервиса | `b2.cluster.performance-resource-control` | Локализует latency/throughput bottleneck по измерениям service path и подтверждает причинность экспериментом | `b2.module.performance-resource-control` |
| `b2.capability.control-service-load-resources` | Управление нагрузкой и ресурсами | `b2.cluster.performance-resource-control` | Задаёт pools, concurrency/queue limits, admission и backpressure так, чтобы сервис сохранял предсказуемое поведение при перегрузке | `b2.module.performance-resource-control` |

## Намеренно не выделено

- «Знать FastAPI/Pydantic/ASGI» — это технология и topics/artifacts, а не capability.
- «Писать CRUD» — слишком узкая реализация и не отражает инженерное решение.
- «Проектировать distributed systems» — владелец B5.
- «Обеспечивать SRE» — общая дисциплина принадлежит B7; B2 отвечает за service-specific behavior и instrumentation.
- «Руководить API governance» — организационная часть C1; B2 может владеть только техническими conventions и migration mechanisms.
