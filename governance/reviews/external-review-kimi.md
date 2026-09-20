---
id: ela.review.external-kimi
kind: review
status: published
updated: 2026-08-15
model: kimi
verdict: accepted_with_changes
---

# Независимое внешнее review — Engineering Leadership & Architecture Blueprint

## Scope

Полный пакет `engineering-leadership-architecture-blueprint/` на момент review (после acceptance M1.4 / G3):

- корневые governance-документы: `README.md`, `governance/state/STATUS.md`, `governance/decisions.md`, `governance/state/OPEN-QUESTIONS.md`, `governance/planning/execution-plan.md`, `authoring/workflow/review-protocol.md`;
- `docs/01`–`docs/08` (vision, track map, level model, learning flow, content standard, information architecture, diagnostic, audience);
- `governance/architecture/metamodel/` (entities, relationships-and-invariants, identifiers, metadata);
- `matrix/` (README, role-summary, 15 skeleton track cards a1–c1);
- `pilot/` (M1.3 pilot selection, blueprint B2: modules, capabilities, level-outcomes, prerequisites, role-requirements, scenarios, coverage-map);
- `routes/` (Backend / Distributed Systems, Architecture / Technical Leadership);
- `governance/registry/` (repositories.yaml, id-aliases.yaml);
- `governance/reviews/` (записи M1.1–M1.4 — проверялись на согласованность с артефактами, не как предмет повторного gate).

## Model

`kimi` (Kimi Code CLI). Reviewer не редактировал проверяемые файлы. Проверка выполнялась в три роли по `authoring/workflow/review-protocol.md`: structure (границы, декомпозиция, соответствие метамодели, идентификаторы, prerequisites), subject-matter/domain (техническая корректность и полнота), learning/interview (наблюдаемость уровней, полезность как конспекта). Сквозные несоответствия между governance-документами проверены основным агентом напрямую; `matrix/` и `pilot/+routes/` дополнительно проверены двумя независимыми параллельными проходами.

## Verdict

**accepted_with_changes**

Блокеров не обнаружено. Пакет внутренне согласован на уровне метамодели, skeleton matrix и пилотного blueprint B2; заявленные количественные характеристики (10 modules / 19 capabilities / 69 LevelOutcomes; 155 clusters) подтверждаются пересчётом. Однако есть несколько major-несоответствий между старыми M0-документами и принятой метамоделью M1.1 — они не ломают текущий пакет, но создадут конфликтующие примеры для следующих work packages, если их не исправить до M1.5.

## Findings

### F-01 — major

- **artifact:** `governance/architecture/information-architecture.md`
- **evidence:** Пример метаданных атомарного артефакта (строки 49–62) использует `id: py-iter-001`, `track: python-engineering`, `artifact_type: learn`, `status: draft`, `last_verified`. Принятая метамодель требует: ID формата `<owner>.<kind>.<slug>` (`governance/architecture/metamodel/identifiers.md:23-41`), поле `kind` вместо `artifact_type`, статус `drafting` — прямо оговорено «В канонических metadata используется `drafting`, не `draft`» (`governance/architecture/metamodel/metadata.md:147`), freshness наследуется от Module baseline с artifact-level override (`governance/architecture/metamodel/metadata.md:74`).
- **impact:** M0-документ со статусом `accepted` демонстрирует устаревший контракт метаданных. Авторы следующих пакетов (M1.5 thin slice) могут скопировать неканонический пример, что породит невалидные front matter в первом же контенте.
- **recommendation:** Привести пример в `docs/06` к каноническому виду `governance/architecture/metamodel/metadata.md` (ID `b1.learn.<slug>`, `kind`, `status: drafting`, ссылка на Module freshness baseline) или заменить inline-пример ссылкой на метамодель.

### F-02 — major

