---
id: ela.review.consolidated-external
kind: review
status: published
updated: 2026-08-15
language: ru
sources:
  - governance/reviews/external-review-glm.md (glm-5.2, 16 findings)
  - governance/reviews/external-review-kimi.md (kimi, 22 findings)
verdict: accepted_with_changes
---

# Консолидированное внешнее review — Engineering Leadership & Architecture Blueprint

## Назначение и метод

Документ объединяет два независимых внешних review пакета `engineering-leadership-architecture-blueprint` (состояние M0 + M1.1–M1.4, все артефакты accepted на 2026-08-15):

- **GLM** (`governance/reviews/external-review-glm.md`, модель glm-5.2) — 16 findings;
- **Kimi** (`governance/reviews/external-review-kimi.md`, модель kimi) — 22 findings.

Метод консолидации:

1. каждый уникальный finding обоих reviewers перепроверен по исходным файлам пакета напрямую (не по тексту чужого review);
2. дубликаты объединены (12 пересечений, см. приложении);
3. расхождения severity разрешены adjudication с приведением обоснования;
4. формулировки evidence/impact/recommendation сохранены от более сильного варианта.

Оба reviewers не редактировали проверяемые файлы; настоящая консолидация также не вносила правок в пакет.

## Scope (общий для обоих reviews)

Весь репозиторий: корневые governance-документы (`README`, `STATUS`, `DECISIONS`, `OPEN-QUESTIONS`, `EXECUTION-PLAN`, `REVIEW-PROTOCOL`), `docs/01`–`docs/08`, `governance/architecture/metamodel/*`, `governance/registry/*.yaml`, `matrix/*` (15 карточек треков), `routes/*`, `pilot/M1.3` и `curriculum/tracks/b2/*`, `governance/reviews/M1.1–M1.4` (как история решений). Роли: structure + domain + learning/interview.

## Verdict

**accepted_with_changes**

```text
blocker: 0
major: 4   (C-01 … C-04)
minor: 13  (C-05 … C-17)
note: 9    (C-18 … C-26)
```

Условие принятия: четыре major закрыты до старта M1.5 — все четыре находятся в документах, которые служат шаблонами/контрактами для следующих work packages.

## Подтверждённые механические проверки (обоими reviewers, сверены независимо)

| Проверка | Результат |
|---|---|
| Clusters в skeleton A1–C1 | 155 — совпадает с заявленным в STATUS |
| Modules / Capabilities / LevelOutcomes B2 | 10 / 19 / 69 — совпадает (12×4 + 7×3 outcomes) |
| Internal hard-prerequisite DAG B2 | ацикличен; 11 edges, 8 корней |
| L4-outcomes B2: обязательные + conditional | 5 + 12 = 17 — полное множество, потерь нет |
| Primary module capability ∈ develops этого module | 19/19 |
| Semantic references (capabilities, level-outcomes, якоря routes) | битых ссылок нет |
| Сценарии S01–S15 | все определены и используются |
| Технологии из track map | все покрыты clusters соответствующих треков |
| Предметная корректность B2-модели | устаревших практик и фактических ошибок не выявлено |
| DECISIONS D-001–D-032 ↔ STATUS ↔ артефакты | согласованы, кроме отставания skeleton B2 от D-032 (→ C-04) |

## Major findings

### C-01 — docs/06: устаревший пример метаданных противоречит принятой метамодели

- severity: **major** (GLM №1 + Kimi F-01)
- artifact: `governance/architecture/information-architecture.md` (раздел «Метаданные атомарного артефакта») против `governance/architecture/metamodel/identifiers.md`, `governance/architecture/metamodel/metadata.md`
- evidence: пример использует `id: py-iter-001`, `track: python-engineering`, `module: iteration`, `artifact_type: learn`, `status: draft`. Метамодель (accepted на день позже, 2026-08-14) требует ID `<owner>.<kind>.<slug>` (например `b1.learn.<slug>`), поле `kind`, `owner_track`, `language`, статус `drafting` («В канонических metadata используется `drafting`, не `draft`»), freshness от Module baseline с artifact-override.
- impact: два accepted-документа конфликтуют как source of truth. Автор M1.5, скопировавший шаблон из docs/06, создаст невалидные front matter в первом же контенте.
- recommendation: привести пример к каноническому виду `governance/architecture/metamodel/metadata.md` или заменить inline-пример ссылкой на метамодель. До M1.5.

