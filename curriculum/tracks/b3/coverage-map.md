---
artifact: b3-coverage-map
status: accepted
updated: 2026-09-13
language: ru
---

# Coverage B3: принятые SQ01 и SE01

Реестр показывает, какие существующие материалы объясняют или проверяют профессиональные действия. Coverage — назначение artifact, не результат деятельности участника и не proficiency. Источник связей — YAML `coverage` каждого материала; строки таблиц ниже сериализуют эти отношения, а не добавляют их повторно. Принятый capability blueprint сам по себе учебных связей не создаёт.

## Planned map

План M1.9.3 относится только к [SQ01](scenarios.md#sq01) и [модулю корректных результатов](modules.md#sql-querying). Две capabilities и шесть принятых outcomes существуют в [каталоге](level-outcomes.md#compose-relational-queries). Планируемое назначение отделено от фактической регистрации ниже:

| Материал | Планируемая роль | Уровни двух capabilities |
|---|---|---|
| index | reference | Только capabilities, без уровня |
| learn | explain | L1–L3 |
| interview | probe | L1–L3 |
| kata | practice, assess | L1/L2 |
| project-spec | integrate, assess | L2/L3 |

SE01 зарегистрирован отдельно ниже по M1.9.5 после подтверждённого Gate 0 и принятия G26; его отношения входят в accepted totals. BR01 остаётся кандидатом из [B3 README](README.md) без artifacts и coverage. Остальные модули не получают связей из этих примеров.

## Фактические принятые artifact relationships SQ01

Пересчёт 2026-09-13 по YAML пяти SQ01 и пяти SE01 artifacts подтверждает `status: accepted`: по 30 принятых отношений к восьми targets в каждом slice. Прежний текст о review описывал авторскую передачу до G24/G26; текущий factual recount использует фактические статусы материалов. Принятие SQ01 и SE01 не означает proficiency участника.

| Artifact | Exact targets | Roles | Число отношений |
|---|---|---|---:|
| [`b3.index.sql-result-correctness`](slices/sql-result-correctness/README.md) | `b3.capability.compose-relational-queries`, `b3.capability.derive-grouped-window-results` | `reference` | 2 |
| [`b3.learn.join-cardinality-and-result-grain`](slices/sql-result-correctness/learn/join-cardinality-and-result-grain.md) | `b3.level-outcome.compose-relational-queries-l1-explain-observed-behavior`, `b3.level-outcome.compose-relational-queries-l2-perform-bounded-action`, `b3.level-outcome.compose-relational-queries-l3-defend-uncertain-decision`, `b3.level-outcome.derive-grouped-window-results-l1-explain-observed-behavior`, `b3.level-outcome.derive-grouped-window-results-l2-perform-bounded-action`, `b3.level-outcome.derive-grouped-window-results-l3-defend-uncertain-decision` | `explain` | 6 |
| [`b3.interview.correct-query-wrong-total`](slices/sql-result-correctness/interview/correct-query-wrong-total.md) | `b3.level-outcome.compose-relational-queries-l1-explain-observed-behavior`, `b3.level-outcome.compose-relational-queries-l2-perform-bounded-action`, `b3.level-outcome.compose-relational-queries-l3-defend-uncertain-decision`, `b3.level-outcome.derive-grouped-window-results-l1-explain-observed-behavior`, `b3.level-outcome.derive-grouped-window-results-l2-perform-bounded-action`, `b3.level-outcome.derive-grouped-window-results-l3-defend-uncertain-decision` | `probe` | 6 |
| [`b3.kata.stop-join-multiplication`](slices/sql-result-correctness/kata/stop-join-multiplication.md) | `b3.level-outcome.compose-relational-queries-l1-explain-observed-behavior`, `b3.level-outcome.compose-relational-queries-l2-perform-bounded-action`, `b3.level-outcome.derive-grouped-window-results-l1-explain-observed-behavior`, `b3.level-outcome.derive-grouped-window-results-l2-perform-bounded-action` | `practice`, `assess` | 8 |
| [`b3.project-spec.orders-financial-summary`](slices/sql-result-correctness/project-spec/orders-financial-summary.md) | `b3.level-outcome.compose-relational-queries-l2-perform-bounded-action`, `b3.level-outcome.compose-relational-queries-l3-defend-uncertain-decision`, `b3.level-outcome.derive-grouped-window-results-l2-perform-bounded-action`, `b3.level-outcome.derive-grouped-window-results-l3-defend-uncertain-decision` | `integrate`, `assess` | 8 |

Одна пара `(target, role)` одного artifact — одно отношение. В строках с двумя roles каждое назначение применяется к каждому перечисленному target.

## Recount SQ01 по semantic target

| Target | reference | explain | probe | practice | assess | integrate | Всего |
|---|---:|---:|---:|---:|---:|---:|---:|
| `b3.capability.compose-relational-queries` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `b3.capability.derive-grouped-window-results` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `b3.level-outcome.compose-relational-queries-l1-explain-observed-behavior` | 0 | 1 | 1 | 1 | 1 | 0 | 4 |
| `b3.level-outcome.compose-relational-queries-l2-perform-bounded-action` | 0 | 1 | 1 | 1 | 2 | 1 | 6 |
| `b3.level-outcome.compose-relational-queries-l3-defend-uncertain-decision` | 0 | 1 | 1 | 0 | 1 | 1 | 4 |
| `b3.level-outcome.derive-grouped-window-results-l1-explain-observed-behavior` | 0 | 1 | 1 | 1 | 1 | 0 | 4 |
| `b3.level-outcome.derive-grouped-window-results-l2-perform-bounded-action` | 0 | 1 | 1 | 1 | 2 | 1 | 6 |
| `b3.level-outcome.derive-grouped-window-results-l3-defend-uncertain-decision` | 0 | 1 | 1 | 0 | 1 | 1 | 4 |
| **Итого** | **2** | **6** | **6** | **4** | **8** | **4** | **30** |

Два capability targets и шесть outcome targets; outcome-level отношений 28: L1 — 8, L2 — 12, L3 — 8. Kata не получает L3, project не получает L1; L4/L5 отсутствуют. Outcome ID каждого назначения можно сверить в [compose](level-outcomes.md#compose-relational-queries) и [grouped/window](level-outcomes.md#derive-grouped-window-results).

## Почему роли соответствуют заданиям

Learn объясняет пары строк, NULL, пустые совпадения, вход окна и выбор композиции при разных прочтениях требования. Interview выявляет эти рассуждения через последовательные вопросы и rubric, поэтому получает probe. Kata практикует и оценивает прослеживание строк с поддержкой (L1) и самостоятельный запрос/сверку по фиксированному договору (L2). Project интегрирует те же действия L2 и требует L3 evidence: две трактовки, различающие таблицы, decision record, локализацию искажения и сравнение этапов по смыслу и сопровождаемости. Реальные результаты должны быть получены участником и отдельно проверены.

Ролевые проекции не меняются: [Backend и Architecture](role-requirements.md) ссылаются на принятые outcomes. Внешняя подготовка, runtime Gate 0 автора, источники PostgreSQL и собственная SQL-схема задания не являются отдельными proficiency relationships. Query plans/indexes, relational schema, B2 verification и B4 analytics не начисляются.

## SE01: planned map и фактическая принятая регистрация

[M1.9.5](../../../governance/work-packages/M1.9.5-schema-evolution-se01-slice.md) после подтверждённого Gate 0 создал [маршрут совместимого изменения суммы](slices/compatible-orders-amount-migration/README.md). План и факт совпадают: index — reference двух capabilities; learn/interview — explain/probe шести L1–L3 outcomes; kata — practice/assess четырёх L1/L2 outcomes; project — integrate/assess четырёх L2/L3 outcomes. Все пять материалов имеют status: accepted после G26 и correction-pass M1.9.5a. Источник регистрации — их YAML coverage; runtime автора не создаёт отношений сам по себе.

| Artifact | Exact targets | Roles | Число отношений |
|---|---|---|---:|
| [`b3.interview.concurrent-write-during-backfill`](slices/compatible-orders-amount-migration/interview/concurrent-write-during-backfill.md) | `b3.level-outcome.plan-compatible-schema-transitions-l1-explain-observed-behavior`, `b3.level-outcome.plan-compatible-schema-transitions-l2-perform-bounded-action`, `b3.level-outcome.plan-compatible-schema-transitions-l3-defend-uncertain-decision`, `b3.level-outcome.validate-online-data-change-l1-explain-observed-behavior`, `b3.level-outcome.validate-online-data-change-l2-perform-bounded-action`, `b3.level-outcome.validate-online-data-change-l3-defend-uncertain-decision` | `probe` | 6 |
| [`b3.kata.stop-stale-orders-backfill`](slices/compatible-orders-amount-migration/kata/stop-stale-orders-backfill.md) | `b3.level-outcome.plan-compatible-schema-transitions-l1-explain-observed-behavior`, `b3.level-outcome.plan-compatible-schema-transitions-l2-perform-bounded-action`, `b3.level-outcome.validate-online-data-change-l1-explain-observed-behavior`, `b3.level-outcome.validate-online-data-change-l2-perform-bounded-action` | `practice`, `assess` | 8 |
| [`b3.learn.expand-backfill-validate-contract`](slices/compatible-orders-amount-migration/learn/expand-backfill-validate-contract.md) | `b3.level-outcome.plan-compatible-schema-transitions-l1-explain-observed-behavior`, `b3.level-outcome.plan-compatible-schema-transitions-l2-perform-bounded-action`, `b3.level-outcome.plan-compatible-schema-transitions-l3-defend-uncertain-decision`, `b3.level-outcome.validate-online-data-change-l1-explain-observed-behavior`, `b3.level-outcome.validate-online-data-change-l2-perform-bounded-action`, `b3.level-outcome.validate-online-data-change-l3-defend-uncertain-decision` | `explain` | 6 |
| [`b3.project-spec.compatible-orders-amount-migration`](slices/compatible-orders-amount-migration/project-spec/compatible-orders-amount-migration.md) | `b3.level-outcome.plan-compatible-schema-transitions-l2-perform-bounded-action`, `b3.level-outcome.plan-compatible-schema-transitions-l3-defend-uncertain-decision`, `b3.level-outcome.validate-online-data-change-l2-perform-bounded-action`, `b3.level-outcome.validate-online-data-change-l3-defend-uncertain-decision` | `integrate`, `assess` | 8 |
| [`b3.index.compatible-orders-amount-migration`](slices/compatible-orders-amount-migration/README.md) | `b3.capability.plan-compatible-schema-transitions`, `b3.capability.validate-online-data-change` | `reference` | 2 |

Каждая пара (target, role) одного artifact считается один раз; две roles применяются к каждому target строки. Допустимы только capabilities планирования совместимых переходов и проверки ограниченного изменения, а также их принятые outcomes. Ни B2, ни изоляция транзакций, ни monetary domain или PostgreSQL operations не получают отдельного coverage.

### Recount SE01: accepted

| Target | reference | explain | probe | practice | assess | integrate | Всего |
|---|---:|---:|---:|---:|---:|---:|---:|
| `b3.capability.plan-compatible-schema-transitions` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `b3.capability.validate-online-data-change` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `b3.level-outcome.plan-compatible-schema-transitions-l1-explain-observed-behavior` | 0 | 1 | 1 | 1 | 1 | 0 | 4 |
| `b3.level-outcome.plan-compatible-schema-transitions-l2-perform-bounded-action` | 0 | 1 | 1 | 1 | 2 | 1 | 6 |
| `b3.level-outcome.plan-compatible-schema-transitions-l3-defend-uncertain-decision` | 0 | 1 | 1 | 0 | 1 | 1 | 4 |
| `b3.level-outcome.validate-online-data-change-l1-explain-observed-behavior` | 0 | 1 | 1 | 1 | 1 | 0 | 4 |
| `b3.level-outcome.validate-online-data-change-l2-perform-bounded-action` | 0 | 1 | 1 | 1 | 2 | 1 | 6 |
| `b3.level-outcome.validate-online-data-change-l3-defend-uncertain-decision` | 0 | 1 | 1 | 0 | 1 | 1 | 4 |
| **Итого accepted SE01** | **2** | **6** | **6** | **4** | **8** | **4** | **30** |

Два capability targets, шесть outcome targets; 28 outcome-level отношений: L1 — 8, L2 — 12, L3 — 8. Планирование: [L1–L3](level-outcomes.md#plan-compatible-schema-transitions); проверка изменения: [L1–L3](level-outcomes.md#validate-online-data-change). Kata не получает L3, project не получает L1; L4/L5 отсутствуют.

Learn объясняет состояния, гонку, полноту, порядок ограничений и компромиссы неизвестного writer. Interview исследует то же рассуждение через probe. Kata даёт заданную матрицу для объяснения L1 и самостоятельный ограниченный план/исполнение/сверку/stop-resume для L2. Project интегрирует обе способности L2 и оценивает L3 через сравнение альтернатив на различающих данных, неизвестного потребителя, конфликт срока/доступности и decision record. Это назначения заданий, не доказательства выполнения участником.

## Итоговый factual recount по статусам

| Статус материалов | Artifacts | Уникальные targets | reference | explain | probe | practice | assess | integrate | Relationships |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| accepted: SQ01 | 5 | 8 | 2 | 6 | 6 | 4 | 8 | 4 | 30 |
| accepted: SE01 | 5 | 8 | 2 | 6 | 6 | 4 | 8 | 4 | 30 |
| Все зарегистрированные, без повышения статуса | 10 | 16 | 4 | 12 | 12 | 8 | 16 | 8 | 60 |

Accepted totals составляют 60: по 30 отношений SQ01 и SE01. Планируемые отношения не суммируются с фактическими повторно. Принятие G26 подтверждает качество материалов и правдивость регистрации, но не является module completion, proficiency участника или ImplementationReference; BR01 не запущен.