- **artifact:** `governance/architecture/information-architecture.md`
- **evidence:** Zoom-модель (строки 11–21) описывает `Program → Domain → Vertical track → Module / capability → Atomic topic`: присутствует слой `Domain`, отсутствует `Cluster`. В `governance/planning/execution-plan.md:39` zoom определён как `program → track → cluster → capability → topic → artifact`; сущности `Domain` в метамодели нет (`governance/architecture/metamodel/entities.md`), а `Cluster` — обязательная навигационная группа с cardinality `Track содержит 1..N clusters` (`governance/architecture/metamodel/relationships-and-invariants.md:31`).
- **impact:** Два accepted-документа фиксируют разные zoom-иерархии. Неоднозначность уровня навигации — это именно тот класс проблем, который G1 должен был исключить; индексы будущих репозиториев не смогут следовать обеим моделям одновременно.
- **recommendation:** Синхронизировать zoom в `docs/06` с execution plan/метамоделью; если слой Domain нужен как чисто навигационный, либо явно ввести его в метамодель, либо удалить из zoom-схемы.

### F-03 — minor

- **artifact:** `curriculum/program/diagnostic-and-routing.md`
- **evidence:** Шаг 1 (строки 36–41) перечисляет шесть ролевых представлений, а строка 43 утверждает «Готовые role views входят в программу». Фактически в `routes/` существуют только два (Backend / Distributed Systems, Architecture / Technical Leadership); governance/state/STATUS.md честно помечает оба как `Draft`. Семейство Python Developer по D-028 ещё не формализовано.
- **impact:** Читатель, следуя диагностике, запросит несуществующие артефакты; формулировка создаёт ложное ожидание о готовности.
- **recommendation:** Пометить четыре отсутствующих role view как planned со ссылкой на порядок появления (OPEN-QUESTIONS п.6), либо смягчить формулировку до «по мере публикации».

### F-04 — minor

- **artifact:** `governance/registry/repositories.yaml`
- **evidence:** Реестр содержит только `ela`, `b2`, `b3` (последние два — `status: planned`). При этом `matrix/`, `routes/` и `curriculum/tracks/b2/` ссылаются на все 15 треков как на владельцев capabilities, и контракт cross-repository reference (`governance/architecture/metamodel/identifiers.md:81-89`) требует, чтобы поле `repository` содержало ID записи из этого реестра.
- **impact:** Для 13 из 15 треков cross-repository ссылки сейчас неразрешимы по контракту; при старте M2 (трек B5) потребуется внеплановая правка реестра.
- **recommendation:** Зарегистрировать все 15 треков со `status: planned` — это не создаёт репозитории, но делает реестр полным источником ID.

### F-05 — minor

- **artifact:** `governance/architecture/metamodel/identifiers.md`, `governance/architecture/metamodel/metadata.md`
- **evidence:** Поле `repository` перегружено: в cross-repository reference это ID записи из глобального реестра (`identifiers.md:83-87`, «URL не выводится из naming convention»), а в примере ImplementationReference — внешний URL (`metadata.md:130`: `repository: https://github.com/example/reliable-api`).
- **impact:** Одноимённые поля с разной семантикой в соседних документах метамодели; при появлении формального validator (запланирован после двух slices) это станет конфликтом схемы.
- **recommendation:** Переименовать одно из полей, например `repository` → `external_url`/`locator` в ImplementationReference, зафиксировав решение в governance/decisions.md.

### F-06 — minor

- **artifact:** `curriculum/program/diagnostic-and-routing.md`, `governance/state/OPEN-QUESTIONS.md`
- **evidence:** Шаг 4 требует: «Все обязательные core-компетенции доводятся минимум до установленного baseline» (строка 70), но состав core и baseline нигде не определён — это прямо признано открытым вопросом №5 в `governance/state/OPEN-QUESTIONS.md:24`.
- **impact:** Маршрутизация ссылается на несуществующий норматив; для self-study читателя правило невыполнимо до определения core.
- **recommendation:** До закрытия вопроса №5 заменить нормативную формулировку на рекомендательную («core-компетенции определяются role view по мере их публикации») либо явно связать текст с открытым вопросом.

