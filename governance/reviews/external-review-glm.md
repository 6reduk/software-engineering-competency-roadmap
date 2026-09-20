---
id: ela.review.external-glm
kind: review
status: published
updated: 2026-08-15
language: ru
reviewer_model: glm-5.2
review_type: external-independent
scope_package: M0 + M1.1–M1.4 (accepted state as of 2026-08-15)
verdict: accepted_with_changes
---

# External independent review — GLM

Независимое review пакета `engineering-leadership-architecture-blueprint` моделью GLM (glm-5.2), не участвовавшей в авторстве и в предыдущих gate-ревью G1–G3. Проверяемые файлы не изменялись; создан только настоящий артефакт.

## Scope

Все 60 файлов репозитория, прочитанные полностью:

- управляющие: `README.md`, `governance/state/STATUS.md`, `governance/decisions.md`, `governance/state/OPEN-QUESTIONS.md`, `governance/planning/execution-plan.md`, `authoring/workflow/review-protocol.md`;
- `docs/01`–`docs/08`;
- `governance/architecture/metamodel/*` (entities, relationships-and-invariants, identifiers, metadata, README) и `governance/registry/*.yaml`;
- `curriculum/tracks/README.md`, `curriculum/roles/role-summary.md`, все 15 карточек `curriculum/tracks/catalog/a1..c1`;
- `curriculum/roles/README.md`, `curriculum/roles/backend-distributed-systems.md`, `curriculum/roles/architecture-technical-leadership.md`;
- `governance/planning/M1.3-pilot-selection.md` и весь `curriculum/tracks/b2/*` (README, modules, capabilities, level-outcomes, prerequisites, scenarios, coverage-map, role-requirements);
- `governance/reviews/M1.1-G1.md` … `governance/reviews/M1.4-G3.md` — как история решений, не как объект проверки.

Уровень проверки: structure + domain + learning/interview в одном лице (внешний reviewer); механические проверки выполнены вручную.

## Model

- Model: `glm-5.2` (суффикс артефакта `-glm`).
- Дата: 2026-08-15.
- Роль: внешний независимый reviewer по `authoring/workflow/review-protocol.md`; правки проверяемых файлов не вносились.

## Механически перепроверенные инварианты

| Проверка | Результат |
|---|---|
| Кластеров в skeleton A1–C1 | 155 — совпадает с заявленным в STATUS |
| Modules / Capabilities / LevelOutcomes B2 | 10 / 19 / 69 — совпадает |
| Internal hard-prerequisite DAG B2 | ацикличен; 11 edges, 8 корней — совпадает со списком |
| L4-outcomes B2: обязательные + conditional | 5 + 12 = 17 = полное множество L4 — потерь нет |
| Primary module каждой capability ∈ develops этого module | 19/19 ✓ |
| Сценарии S01–S15 ↔ coverage map | все 15 использованы, висячих нет |
| Разбиение L1–L5 по уровням (без искусственного заполнения) | выдержано: capabilities без L1 и/или L5 объяснимы |

## Findings

### 1. Major — устаревший пример метаданных в docs/06 противоречит принятой метамодели

- severity: major
- artifact: `governance/architecture/information-architecture.md` (раздел «Метаданные атомарного артефакта») против `governance/architecture/metamodel/identifiers.md`, `governance/architecture/metamodel/metadata.md`
- criterion: correctness / structure
- evidence: docs/06 датирован 2026-08-13 (до M1.1) и приводит шаблон `id: py-iter-001`, `track: python-engineering`, `module: iteration`, `artifact_type: learn`, `levels: [L1, L2, L3]` без `kind`, `owner_track`, `language`. Метамодель (accepted 2026-08-14, D-023/D-024) требует `id` формата `<owner>.<kind>.<slug>` (например `b1.learn.<slug>`), поля `kind`, `owner_track`, `language` и статус `drafting` вместо `draft`.
- impact: два документа со статусом accepted конфликтуют как source of truth. Автор track-repository, берущий шаблон из docs/06, создаст артефакты, не соответствующие метамодели; рассинхронизация проявится на M1.5/M1.6 при материализации сущностей B2.
- recommendation: привести пример в docs/06 к конформному метамодельному виду (или явно пометить раздел как superseded со ссылкой на `governance/architecture/metamodel/metadata.md`). Минимальная правка, до M1.5.

