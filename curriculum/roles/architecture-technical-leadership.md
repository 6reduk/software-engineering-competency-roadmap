---
artifact: role-view
role: architecture-technical-leadership
status: drafting
updated: 2026-08-15
language: ru
---

# Architecture / Technical Leadership

## Ответственность роли

Формирование технического направления, согласование решений между командами и снижение организационных/системных рисков. Роль не равна «самый сильный разработчик» и не предполагает одинаковой экспертности во всех технологиях.

## Роли вертикалей

Для этой роли используются два измерения:

- собственная техническая специализация — 2–4 `depth`-вертикали;
- способность принимать межсистемные решения — обязательный `core/awareness` по остальным.

Ниже приведена проекция для архитектора/tech lead с базовой специализацией Backend / Distributed Systems.

| Track | Роль | Целевой уровень | Обоснование |
|---|---|---:|---|
| A1 CS & Problem Solving | core | L3 | Достаточно для корректного reasoning и оценки ограничений. |
| A2 Software Engineering Practice | core | L5 | Стандарты, governance, delivery и эволюция engineering system. |
| A3 Networks, Linux & Security Foundations | core | L3–L4 | Общий baseline L3; threat modeling, IAM/trust boundaries и supply-chain consequences — L4. |
| B1 Python Engineering | core | L3 | Глубина основного стека без требования быть language implementer. |
| B2 Backend & API Engineering | depth | L4 | Базовая специализация данного role view. |
| B3 Transactional & Operational Data Systems | depth | L4 | Data ownership, store selection и consistency — архитектурный фундамент. |
| B4 Data Engineering & Analytical Platforms | awareness | L3 | Нужно проектировать границы operational/analytical data flows. |
| B5 Distributed Systems & System Design | depth | L5 | Решения организационного масштаба и эволюция систем. |
| B6 Platform, Cloud & Infrastructure Engineering | core | L4 | Platform boundaries, cloud economics, security и delivery strategy. |
| B7 Reliability, Observability & Production Engineering | depth | L5 | SLO, systemic risk, incident learning и resilience strategy. |
| B8 Classical ML & Data Science | awareness | L2 | Понимание lifecycle, evaluation и организационных рисков ML. |
| B9 Deep Learning & Foundation Models | awareness | L2 | Достаточно для проверки feasibility и коммуникации со специалистами. |
| B10 LLM Applications, Retrieval & Agentic Systems | awareness | L2–L3 | Architecture, security, evaluation, cost и vendor/model risks. |
| B11 MLOps & LLMOps | awareness | L2–L3 | Platform/lifecycle boundaries и build/buy decisions. |
| C1 Engineering Leadership & Architecture | integrating depth | L5 | Основная интегрирующая вертикаль роли. |

## Приоритетные outcomes

Инженер способен:

1. Перевести бизнес-цель и ограничения в техническую стратегию.
2. Разделить решение на устойчивые ownership boundaries.
3. Выбрать компромисс и явно назвать его стоимость, риски и reversibility.
4. Создать RFC/ADR, добиться согласования и обеспечить исполнение несколькими командами.
5. Провести эволюционную миграцию без неоправданного big bang.
6. Управлять technical debt как портфелем рисков, а не списком раздражающих задач.
7. Разбирать инциденты системно и менять механизмы, а не искать виноватых.
8. Создать standards/platforms/golden paths, не превращаясь в bottleneck.
9. Развивать инженеров и преемников, снижая зависимость от себя.
10. Оценивать build/buy, vendor lock-in, безопасность и total cost of ownership.

## Приоритетные competency clusters

Authoritative B2 requirements после G3: [B2 role requirements](../tracks/b2/role-requirements.md#architecture--technical-leadership--backend-specialization).

- `c1.cluster.problem-framing-constraints` — problem framing, requirements и constraints;
- `c1.cluster.decomposition-ownership` — architecture decomposition и ownership boundaries;
- `c1.cluster.quality-attributes-tradeoffs` — quality attributes, alternatives и reversibility;
- `c1.cluster.architecture-communication` — RFC, ADR, diagrams и decision records;
- `c1.cluster.strategy-roadmap` — technical strategy, sequencing и portfolio thinking;
- `c1.cluster.evolution-migrations` — migrations, evolutionary architecture и legacy modernization;
- `c1.cluster.risk-security-compliance` — reliability/security/compliance и systemic risk;
- `c1.cluster.platform-standards-dx` — platform strategy, standards и developer experience;
- `c1.cluster.engineering-economics` — build/buy, TCO и vendor risk;
- `c1.cluster.reliability-incident-leadership` — incident leadership и systemic learning;
- `c1.cluster.influence-mentoring-succession` — mentoring, delegation, succession и influence;
- `c1.cluster.feedback-organizational-learning` — metrics, feedback loops и проверка гипотез.

Следующий zoom: разложить clusters на capabilities с наблюдаемыми критериями L3–L5 и привязать их к техническим проектам и кейсам.