### C-02 — docs/06: zoom-модель расходится с принятой иерархией (лишний Domain, отсутствует Cluster)

- severity: **major** (GLM №2 minor + Kimi F-02 major; повышено до major)
- artifact: `governance/architecture/information-architecture.md` (zoom-модель) против `governance/architecture/metamodel/entities.md`, `governance/architecture/metamodel/relationships-and-invariants.md`, `governance/planning/execution-plan.md`
- evidence: docs/06 описывает `Program → Domain → Vertical track → Module/capability → Atomic topic`: слой `Domain` в метамодели отсутствует, а обязательный `Cluster` (Track содержит 1..N clusters) в схеме пропущен. EXECUTION-PLAN определяет zoom как `program → track → cluster → capability → topic → artifact`.
- impact: два accepted-документа фиксируют разные навигационные иерархии — ровно тот класс неоднозначности, который G1 должен был исключить; индексы track-repository не смогут следовать обеим моделям.
- recommendation: синхронизировать zoom в docs/06 с метамоделью/execution plan. Если слой Domain желателен как чисто навигационная группировка — либо явно ввести его в метамодель, либо удалить. Можно одной правкой с C-01.
- adjudication: GLM классифицировал как minor (staleness), Kimi — major (конфликт двух accepted-контрактов навигации). Принята оценка major: противоречие структурного контракта, а не только примера.

### C-03 — B11: фактическая ошибка в описании LMFlow, закреплённая accepted-решением G2

- severity: **major** (Kimi F-09 + GLM №14 note; повышено до major)
- artifact: `curriculum/tracks/catalog/b11-mlops-llmops.md` (кластер `b11.cluster.lmflow-workflows`), `governance/decisions.md` (D-005), `governance/reviews/M1.2-G2.md`
- evidence: кластер описан как «orchestration, lineage, reproducibility и lifecycle integration через LMFlow». LMFlow (OptimalScale/LMFlow) — toolkit для fine-tuning и inference LLM, а не оркестратор lifecycle; описание соответствует скорее классу Metaflow/ZenML. Внутреннее противоречие: инструмент именно для adaptation помещён в B11 с несвойственной ролью, а его собственная семантика вынесена в B9. Формулировка внесена по итогам G2, т.е. ошибка зафиксирована accepted-изменением.
- impact: неверная ментальная модель инструмента у учащегося; при детализации B11 кластер придётся перепроектировать; нишевый инструмент якорит весь кластер.
- recommendation: переформулировать кластер как «LLM fine-tuning/inference workflows через LMFlow» с явной границей к B9 (model semantics), либо заменить инструмент, если требовалась lifecycle-оркестрация; проверить maintenance-статус LMFlow; зафиксировать изменение в governance/decisions.md.
- adjudication: GLM ограничился note (нишевость инструмента), Kimi указал на фактическую ошибку в описании. Принята оценка major: предметная ошибка в accepted-артефакте.

### C-04 — Skeleton matrix B2 отстала от решения D-032 (кэш и API abuse controls)

- severity: **major** (Kimi F-10; GLM не обнаружил)
- artifact: `curriculum/tracks/catalog/b2-backend-api.md` против `curriculum/tracks/catalog/b5-distributed-systems.md`, `governance/decisions.md` (D-032), `curriculum/tracks/b2/capabilities.md`
- evidence: D-032 (2026-08-15) постановляет «B2 владеет применением cache и API abuse/security controls на service boundary»; blueprint B2 уже содержит `integrate-application-caching` и `enforce-api-security-abuse-controls`. При этом карточка B2 в skeleton (accepted 2026-08-14, не обновлялась) не упоминает применение кэша и abuse/throttling ни в In scope, ни в Non-goals, а `b5.cluster.caching-load-control` («caching, rate limiting, load shedding и backpressure») выглядит владельцем и механизмов, и применения. Backpressure дополнительно присутствует в B2 (`performance-resource-control`) без disclaimer.
- impact: skeleton-карточка противоречит более позднему принятому решению и пилотному blueprint; при детализации B5 (M2) есть риск занять прикладную область B2.
- recommendation: обновить карточку B2 — добавить в In scope применение кэша и throttling/abuse controls на границе сервиса; в Non-goals B2/B5 взаимно зафиксировать «механизмы и теория — B5, применение в сервисе — B2». Новые кластеры не обязательны: пилотные capabilities уже размещены в существующих кластерах (`persistence-transactions`, `identity-access-boundaries`).

