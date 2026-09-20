---
artifact: b5-coverage-map
status: accepted
updated: 2026-09-18
language: ru
---

# Первый реестр учебного покрытия B5

Реестр показывает назначение существующих материалов: что они объясняют, исследуют вопросами, тренируют или оценивают. Источник фактических отношений — YAML `coverage` пяти материалов M2.3. Таблицы ниже сериализуют эти отношения, не создают второй набор. Coverage не равно proficiency, выполнению проекта, завершению модуля или production readiness. Авторский Gate 0 сам не начисляет покрытие.

## Planned blueprint

Принятый [B5 blueprint](README.md) содержит 6 modules, 17 capabilities, 51 outcome L1–L3 и 11 сценариев. Это карта ожидаемых способностей, не 51 выполненный результат и не набор учебных artifacts. [Мандат M2.3](../../../governance/work-packages/M2.3-stale-authority-fencing-slice.md) назначает один slice [TO01](scenarios.md#to01), ограниченно используя [CL01](scenarios.md#cl01).

| Материал | Планируемое назначение | Граница |
|---|---|---|
| index | reference трёх capabilities | Без начисления уровней |
| learn | explain primary L1–L3 и supporting L1/L2 | Leadership L3 отсутствует |
| interview | probe тех же восьми outcomes | Рассуждение не заменяет исполнение |
| kata | practice и assess primary L1/L2 | Одна передача, заданный договор |
| project-spec | integrate и assess primary L2/L3 | Самостоятельный выбор, несколько историй |

Primary: [причинный порядок](capabilities.md#reconstruct-causal-order) и [исключение старого владельца](capabilities.md#exclude-stale-actors). Supporting: [границы лидерства](capabilities.md#assess-leadership-guarantees), только reference/explain/probe. План не суммируется с фактом.

## Фактические artifact relationships: accepted

Все пять материалов приняты после G31 и точечной проверки correction-pass M2.3a. В строке с двумя roles каждая роль применяется к каждому перечисленному target; одна тройка `(artifact, target, role)` считается один раз.

| Artifact | Exact targets | Roles | Отношений |
|---|---|---|---:|
| [`b5.index.stale-authority-fencing`](slices/stale-authority-fencing/README.md) | `b5.capability.reconstruct-causal-order`, `b5.capability.exclude-stale-actors`, `b5.capability.assess-leadership-guarantees` | `reference` | 3 |
| [`b5.learn.authority-lease-fencing-boundary`](slices/stale-authority-fencing/learn/authority-lease-fencing-boundary.md) | `b5.level-outcome.reconstruct-causal-order-l1-explain-history`, `b5.level-outcome.reconstruct-causal-order-l2-define-bounded-model`, `b5.level-outcome.reconstruct-causal-order-l3-defend-tradeoff`, `b5.level-outcome.exclude-stale-actors-l1-explain-history`, `b5.level-outcome.exclude-stale-actors-l2-define-bounded-model`, `b5.level-outcome.exclude-stale-actors-l3-defend-tradeoff`, `b5.level-outcome.assess-leadership-guarantees-l1-explain-history`, `b5.level-outcome.assess-leadership-guarantees-l2-define-bounded-model` | `explain` | 8 |
| [`b5.interview.old-worker-after-authority-transfer`](slices/stale-authority-fencing/interview/old-worker-after-authority-transfer.md) | `b5.level-outcome.reconstruct-causal-order-l1-explain-history`, `b5.level-outcome.reconstruct-causal-order-l2-define-bounded-model`, `b5.level-outcome.reconstruct-causal-order-l3-defend-tradeoff`, `b5.level-outcome.exclude-stale-actors-l1-explain-history`, `b5.level-outcome.exclude-stale-actors-l2-define-bounded-model`, `b5.level-outcome.exclude-stale-actors-l3-defend-tradeoff`, `b5.level-outcome.assess-leadership-guarantees-l1-explain-history`, `b5.level-outcome.assess-leadership-guarantees-l2-define-bounded-model` | `probe` | 8 |
| [`b5.kata.reject-stale-worker-effect`](slices/stale-authority-fencing/kata/reject-stale-worker-effect.md) | `b5.level-outcome.reconstruct-causal-order-l1-explain-history`, `b5.level-outcome.reconstruct-causal-order-l2-define-bounded-model`, `b5.level-outcome.exclude-stale-actors-l1-explain-history`, `b5.level-outcome.exclude-stale-actors-l2-define-bounded-model` | `practice`, `assess` | 8 |
| [`b5.project-spec.fenced-order-allocation-worker`](slices/stale-authority-fencing/project-spec/fenced-order-allocation-worker.md) | `b5.level-outcome.reconstruct-causal-order-l2-define-bounded-model`, `b5.level-outcome.reconstruct-causal-order-l3-defend-tradeoff`, `b5.level-outcome.exclude-stale-actors-l2-define-bounded-model`, `b5.level-outcome.exclude-stale-actors-l3-defend-tradeoff` | `integrate`, `assess` | 8 |

## Пересчёт по semantic targets

Capabilities разрешаются в [каталоге действий](capabilities.md); outcomes — в разделах [причинного порядка](level-outcomes.md#reconstruct-causal-order), [исключения старого владельца](level-outcomes.md#exclude-stale-actors) и [оценки лидерства](level-outcomes.md#assess-leadership-guarantees). Все IDs ниже уже существуют в принятой карте.

| Target | reference | explain | probe | practice | assess | integrate | Всего |
|---|---:|---:|---:|---:|---:|---:|---:|
| `b5.capability.reconstruct-causal-order` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `b5.capability.exclude-stale-actors` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `b5.capability.assess-leadership-guarantees` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `b5.level-outcome.reconstruct-causal-order-l1-explain-history` | 0 | 1 | 1 | 1 | 1 | 0 | 4 |
| `b5.level-outcome.reconstruct-causal-order-l2-define-bounded-model` | 0 | 1 | 1 | 1 | 2 | 1 | 6 |
| `b5.level-outcome.reconstruct-causal-order-l3-defend-tradeoff` | 0 | 1 | 1 | 0 | 1 | 1 | 4 |
| `b5.level-outcome.exclude-stale-actors-l1-explain-history` | 0 | 1 | 1 | 1 | 1 | 0 | 4 |
| `b5.level-outcome.exclude-stale-actors-l2-define-bounded-model` | 0 | 1 | 1 | 1 | 2 | 1 | 6 |
| `b5.level-outcome.exclude-stale-actors-l3-defend-tradeoff` | 0 | 1 | 1 | 0 | 1 | 1 | 4 |
| `b5.level-outcome.assess-leadership-guarantees-l1-explain-history` | 0 | 1 | 1 | 0 | 0 | 0 | 2 |
| `b5.level-outcome.assess-leadership-guarantees-l2-define-bounded-model` | 0 | 1 | 1 | 0 | 0 | 0 | 2 |
| **Итого accepted** | **3** | **8** | **8** | **4** | **8** | **4** | **35** |

Итого: **5 учебных artifacts, 11 уникальных targets, 35 отношений**. Из targets три capabilities и восемь outcomes. Outcome-level отношений 32: L1 — 10, L2 — 14, L3 — 8. Принято по D-075: **5 artifacts / 35 relationships**. Coverage map — служебный реестр с `artifact`, без собственного `coverage`; он не является шестым учебным материалом. B5 README blueprint тоже не добавляет отношений slice.

## Почему это соответствует evidence заданий

Index только адресует три действия. Learn объясняет причинные рёбра и неизвестный порядок, ресурсную проверку, варианты authority и цену остановки при разделении связи; заданная quorum-модель используется лишь для supporting L1/L2. Interview исследует те же действия вопросами и rubric, поэтому получает probe, не assess.

Kata сначала просит объяснить заданный след L1, затем самостоятельно построить граф с конкурентной парой, локализовать проверку и получить контроль/дефект/исправление/recovery L2. Project интегрирует обе primary способности L2, а L3 оценивает через выбор порядка и authority, альтернативы, неполные следы, неизвестный ответ, разделение связи и обход. Эти задания способны породить evidence, но результат участника пока отсутствует. План и фактическая регистрация совпадают, отклонений нет.

[Ролевые требования](role-requirements.md) не меняются. Backend: причинный порядок L2 required, исключение L3 conditional, leadership L2 deepening. Architecture: порядок L3 deepening, исключение L3 required; required leadership L3 **не покрыт** этим slice. Наличие supporting L1/L2 не закрывает L3.

Ни B2/B3/B6/B7/C1, ни leadership L3, ни B5 L4/L5, implementation или production operations не начислены. [C1-линза проекта](slices/stale-authority-fencing/project-spec/fenced-order-allocation-worker.md#decision-record) — носитель авторского обоснования и учебного требования, не C1 capability или proficiency. Остальные 14 capabilities B5 и 43 outcomes не имеют прямых targets в этом первом реестре; их blueprint не превращён в coverage. Второй slice не выбран и не создан.