### F-07 — note

- **artifact:** `curriculum/program/diagnostic-and-routing.md`
- **evidence:** В рабочем шаблоне самооценки названия треков сокращены относительно канонических: «B4 Data Engineering & Analytics» против «Data Engineering & Analytical Platforms» (`curriculum/program/track-map.md:39`), «B7 Reliability & Production Engineering» против «Reliability, Observability & Production Engineering» (`curriculum/program/track-map.md:51`).
- **impact:** Косметический дрейф названий; риск рассинхронизации при поиске/автоматической сверке.
- **recommendation:** Использовать в шаблоне точные названия из track map.

### F-08 — note

- **artifact:** `curriculum/program/level-model.md`
- **evidence:** Строка 18: «Expert / Distinguished*» — звёздочка сноски не имеет соответствующего определения в документе.
- **impact:** Незакрытая отсылка; читатель не понимает, что маркирует `*` (вероятно, необязательность L6, но это сказано отдельным предложением).
- **recommendation:** Убрать `*` или добавить сноску.

### F-09 — major

- **artifact:** `curriculum/tracks/catalog/b11-mlops-llmops.md:34`
- **evidence:** `b11.cluster.lmflow-workflows` описан как «orchestration, lineage, reproducibility и lifecycle integration через LMFlow; model/adaptation semantics остаются в B9». LMFlow (OptimalScale/LMFlow) — toolkit для fine-tuning и inference LLM, а не инструмент orchestration/lineage/lifecycle; описание соответствует скорее Metaflow/ZenML. Внутреннее противоречие: инструмент именно для adaptation помещён в B11 с несвойственной ролью, а его собственная семантика вынесена в B9. Исправление внесено по результатам G2 (`governance/reviews/M1.2-G2.md`), то есть ошибка закреплена accepted-решением.
- **impact:** Учащийся получит неверную ментальную модель инструмента; при детализации B11 кластер придётся перепроектировать.
- **recommendation:** Переформулировать кластер как LLM fine-tuning/inference workflows через LMFlow с явной границей к B9 (model semantics), либо заменить инструмент, если имелась в виду lifecycle-оркестрация; зафиксировать в governance/decisions.md.

### F-10 — major

- **artifact:** `curriculum/tracks/catalog/b2-backend-api.md:26-35` vs `curriculum/tracks/catalog/b5-distributed-systems.md:33`, `governance/decisions.md` (D-032)
- **evidence:** В карточке B2 нет ни одного cluster про caching и API abuse/rate limiting; `b5.cluster.caching-load-control — caching, rate limiting, load shedding и backpressure` забирает и механизмы, и де-факто применение. При этом D-032 (2026-08-15) постановляет: «B2 владеет применением cache и API abuse/security controls на service boundary», и blueprint B2 уже содержит capabilities `integrate-application-caching` и `enforce-api-security-abuse-controls`. Дополнительно backpressure дублируется в B2 и B5 без disclaimer.
- **impact:** Skeleton matrix B2 противоречит более позднему accepted-решению и пилотному blueprint; прикладной ownership в глобальной матрице отсутствует, детализация B5 может занять чужую область.
- **recommendation:** Добавить в B2 cluster/строку In scope про применение кэша и throttling/abuse controls на границе сервиса; в Non-goals B2/B5 взаимно зафиксировать «механизмы и теория — B5, применение в сервисе — B2».

### F-11 — minor

- **artifact:** `curriculum/tracks/catalog/a3-networks-linux-security.md:34` vs `curriculum/tracks/catalog/b6-platform-cloud.md:34`
- **evidence:** `a3.cluster.supply-chain-security` (dependencies, artifacts, provenance, vulnerability handling) и `b6.cluster.supply-chain` (artifact provenance, scanning, signing, admission controls) почти совпадают; Non-goals обоих треков не разграничивают supply chain.
- **impact:** Неоднозначный ownership supply chain security (baseline vs platform-enforcement), риск дублирования материала.
- **recommendation:** Перекрёстные Non-goals: в A3 «platform/admission enforcement — B6», в B6 «security baseline и threat model — A3».