## Minor findings

### C-05 — docs/07 обещает шесть готовых role views, существуют два

- severity: minor (Kimi F-03)
- artifact: `curriculum/program/diagnostic-and-routing.md`
- evidence: шаг 1 перечисляет шесть ролевых представлений, текст утверждает «Готовые role views входят в программу». Фактически в `routes/` два draft-представления; семейство Python Developer по D-028 не формализовано.
- impact: читатель запросит несуществующие артефакты.
- recommendation: пометить отсутствующие role views как planned со ссылкой на порядок появления (OPEN-QUESTIONS п.6) либо смягчить формулировку.

### C-06 — governance/registry/repositories.yaml неполон и рассинхронизирован

- severity: minor (GLM №3 + Kimi F-04)
- artifact: `governance/registry/repositories.yaml`
- evidence: содержит только `ela`, `b2`, `b3` (planned); присутствие b3 нигде не мотивировано. Контракт cross-repository reference требует `repository` = ID из этого реестра — для 13 из 15 треков ссылки неразрешимы. Обновлён 2026-08-14, до принятия blueprint B2 (G3).
- impact: реестр — заявленный единственный authoritative источник ID репозиториев; его неполнота блокирует контракт ссылок; внеплановая правка потребуется уже на M2 (B5).
- recommendation: зарегистрировать все 15 треков со `status: planned` (создания репозиториев это не требует) и синхронизировать записи b2/b3 с D-029/D-031; зафиксировать policy наполнения.

### C-07 — коллизия семантики поля `repository` в метамодели

- severity: minor (GLM №6 + Kimi F-05)
- artifact: `governance/architecture/metamodel/metadata.md` (пример ImplementationReference) против `governance/architecture/metamodel/identifiers.md`
- evidence: в cross-repository reference `repository` — ID записи глобального реестра («URL не выводится»); в ImplementationReference то же поле содержит внешний URL.
- impact: одно имя — две семантики; при появлении validator (D-024) станет конфликтом схемы.
- recommendation: переименовать поле в ImplementationReference (`locator`/`external_url`), оставив `repository` для registry ID; зафиксировать в governance/decisions.md.

### C-08 — docs/07 ссылается на неопределённый норматив core-baseline

- severity: minor (Kimi F-06)
- artifact: `curriculum/program/diagnostic-and-routing.md` против `governance/state/OPEN-QUESTIONS.md` (п.5)
- evidence: «Все обязательные core-компетенции доводятся минимум до установленного baseline» — состав core и baseline не определён, что прямо признано открытым вопросом.
- impact: правило невыполнимо до закрытия вопроса.
- recommendation: до закрытия вопроса заменить нормативную формулировку на рекомендательную либо явно связать с открытым вопросом.

### C-09 — перекрытие supply chain security: A3 vs B6

- severity: minor (Kimi F-11)
- artifact: `curriculum/tracks/catalog/a3-networks-linux-security.md` (`a3.cluster.supply-chain-security`) vs `curriculum/tracks/catalog/b6-platform-cloud.md` (`b6.cluster.supply-chain`)
- evidence: кластеры почти совпадают по формулировке; взаимных Non-goals нет.
- impact: неоднозначный ownership (security baseline vs platform enforcement), риск дублирования материала.
- recommendation: перекрёстные Non-goals: в A3 «platform/admission enforcement — B6», в B6 «security baseline и threat model — A3».

