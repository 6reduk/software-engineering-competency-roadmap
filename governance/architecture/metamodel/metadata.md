---
id: ela.metamodel.metadata
kind: metamodel
status: accepted
updated: 2026-08-18
---

# Минимальные метаданные

Поля добавляются только для навигации, review, coverage или freshness.

## Общие обязательные поля

```yaml
id: b2.learn.http-idempotency
kind: learn
title: HTTP idempotency
status: drafting
updated: 2026-08-14
language: ru
```

## Capability

```yaml
id: b2.capability.evolve-api-contracts
kind: capability
title: Эволюция API-контрактов
owner_track: b2
primary_cluster: b2.cluster.api-contracts
status: drafting
updated: 2026-08-14
```

## LevelOutcome

```yaml
id: b2.level-outcome.evolve-api-contracts-l4-cross-team-migration
kind: level-outcome
capability: b2.capability.evolve-api-contracts
level: L4
status: drafting
updated: 2026-08-14
```

Action, context, autonomy и evidence criteria хранятся в теле outcome/capability до появления проверенного автоматического потребителя.

## Topic

```yaml
id: b2.topic.http-idempotency
kind: topic
title: Семантика HTTP idempotency
owner_track: b2
status: drafting
updated: 2026-08-14
```

Topic необязателен: короткая ментальная модель может оставаться частью brief.

## Module

```yaml
id: b2.module.reliable-http-api
kind: module
title: Надёжный HTTP API
owner_track: b2
status: drafting
updated: 2026-08-14
verified_baseline: 2026-08-14
versions: {}
```

Module хранит общий freshness baseline. Version-sensitive Artifact задаёт `last_verified`/`versions` только как override.

## Artifact и coverage

```yaml
id: b2.interview.http-idempotency
kind: interview
title: Идемпотентность HTTP-операций
owner_track: b2
module: b2.module.reliable-http-api
topics:
  - b2.topic.http-idempotency
coverage:
  - target: b2.capability.design-idempotent-operations
    role: probe
  - target: b2.level-outcome.design-idempotent-operations-l3-failure-recovery
    role: probe
status: drafting
updated: 2026-08-14
```

Capability-level coverage не подтверждает конкретный уровень. Для level coverage нужен LevelOutcome ID.

## Role requirements

Track-level summary:

```yaml
role: ela.role-view.backend-distributed
track: b2
importance: depth
target_level_summary: L4
```

Summary используется для навигации и не наследуется всеми capabilities.

Authoritative detail:

```yaml
role: ela.role-view.backend-distributed
required_outcomes:
  - b2.level-outcome.evolve-api-contracts-l3-compatible-change
  - b2.level-outcome.evolve-api-contracts-l4-cross-team-migration
```

Отсутствие outcome означает «требование ещё не задано», а не нулевой уровень.

## ImplementationReference

```yaml
id: b2.implementation-reference.reliable-api-example-01
kind: implementation-reference
title: Пример реализации надёжного API
owner_track: b2
module: b2.module.reliable-http-api
implements: b2.project-spec.reliable-api
locator: https://github.com/example/reliable-api
revision: v1.0.0
review_status: reviewed
reviewed_at: 2026-08-14
status: published
updated: 2026-08-14
language: ru
```

`locator` адресует внешний project repository и не обязан указывать GitHub. Поле `repository` зарезервировано для ID из глобального `governance/registry/repositories.yaml` в cross-repository references между управляемыми сущностями программы.

## Статусы

```text
Planning entities: proposed → accepted
Content artifacts: drafting → review → accepted → published → maintenance
                                      ↘ needs-update
                                      ↘ superseded
```

`accepted` имеет контекстную семантику: для planning entity это принятое решение или контракт, а для content artifact — состояние после успешного review. После исправлений artifact может вернуться из `review` в `drafting`; из `accepted`, `published` или `maintenance` — перейти в `needs-update` либо `superseded`.

В канонических metadata используется `drafting`, не `draft`.

## Необязательные поля

- `prerequisites`, `related` — semantic IDs;
- `related_clusters`;
- `non_goals`;
- `last_verified`, `versions` — Artifact overrides Module baseline;
- `redirected_to` — только денормализованная подсказка tombstone; authoritative redirect хранится в global alias registry;
- `superseded_by`;
- `translation_of`;
- `sources` — только при реальном машинном потребителе.

## Не формализуется в M1.1

- JSON Schema и validator;
- полный source registry;
- coverage score;
- вычисление hiring-grade;
- обязательная taxonomy tags;
- формат будущего сайта.

Это добавляется после двух pilot slices при появлении реальных потребителей.