### 2. Minor — «Zoom-модель» в docs/06 вводит слой Domain, не используемый в остальном пакете

- severity: minor
- artifact: `governance/architecture/information-architecture.md`
- criterion: structure
- evidence: zoom-модель содержит `Domain (foundation / engineering / data-ml / leadership)`, тогда как skeleton matrix (`curriculum/tracks/README.md`) использует группы Foundation / Technical verticals / Integration, и нигде больше слой Domain не появляется.
- impact: двусмысленная навигационная таксономия; при создании индексов track-repository неясно, какой уровень считать каноническим.
- recommendation: синхронизировать пример с фактической группировкой skeleton или удалить слой Domain из схемы (можно вместе с правкой finding 1).

### 3. Minor — governance/registry/repositories.yaml несинхронизирован и содержит необъяснённую запись b3

- severity: minor
- artifact: `governance/registry/repositories.yaml`
- criterion: structure / freshness
- evidence: файл обновлён 2026-08-14 и содержит только `ela`, `b2` (planned), `b3` (planned). Нет ни одной другой вертикали; присутствие b3 нигде не мотивировано (D-029/D-031 относятся к b2). На 2026-08-15 blueprint B2 принят (G3 passed), а запись b2 осталась `planned` без поля даты/статуса решения.
- impact: реестр — контракт cross-repository ссылок (`identifiers.md`); его drift от STATUS/DECISIONS подрывает заявленную «единственную authoritative» роль.
- recommendation: зафиксировать policy наполнения (например, только репозитории, готовые к созданию) и синхронизировать записи с D-029/D-031; либо удалить b3 до появления причины.

### 4. Minor — таблица «Coverage clusters» в modules.md конфликтует с primary modulescapabilities и использует неопределённую семантику

- severity: minor
- artifact: `curriculum/tracks/b2/modules.md` (раздел Coverage clusters) против `curriculum/tracks/b2/capabilities.md`
- criterion: structure
- evidence: для кластера `b2.cluster.evolution-delivery` указан primary module `safe-service-evolution`, но capability `b2.capability.evolve-api-contracts` (primary cluster именно этот) имеет primary module `evolvable-api-contracts`. Аналогично для `b2.cluster.async-background-integration` указан `background-message-workflows`, тогда как `integrate-external-services` и `control-concurrency-cancellation` из этого кластера имеют primary module `external-service-integration`. Метамодель не определяет отношения «cluster → primary module» вообще (модуль — у capability).
- impact: при материализации track-repository и расстановке cluster-indexes возможна ошибка размещения; таблица читается как инвариант, которым не является.
- recommendation: переименовать колонку в «Entry/default module» с пояснением, либо убрать таблицу и выводить размещение из capabilities.md.

### 5. Minor — role requirements требуют L4 без заявленной импликации L3

- severity: minor
- artifact: `curriculum/tracks/b2/role-requirements.md`
- criterion: level
- evidence: в оба списка входят, например, `evolve-api-contracts-l4-lead-cross-team-migration` и `deliver-service-changes-safely-l4-coordinate-cross-team-change`, при этом одноимённые L3-outcomes в required не значатся. Interpretive guardrails не содержат утверждения, что required L4 влечёт соответствующее поведение L3.
- impact: читатель не может решить, является ли пропуск L3 намеренным («сразу L4») или багом списка; при сверке профиля возникнут ложные «пробелы».
- recommendation: добавить один guardrail-пункт: «required L4 outcome подразумевает соответствующее L3-поведение той же capability; отдельная строка L3 не требуется».

### 6. Minor — коллизия имени поля `repository` в метамодели

- severity: minor
- artifact: `governance/architecture/metamodel/metadata.md` (пример ImplementationReference) против `governance/architecture/metamodel/identifiers.md`
- criterion: correctness
- evidence: в identifiers.md поле `repository` в cross-repository reference содержит ID записи из глобального registry (`b3`), и прямо сказано «URL не выводится»; в примере ImplementationReference то же поле содержит внешний URL `https://github.com/example/reliable-api`.
- impact: одно имя поля — две разные семантики (ID внутреннего реестра vs внешний locator); при появлении schema/validator (D-024) конфликт станет формальной ошибкой.
- recommendation: в ImplementationReference переименовать поле во внешний locator (например `url` или `locator`), оставив `repository` только для registry ID.