### C-10 — перекрытие DR/backup: B3 vs B7

- severity: minor (Kimi F-12)
- artifact: `curriculum/tracks/catalog/b3-transactional-data.md` (`b3.cluster.backup-restore-dr`) vs `curriculum/tracks/catalog/b7-reliability-production.md` (`b7.cluster.dr-continuity`)
- evidence: кластеры пересекаются (backup, restore, DR); границы не зафиксированы.
- impact: дублирование ownership без разделения «механика store — B3 / RTO-RPO-стратегия и continuity — B7».
- recommendation: добавить взаимные Non-goals с этой формулировкой границы.

### C-11 — перекрытие rollout/release: B2 vs B6 vs B7

- severity: minor (Kimi F-13; смежно с C-04)
- artifact: `curriculum/tracks/catalog/b2-backend-api.md` (`evolution-delivery`) vs `b6.cluster.delivery-strategies`, `b7.cluster.production-readiness`
- evidence: rollout/release/change safety упоминаются в трёх треках без взаимных disclaimers.
- impact: размывание границ «контрактная эволюция сервиса / инфраструктурный delivery / операционный risk gate» при детализации.
- recommendation: в Non-goals B2 добавить «deployment/rollout mechanics — B6, release risk/change safety — B7» (согласовать с правкой C-04).

### C-12 — несовпадение primary module capability с «primary module» её кластера; таблица Coverage clusters без определённой семантики

- severity: minor (GLM №4 + Kimi F-21 note; консолидировано как minor)
- artifact: `curriculum/tracks/b2/modules.md` (Coverage clusters) против `curriculum/tracks/b2/capabilities.md`
- evidence: для `evolution-delivery` указан primary module `safe-service-evolution`, но `evolve-api-contracts` (primary cluster — этот) имеет primary module `evolvable-api-contracts`; аналогично `async-background-integration` → `background-message-workflows` против `external-service-integration` у двух из трёх capabilities кластера. Метамодель не определяет отношение «cluster → primary module».
- impact: таблица читается как инвариант, которым не является; риск ошибки размещения cluster-indexes при материализации track repository.
- recommendation: переименовать колонку в «Entry/default module» с пояснением в README, что primary module capability не обязан совпадать с primary module её кластера, либо убрать таблицу и выводить размещение из capabilities.

### C-13 — role requirements требуют L4 без заявленной импликации L3

- severity: minor (GLM №5 + Kimi F-20 note; консолидировано как minor)
- artifact: `curriculum/tracks/b2/role-requirements.md`
- evidence: Backend требует `evolve-api-contracts-l4` и `deliver-service-changes-safely-l4` без одноимённых L3; Architecture требует `design-http-api-contracts-l4` без L3. Правило «L4 ⊃ L3» нигде не зафиксировано.
- impact: читатель не может решить, пропуск L3 намеренный или дефект списка; при сверке профиля возникнут ложные пробелы.
- recommendation: добавить guardrail: «required L4 outcome подразумевает соответствующее L3-поведение той же capability; отдельная строка L3 не требуется».

### C-14 — асимметрия scenario ↔ coverage map (S14/S15)

- severity: minor (Kimi F-17; GLM не обнаружил)
- artifact: `curriculum/tracks/b2/coverage-map.md` против `curriculum/tracks/b2/scenarios.md`
- evidence: S14 объявляет основными `control-service-load-resources` и `integrate-identity-access-control`, но их строки coverage-map ссылаются только на S08/S13 и S05; аналогично S15 ↔ `manage-application-transaction-boundaries` (S07) и `control-service-load-resources`.
- impact: обход capability→scenario неполон; при генерации edges из coverage-map часть связей потеряется.
- recommendation: дополнить колонку Primary scenarios (S14/S15) либо явно указать, что колонка не обязана быть симметричной «основным capabilities» сценария.

### C-15 — нарушение собственного правила сериализации в scenarios.md