### F-12 — minor

- **artifact:** `curriculum/tracks/catalog/b3-transactional-data.md:34` vs `curriculum/tracks/catalog/b7-reliability-production.md:32`
- **evidence:** `b3.cluster.backup-restore-dr` (backup, restore, PITR, disaster recovery) и `b7.cluster.dr-continuity` (RTO/RPO, backup validation, continuity exercises) пересекаются; взаимных Non-goals нет.
- **impact:** Дублирование DR/backup ownership (store-level механика vs org-level continuity не разведены).
- **recommendation:** Зафиксировать границу «механика backup/PITR конкретного store — B3; RTO/RPO-стратегия и continuity-упражнения — B7» в Non-goals обоих треков.

### F-13 — minor

- **artifact:** `curriculum/tracks/catalog/b2-backend-api.md:35` vs `curriculum/tracks/catalog/b6-platform-cloud.md:31`, `curriculum/tracks/catalog/b7-reliability-production.md:33`
- **evidence:** `b2.cluster.evolution-delivery` (migrations, rollout, backward compatibility, deprecation) пересекается с `b6.cluster.delivery-strategies` (CI/CD integration, rollout, rollback, promotion) и `b7.cluster.production-readiness` (readiness reviews, change safety, release risk); взаимных disclaimers нет.
- **impact:** rollout/release/change safety упоминаются в трёх треках; без разграничения «контрактная эволюция сервиса / инфраструктурный delivery / операционный risk gate» границы размоются при детализации.
- **recommendation:** В Non-goals B2 добавить «deployment/rollout mechanics — B6, release risk/change safety — B7».

### F-14 — note

- **artifact:** `curriculum/tracks/catalog/` (a1, a2, a3, b1, b8, b9 и др.)
- **evidence:** Раздел `Conditional prerequisites` присутствует только в 9 из 15 файлов; в остальных 6 опущен полностью, тогда как пустой `Hard baseline prerequisites` оформлен явным «Нет».
- **impact:** Контракт README это допускает, но читатель не отличает «нет условных зависимостей» от «раздел забыли».
- **recommendation:** Писать «Нет» в пустых Conditional prerequisites либо зафиксировать в контракте, что отсутствие раздела = отсутствие зависимостей.

### F-15 — note

- **artifact:** `curriculum/tracks/catalog/b11-mlops-llmops.md:50-52`, `curriculum/tracks/catalog/a1-computer-science.md:40-42`
- **evidence:** Strong connections B11 — только «B2, B5, C1», хотя B6, B7 и B10 объявляют B11 своей strong connection (несимметрично); A1 перечисляет B3, но не B4, хотя B4 имеет hard prerequisite на A1.
- **impact:** Навигационная асимметрия графа связей; треки выглядят изолированнее, чем есть.
- **recommendation:** Симметризовать strong connections либо зафиксировать в контракте, что prerequisite-связи не дублируются в strong connections.

### F-16 — note

- **artifact:** `curriculum/roles/role-summary.md:12`
- **evidence:** «После M1.4 authoritative требования будут ссылаться на LevelOutcomes» — шкала L1–L5 и LevelOutcomes в `matrix/` не определены; ссылка на `curriculum/program/level-model.md` отсутствует.
- **impact:** Summary-уровни в матрице непроверяемы без внешней легенды.
- **recommendation:** Добавить в `curriculum/tracks/README.md` ссылку на модель уровней.

### F-17 — minor

