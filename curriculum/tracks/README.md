---
id: ela.index.skeleton-matrix
kind: index
title: Skeleton matrix
status: accepted
updated: 2026-08-15
language: ru
---

# Skeleton matrix программы

Это укрупнённая карта A1–C1. Она определяет ownership и границы до детализации capabilities. Cluster здесь является навигационной областью, а не списком будущих файлов.

Все target levels интерпретируются по канонической [`Модели уровней`](../program/level-model.md); track-level значение остаётся навигационным summary и не назначается автоматически каждой capability.

## Контракт карточки трека

Каждая карточка содержит:

1. `Mission` — какую инженерную ответственность развивает трек.
2. `In scope` — принадлежащие треку вопросы.
3. `Non-goals` — соседние вопросы с другим owner.
4. `Clusters` — 5–12 крупных областей без atomic topics.
5. `Hard baseline prerequisites` — только безусловный минимальный gate; пустой список допустим.
6. `Conditional prerequisites` — module/cluster-specific зависимости, если они есть.
7. `Strong connections` — важные связи, не создающие prerequisite.

`Strong connections` — направленная editorial/navigation связь: карточка перечисляет соседей, особенно важных для понимания собственного scope. Обратная запись полезна, но не обязательна; симметрия не является инвариантом и не должна достраиваться автоматически.

## Индекс

### Foundation

- [A1 Computer Science & Problem Solving](catalog/a1-computer-science.md)
- [A2 Software Engineering Practice](catalog/a2-software-engineering.md)
- [A3 Networks, Linux & Security Foundations](catalog/a3-networks-linux-security.md)

### Technical verticals

- [B1 Python Engineering](catalog/b1-python-engineering.md)
- [B2 Backend & API Engineering](catalog/b2-backend-api.md)
- [B3 Transactional & Operational Data Systems](catalog/b3-transactional-data.md)
- [B4 Data Engineering & Analytical Platforms](catalog/b4-data-engineering.md)
- [B5 Distributed Systems & System Design](catalog/b5-distributed-systems.md)
- [B6 Platform, Cloud & Infrastructure Engineering](catalog/b6-platform-cloud.md)
- [B7 Reliability, Observability & Production Engineering](catalog/b7-reliability-production.md)
- [B8 Classical Machine Learning & Data Science](catalog/b8-classical-ml.md)
- [B9 Deep Learning & Foundation Models](catalog/b9-deep-learning.md)
- [B10 LLM Applications, Retrieval & Agentic Systems](catalog/b10-llm-applications.md)
- [B11 MLOps & LLMOps](catalog/b11-mlops-llmops.md)

### Integration

- [C1 Engineering Leadership & Architecture](catalog/c1-leadership-architecture.md)

### Role projection

- [Backend/Distributed и Architecture/Leadership](../roles/role-summary.md)