- severity: minor (Kimi F-18 + GLM №10)
- artifact: `curriculum/tracks/b2/scenarios.md` против `curriculum/tracks/b2/README.md`
- evidence: README требует «relationship target всегда записывается полным semantic ID», но колонка Module содержит plain labels («HTTP service runtime»…); модуль identity назван по-разному в S05 («Identity-aware boundaries») и S14 («Identity/API security boundaries»); строки S14/S15 вставлены между S05–S08 без упорядочивания.
- impact: риск рассинхронизации при материализации; падение сканируемости.
- recommendation: заменить labels на `b2.module.*` ID, унифицировать название identity-модуля, отсортировать строки.

### C-16 — пропущенные уровни (L1/L4) у отдельных capabilities не объяснены

- severity: minor (Kimi F-19)
- artifact: `curriculum/tracks/b2/level-outcomes.md`
- evidence: отсутствие L5 мотивировано отдельной секцией, но L1 отсутствует без пояснения у 5 capabilities (caching, idempotent operations, async workflows, diagnose performance, control load), L4 — у trace-request-execution и manage-application-transaction-boundaries.
- impact: не отличить осознанный пропуск от недоработки.
- recommendation: добавить краткие пояснения по аналогии с секцией про L5 (можно одной строкой на capability).

### C-17 — контрастный slice M1.7 не связан с именем gate G4b

- severity: minor (GLM №8)
- artifact: `governance/planning/execution-plan.md` (M1.7), `governance/state/STATUS.md` против `authoring/workflow/review-protocol.md`
- evidence: REVIEW-PROTOCOL определяет gate `G4b Contrast slice` со своими обязательными reviewers, но идентификатор G4b не встречается нигде вне таблицы протокола.
- impact: риск пропуска обязательного gate при планировании M1.7.
- recommendation: явно вписать «gate G4b» в M1.7 EXECUTION-PLAN и в строку STATUS.

## Notes

### C-18 — раздел Conditional prerequisites отсутствует в 6 из 15 карточек

(GLM №7 + Kimi F-14; по перепроверке — 6 карточек: A1, A2, A3, B1, B8, B9.) Контракт карточки перечисляет его как элемент; читатель не отличит «нет зависимостей» от «забыли». Recommendation: писать «Нет» либо зафиксировать в контракте, что отсутствие раздела = отсутствие зависимостей.

### C-19 — висячая сноска у L6

(GLM №9 + Kimi F-08.) `curriculum/program/level-model.md`: «Expert / Distinguished*» — звёздочка без сноски. Убрать или расшифровать.

### C-20 — дрейф названий треков в пользовательских документах

(GLM №11 + Kimi F-07.) «B4 Data Engineering & Analytics» и «B7 Reliability & Production Engineering» в `docs/07` и `curriculum/roles/backend-distributed-systems.md` против канонических полных названий. Выровнять.

### C-21 — роль `assess` у interview-coverage на L4 при заявленной недоказуемости L4 интервью

(GLM №12.) Coverage-map целят interview-артефакты в L4-outcomes с ролью `assess`, тут же оговаривая, что interview L4 proficiency не доказывает. Оставить с комментарием в coverage entry либо ввести роль вида `probe`.

### C-22 — актуальность TensorFlow/Keras как «второго production framework»

(GLM №13.) К 2026 г. Keras 3 — мультибэкендный фреймворк (jax/tf/torch); при детализации B9 зафиксировать, что именно сравнивается, и проверить по первичным источникам с `last_verified`.

### C-23 — асимметрия strong connections в skeleton

(Kimi F-15.) B11 декларирует связи только «B2, B5, C1», хотя B6/B7/B10 называют B11 своей strong connection; A1 не перечисляет B4 при наличии hard prerequisite B4→A1. Симметризовать либо зафиксировать policy в контракте.

### C-24 — matrix не ссылается на модель уровней

(Kimi F-16.) `curriculum/roles/role-summary.md` использует шкалу L1–L5 без ссылки на `curriculum/program/level-model.md`; добавить ссылку в `curriculum/tracks/README.md`.

### C-25 — routes: предварительные clusters как bullet-списки без semantic IDs

(GLM №15.) Для B2 authoritative-замена уже существует; при следующем zoom заменить bullets на `*.cluster.*` IDs.