- **artifact:** `curriculum/tracks/b2/coverage-map.md`, `curriculum/tracks/b2/scenarios.md`
- **evidence:** S14 (scenarios.md:19) объявляет основными capabilities `enforce-api-security-abuse-controls`, `control-service-load-resources`, `integrate-identity-access-control`, но в coverage-map колонка «Primary scenarios» для `control-service-load-resources` — только S08/S13, для `integrate-identity-access-control` — только S05. Аналогично S15 называет `manage-application-transaction-boundaries` и `control-service-load-resources`, чьи строки ссылаются только на S07 и S08/S13.
- **impact:** Двусторонний обход capability→scenario неполон; при материализации в track repository часть связей потеряется, если генерировать edges только из coverage-map.
- **recommendation:** Добавить S14/S15 в соответствующие строки coverage-map либо явно указать, что колонка «Primary scenarios» не обязана быть симметричной «основным capabilities» сценария.

### F-18 — minor

- **artifact:** `curriculum/tracks/b2/scenarios.md`, `curriculum/tracks/b2/README.md`
- **evidence:** README.md:46 требует «relationship target всегда записывается полным semantic ID», но колонка «Module» в scenarios.md содержит plain labels («HTTP service runtime», «Evolvable API contracts»…), а не `b2.module.*`. Дополнительно S05 использует «Identity-aware boundaries», а S14 — «Identity/API security boundaries» при одном и том же модуле; строки S14/S15 вставлены между S05/S06 и S07/S08 без упорядочивания.
- **impact:** Противоречие собственному правилу сериализации M1.4; риск рассинхронизации при материализации.
- **recommendation:** Заменить labels на полные `b2.module.*` ID, унифицировать название identity-модуля, упорядочить строки.

### F-19 — minor

- **artifact:** `curriculum/tracks/b2/level-outcomes.md`
- **evidence:** Отсутствие L5 мотивировано отдельной секцией (строки 182–184) — это хорошо. Но L1 отсутствует без пояснения у 5 capabilities (integrate-application-caching, design-idempotent-service-operations, design-asynchronous-workflows, diagnose-service-performance, control-service-load-resources), а L4 — у trace-request-execution и manage-application-transaction-boundaries.
- **impact:** Reviewer/learner не отличает осознанный пропуск уровня от недоработки; сами формулировки уровней модели L1–L4 при этом соответствуют, искусственного заполнения нет.
- **recommendation:** Добавить пояснение по аналогии с секцией про L5 — одной строкой на capability с пропущенным уровнем.

### F-20 — note

- **artifact:** `curriculum/tracks/b2/role-requirements.md`
- **evidence:** Backend role (строки 21, 34) требует `evolve-api-contracts-l4-...` и `deliver-service-changes-safely-l4-...`, не включая их L3-variants; Architecture role (строка 46) требует `design-http-api-contracts-l4` без L3. Правило «L4 включает L3» нигде не зафиксировано.
- **impact:** Формально список required outcomes неполон относительно собственного L3 baseline; на практике читается как подразумеваемая иерархия.
- **recommendation:** Зафиксировать в interpretive guardrails, что required L4 подразумевает нижележащие уровни той же capability.

### F-21 — note

- **artifact:** `curriculum/tracks/b2/capabilities.md`, `curriculum/tracks/b2/modules.md`
- **evidence:** `b2.capability.evolve-api-contracts`: primary cluster `b2.cluster.evolution-delivery` (primary module кластера — `safe-service-evolution`), но primary module самой capability — `evolvable-api-contracts`. Аналогично `control-concurrency-cancellation` и `integrate-external-services`.
- **impact:** Формально разрешено («modules — не синонимы clusters»), но двойная primary-принадлежность без пояснения запутывает навигацию.
- **recommendation:** Одной строкой в README пояснить, что primary module capability не обязан совпадать с primary module её cluster.

### F-22 — note

