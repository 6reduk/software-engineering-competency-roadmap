---
artifact: role-view
role: backend-distributed-systems
status: drafting
updated: 2026-09-21
language: ru
---

# Подборка: разработка backend- и распределённых систем

## Для каких задач

Проектирование, реализация и эксплуатация backend-систем: API, данные, интеграции, распределённые взаимодействия, производительность, надёжность и эволюция сервисов.

## Требования по предметным направлениям

| Направление | Значение в подборке | Целевой уровень | Обоснование |
|---|---|---:|---|
| A1 CS & Problem Solving | core | L3 | Complexity, concurrency, memory и problem solving нужны для диагностики и design. |
| A2 Software Engineering Practice | core | L4 | Качество, delivery и стандарты распространяются на команду/несколько команд. |
| A3 Networks, Linux & Security Foundations | core | L3 | Backend-инженер обязан диагностировать путь запроса и базовые security failures. |
| B1 Python Engineering | core | L3 | Production-владение языком; L4 требуется при установлении Python-стандартов. |
| B2 Backend & API Engineering | depth | L4 | Основное прикладное направление специализации. |
| B3 Transactional & Operational Data Systems | depth | L4 | Данные, транзакции, store selection, производительность и эволюция схем критичны. |
| B4 Data Engineering & Analytical Platforms | awareness | L2 | Нужно понимать контракты, pipelines и границы OLTP/OLAP. |
| B5 Distributed Systems & System Design | depth | L4 | Основное системное направление специализации. |
| B6 Platform, Cloud & Infrastructure Engineering | core | L3 | Нужна самостоятельная эксплуатация и конструктивная работа с platform team. |
| B7 Reliability, Observability & Production Engineering | depth | L4 | Mission-critical backend без operational ownership невозможен. |
| B8 Classical ML & Data Science | awareness | L1 | Понимание интеграции и языка взаимодействия. |
| B9 Deep Learning & Foundation Models | awareness | L1 | Понимание ограничений моделей при интеграции. |
| B10 LLM Applications, Retrieval & Agentic Systems | awareness | L2 | Современный backend всё чаще включает model/retrieval integrations. |
| B11 MLOps & LLMOps | awareness | L1 | Понимание lifecycle и границ ответственности. |
| C1 Engineering Leadership & Architecture | core | L3–L4 | ADR, trade-offs, migrations и межкомандные интерфейсы обязательны для lead-роста. |

## Приоритетные outcomes

Инженер способен:

1. Провести запрос от клиента через сеть, приложение, данные и инфраструктуру.
2. Выбрать границы сервиса и контракт с учётом эволюции и отказов.
3. Обеспечить consistency/idempotency и корректную работу с транзакциями.
4. Найти bottleneck по evidence, а не по предположению.
5. Спроектировать наблюдаемость, graceful degradation и recovery.
6. Провести безопасную миграцию данных/API/архитектуры.
7. Защитить решение через требования, альтернативы, риски и стоимость.

## Приоритетные competency clusters

Authoritative B2 requirements после G3: [B2 role requirements](../tracks/b2/role-requirements.md#backend--distributed-systems).

- request lifecycle: `a3.cluster.dns-service-discovery`, `a3.cluster.network-stack`, `a3.cluster.tls-pki`, `a3.cluster.http-proxies`, `b2.cluster.request-runtime`;
- Python runtime и concurrency: `b1.cluster.concurrency-async-parallelism`, `b1.cluster.runtime-memory`, `b1.cluster.errors-resources`;
- API contracts и access boundaries: `b2.cluster.api-contracts`, `b2.cluster.validation-serialization-errors`, `b2.cluster.identity-access-boundaries`;
- data, transactions, caching и messaging: `b3.cluster.relational-model-schema`, `b3.cluster.transactions-concurrency`, `b5.cluster.caching-load-control`, `b5.cluster.messaging-events`;
- distributed reasoning: `b5.cluster.failure-models`, `b5.cluster.consistency-availability`, `b5.cluster.time-order-coordination`, `b5.cluster.idempotency-retries`;
- performance и capacity: `b2.cluster.performance-resource-control`, `b5.cluster.capacity-multi-region`, `b7.cluster.performance-capacity`;
- reliability: `b7.cluster.observability-signals`, `b7.cluster.sli-slo-error-budgets`, `b7.cluster.incident-response`, `b7.cluster.resilience-patterns`;
- delivery/evolution: `a2.cluster.testing-strategy`, `a2.cluster.compatibility-versioning`, `b2.cluster.testing-contracts`, `b2.cluster.evolution-delivery`;
- security: `a3.cluster.threat-modeling-appsec`, `a3.cluster.identity-access`, `a3.cluster.supply-chain-security`;
- architecture communication: `c1.cluster.quality-attributes-tradeoffs`, `c1.cluster.architecture-communication`, `c1.cluster.evolution-migrations`.

Следующий zoom: разложить clusters на capabilities с наблюдаемыми критериями L1–L5.