### C-26 — мелкая неоднородность metadata пилота и routes

(GLM №16 + Kimi F-22.) (а) defaults агрегата в `curriculum/tracks/b2/README.md` объявляют `status: review`, файлы несут `accepted` — уточнить соответствие статусов work package и encoded entities; (б) `curriculum/roles/README.md` — единственный файл без `language: ru` во frontmatter.

## Приложение: соответствие консолидированных findings исходным

| Consolidated | GLM | Kimi | Примечание adjudication |
|---|---|---|---|
| C-01 | №1 major | F-01 major | полное совпадение |
| C-02 | №2 minor | F-02 major | повышено до major (конфликт контрактов навигации) |
| C-03 | №14 note | F-09 major | повышено до major (предметная ошибка в accepted-артефакте) |
| C-04 | — | F-10 major | подтверждено перепроверкой D-032 ↔ skeleton B2 |
| C-05 | — | F-03 minor | подтверждено |
| C-06 | №3 minor | F-04 minor | объединено |
| C-07 | №6 minor | F-05 minor | объединено |
| C-08 | — | F-06 minor | подтверждено |
| C-09 | — | F-11 minor | подтверждено |
| C-10 | — | F-12 minor | подтверждено |
| C-11 | — | F-13 minor | подтверждено; согласовать с C-04 |
| C-12 | №4 minor | F-21 note | консолидировано как minor |
| C-13 | №5 minor | F-20 note | консолидировано как minor |
| C-14 | — | F-17 minor | подтверждено |
| C-15 | №10 note | F-18 minor | консолидировано как minor (нарушение правила сериализации) |
| C-16 | — | F-19 minor | подтверждено |
| C-17 | №8 minor | — | — |
| C-18 | №7 minor | F-14 note | счёт карточек исправлен: 6 из 15 |
| C-19 | №9 minor | F-08 note | консолидировано как note |
| C-20 | №11 note | F-07 note | объединено; добавлен B7 |
| C-21 | №12 note | — | — |
| C-22 | №13 note | — | — |
| C-23 | — | F-15 note | подтверждено |
| C-24 | — | F-16 note | подтверждено |
| C-25 | №15 note | — | — |
| C-26 | №16 note | F-22 note | объединено |

Итого: 38 исходных findings → 26 консолидированных (12 объединённых пар, 2 повышения severity, 1 понижение, 1 исправление счёта).

## Условия и рекомендуемый порядок закрытия

До M1.5 (блокирует шаблоны контента):

1. **C-01 + C-02** — одна правка `docs/06` (метаданные + zoom);
2. **C-04** — обновить карточку B2 по D-032, попутно закрыв C-11 (Non-goals B2/B5/B6/B7);
3. **C-03** — переформулировать `b11.cluster.lmflow-workflows`, запись в governance/decisions.md.

Ближайший work package (можно вместе с M1.5–M1.6): C-05…C-08 (docs/07, registry, метамодель), C-12…C-17 (пилот B2 — до материализации track repository).

Backlog: C-18…C-26.

## Подтверждённые сильные стороны

1. Внутренняя согласованность выдающаяся для пакета такого размера: все проверяемые численные заявления (155/10/19/69/17) сходятся у обоих reviewers, dangling references отсутствуют.
2. Метамодель решает реальные проблемы дублирования (capability как каноническая единица, RoleView без владения, языковые renditions) и осознанно откладывает формализацию до появления потребителей (D-024).
3. Отказ от искусственного заполнения L5 в B2 и от фиктивных числовых рейтингов при выборе пилота — последовательное сопротивление ложной точности.
4. Governance-цепочка D-001–D-032 + review-протокол с adjudication воспроизводима; findings gate-ревью реально влияют на артефакты.

## Ограничения

Предметная глубина проверена на уровне структуры и формулировок; полноценная domain-проверка содержательной корректности будущих briefs возможна только на G5. Механические проверки выполнены вручную обоими reviewers независимо, без автоматического валидатора (соответствует D-024). Консолидация выполнена агентом GLM на основе обоих артефактов с прямой перепроверкой каждого finding по исходным файлам.