- **artifact:** `curriculum/tracks/b2/README.md`, `curriculum/tracks/b2/*.md`, `curriculum/roles/README.md`
- **evidence:** (а) `curriculum/tracks/b2/README.md:42` объявляет file-level default `status: review`, тогда как frontmatter всех каталогов содержит `status: accepted` — неясно, к чему относится default; (б) `curriculum/roles/README.md` — единственный файл без `language: ru` в frontmatter.
- **impact:** Косметическая неоднородность metadata.
- **recommendation:** Уточнить формулировку defaults; выровнять frontmatter.

## Сводка

| Severity | Количество | Findings |
|---|---|---|
| blocker | 0 | — |
| major | 4 | F-01, F-02, F-09, F-10 |
| minor | 10 | F-03, F-04, F-05, F-06, F-11, F-12, F-13, F-17, F-18, F-19 |
| note | 8 | F-07, F-08, F-14, F-15, F-16, F-20, F-21, F-22 |

Обоснование verdict `accepted_with_changes`: блокеров нет, механические проверки (количества, ссылки, ацикличность DAG, покрытие технологий) проходят. Но четыре major — устаревшие примеры контрактов в `docs/06` (F-01, F-02), фактически неверное описание LMFlow (F-09) и отставание skeleton matrix B2 от решения D-032 (F-10) — по правилам `authoring/workflow/review-protocol.md` должны быть исправлены до acceptance либо оформлены явным решением. Рекомендуется закрыть их до старта M1.5, поскольку именно эти документы служат шаблонами для следующих work packages.

## Что проверено и подтверждено без замечаний

- Все Markdown-ссылки из `README.md` (карта документов) разрешаются в существующие файлы.
- `governance/decisions.md` (D-001–D-032) согласован с governance/state/STATUS.md и содержимым пакетов M1.1–M1.4; решения D-026, D-027, D-032 отражены в соответствующих артефактах.
- Review-записи M1.1–M1.4 содержат scope, findings и итоги в формате `authoring/workflow/review-protocol.md`; заявленные исправления присутствуют в артефактах.
- Статусная модель метамодели (`proposed → … → maintenance`, `needs-update`, `superseded`) единообразна между `docs/06` и `governance/architecture/metamodel/metadata.md`.
- **Skeleton matrix:** фактическое число clusters = 155, точно совпадает с заявленным (A1–A3: 9+9+9, B1–B11: 10+10+11+10+11+10+10+10+11+12+11, C1: 12); все треки в пределах контракта 5–12. Все исходно названные технологии (FastAPI, PostgreSQL, Spark, Airflow, BigQuery/Snowflake, PyTorch, Hugging Face, FAISS/Pinecone, LangChain, MLflow, LMFlow, Kubeflow) покрыты clusters соответствующих треков. Висячих ссылок на несуществующие треки и циклов в hard prerequisites нет. Структура карточек единообразна.
- **Pilot B2:** пересчёт подтверждает 10 modules, 19 capabilities, 69 LevelOutcomes (12×4 + 7×3); clusters covered 10/10. Все ссылки замкнуты: capability IDs из coverage-map определены, все ~50 ссылок `b2.level-outcome.*` из coverage-map и 43 ссылки из role-requirements существуют, primary modules/clusters валидны, все scenario labels S01–S15 определены, internal hard-prerequisite DAG ацикличен, якорные ссылки из `routes/` резолвятся, фантомных треков/ролей нет.
- Сценарий S03 соответствует первому slice M1.3 (эволюция API-контракта), контрастный slice покрыт S08 с support S02/S13; у всех 15 сценариев заполнены module, рабочий сценарий, interview probe и capabilities.
- Предметная корректность B2: формулировки про transaction boundaries, dual-write commit/publish windows (S07), SSRF через callback URL (S14), cache stampede/cross-tenant leakage (S15), asyncio cleanup guardrails, queueing-эффект p99 (S12) корректны; устаревших практик не выявлено.
- Политика «L5 не заполняется искусственно» соблюдена и объяснена отдельной секцией в `curriculum/tracks/b2/level-outcomes.md`.