### 7. Minor — контракт карточки трека требует раздел Conditional prerequisites, который отсутствует в 7 из 15 карточек

- severity: minor
- artifact: `curriculum/tracks/README.md` (контракт карточки) против карточек A1, A2, A3, B1, B8, B9, C1
- criterion: structure
- evidence: контракт перечисляет 7 обязательных элементов, включая «Conditional prerequisites»; для hard baseline явно разрешён пустой список, для conditional такого разрешения нет, но перечисленные карточки раздел просто опускают.
- impact: косметическая неоднородность; будущий механический validator будет выдавать ложные срабатывания.
- recommendation: либо добавить в эти карточки строку «Conditional prerequisites: нет», либо дополнить контракт фразой «раздел опускается, если conditional-зависимостей нет».

### 8. Minor — контрастный slice M1.7 не связан с именем gate G4b

- severity: minor
- artifact: `governance/planning/execution-plan.md` (M1.7), `governance/state/STATUS.md` против `authoring/workflow/review-protocol.md`
- criterion: scope / process
- evidence: REVIEW-PROTOCOL определяет gate `G4b Contrast slice`, но EXECUTION-PLAN M1.7 и STATUS ссылаются только на «критерии»/«следующий пакет», не называя G4b; нигде вне таблицы протокола идентификатор G4b не встречается.
- impact: risk пропуска обязательного gate при планировании M1.7 (в протоколе у G4b свои обязательные reviewers).
- recommendation: в M1.7 EXECUTION-PLAN и в строку STATUS M1.7 (когда появится) явно вписать «gate G4b».

### 9. Minor — висячая сноска в модели уровней

- severity: minor
- artifact: `curriculum/program/level-model.md`
- criterion: structure
- evidence: тег L6 записан как «Expert / Distinguished*» со звёздочкой, но сноски/пояснения к звёздочке в документе нет.
- impact: неясно, что маркирует asterisk (вероятно, необязательность уровня, но это уже сказано в самом тексте строки).
- recommendation: удалить звёздочку или добавить сноску.

### 10. Note — строки сценарной таблицы не отсортированы

- severity: note
- artifact: `curriculum/tracks/b2/scenarios.md`
- criterion: structure
- evidence: S14 и S15 стоят между S07 и S08; остальной пакет строго упорядочен.
- impact: мелкое падение сканируемости; кросс-ссылки из coverage-map корректны, ошибки нет.
- recommendation: при следующей правке отсортировать по S-номеру (или сгруппировать по module сознательно, тогда подписать группировку).

### 11. Note — дрейф названия трека B4

- severity: note
- artifact: `curriculum/program/diagnostic-and-routing.md`, `curriculum/roles/backend-distributed-systems.md`
- criterion: structure
- evidence: используется «B4 Data Engineering & Analytics», каноническое название — «B4 Data Engineering & Analytical Platforms» (`curriculum/tracks/catalog/b4-data-engineering.md`).
- impact: минимальный; поиск по каноническому названию не находит всех упоминаний.
- recommendation: выровнять название при ближайшей правке.

### 12. Note — роль `assess` у interview-coverage на L4-outcomes при заявленной недоказуемости L4 интервью

- severity: note
- artifact: `curriculum/tracks/b2/coverage-map.md`
- criterion: level / practice
- evidence: `b2.interview.api-contract-evolution` и `b2.interview.runtime-resource-failure` целятся в L4-outcomes с coverage role `assess`, при этом тут же сказано, что interview L4 proficiency не доказывает.
- impact: семантическая натяжка: `assess` определён как «проверяет действие или решение». Guardrail-текст спасает, но роль покрытия звучит сильнее принятой интерпретации.
- recommendation: либо оставить с явным комментарием в coverage entry, либо ввести роль вроде `probe` для reasoning-без-execution-evidence.

### 13. Note — актуальность TensorFlow/Keras как «второго production framework»

- severity: note
- artifact: `governance/decisions.md` (D-006), `curriculum/tracks/catalog/b9-deep-learning.md`
- criterion: freshness
- evidence: кластер `b9.cluster.tensorflow-keras` описан как «Keras/TensorFlow comparative workflows». К 2026 г. Keras 3 — мультибэкендный фреймворк (jax/tf/torch), что меняет формулировку «второго framework» и само сравнение с PyTorch.
- impact: при детализации B9 формулировки кластера потребуют уточнения; на уровне skeleton ошибки нет.
- recommendation: при zoom B9 зафиксировать, что сравнивается (Keras 3 API vs PyTorch), и проверить актуальность по первичным источникам с `last_verified`.

### 14. Note — LMFlow как якорь отдельного кластера B11

- severity: note
- artifact: `curriculum/tracks/catalog/b11-mlops-llmops.md`, `governance/decisions.md` (D-005)
- criterion: freshness / scope
- evidence: весь кластер `b11.cluster.lmflow-workflows` привязан к LMFlow — нишевому исследовательскому фреймворку; более распространены альтернативы в каждой из перечисленных обязанностей кластера.
- impact: риск, что кластер окажется перегружен инструментом с ограниченной поддержкой, а устойчивые концепции пострадают при его деградации.
- recommendation: при детализации B11 проверить maintenance-статус и покрытие LMFlow; держать формулировки кластера concept-first (orchestration/lineage/reproducibility), инструмент — как пример, а не якорь.

### 15. Note — role views всё ещё описывают clusters маркированными списками без semantic IDs

- severity: note
- artifact: `curriculum/roles/backend-distributed-systems.md`, `curriculum/roles/architecture-technical-leadership.md`
- criterion: structure
- evidence: разделы «Предварительные competency clusters» — свободные bullet-списки без привязки к `*.cluster.*` ID (для B2 уже существует authoritative замена).
- impact: ожидаемо для draft-статуса; риск задержаться в «предварительности» после принятия B2 role requirements.
- recommendation: при следующем zoom заменить bullets на semantic cluster IDs, как это уже сделано ссылкой на B2 role requirements.

### 16. Note — aggregate defaults пилота объявляют `status: review`, файлы несут `accepted`

- severity: note
- artifact: `curriculum/tracks/b2/README.md` (Aggregate catalog notation) против `curriculum/tracks/b2/*.md`
- criterion: structure / process
- evidence: defaults для encoded entity records декларируют `status: review`, тогда как frontmatter файлов — `status: accepted` (work package state). Разница объяснена в том же README, но требует внимательного чтения.
- impact: минимальный; возможна путаница при материализации в track repository.
- recommendation: в правиле defaults явно сопоставить «статус work package файла» и «статус каждой encoded entity».

## Сильные стороны (для баланса)

1. Внутренняя согласованность выдающаяся для пакета такого размера: все проверяемые числовые заявления (155/10/19/69/17) сходятся, dangling semantic references не обнаружены.
2. Метамодель решает реальные проблемы дублирования (capability как каноническая единица, RoleView без владения, renditions для языков) и намеренно откладывает формализацию до появления потребителей — зрелое инженерное решение.
3. Осознанный отказ от искусственного заполнения L5 в B2 и от числовых рейтингов при выборе пилота — редкое сопротивление фиктивной точности.
4. Журнал решений (D-001–D-032) и review-протокол с adjudication создают воспроизводимую governance-цепочку; предыдущие gate-ревью действительно влияли на контент (видно по M1.3/M1.4 findings).

## Verdict

```text
verdict: accepted_with_changes
blocker: 0
major: 1 (finding 1 — docs/06 vs метамодель; исправить до M1.5)
minor: 8 (findings 2–9; можно в ближайший work package)
note: 7 (findings 10–16; backlog)
```

Пакет в состоянии M0+M1.1–M1.4 принимается: структура состоятельна, инварианты выполняются, единственный major — локальная усталость docs/06, не затрагивающая метамодель, матрицу или пилот. Условие принятия: finding 1 должен быть закрыт до вывода шаблонов M1.5, иначе конфликт двух accepted-документов мигрирует в первый thin slice.

Ограничения review: предметная глубина проверена на уровне структуры и формулировок capabilities/outcomes; полноценная domain-проверка содержательной корректности будущих briefs возможна только на G5 по мере их появления. Механические проверки выполнены вручную, без автоматического валидатора (что соответствует D-024).
