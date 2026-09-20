---
artifact: program-status
status: active
updated: 2026-09-20
---

# Статус программы

| Этап | Статус | Результат / следующий gate |
|---|---|---|
| Видение и границы | Принято | Изменения — через журнал решений |
| Карта вертикальных треков | Принята | A1–A3, B1–B11, C1 |
| Модель уровней | Принята | L1–L5 + необязательный ориентир L6 |
| Учебный flow | Принят | Включая project scaffolding без готового решения |
| Стандарт глубины | Принят концептуально | Проверить на 2–3 пробных темах |
| Архитектура репозиториев | Принята | Repository-per-vertical; проекты отдельно |
| Диагностика учащегося | Опциональна | Не является gate проекта или обязательным заданием |
| Role view: Backend / Distributed Systems | Draft | Определены роли треков и competency clusters |
| Role view: Architecture / Technical Leadership | Draft | Определены роли треков и competency clusters |
| Competency matrix | В работе | Следующий zoom: capabilities и критерии L1–L5 |
| План реализации M1+ | Принят | Исполнение начинается с M1.1 |
| Протокол review gates | Принят | Проверить на первом work package |
| Контракт автономного автора | Принят | После каждого пакета оркестратор выдаёт новый `/goal`; один автор владеет ограниченным набором файлов |
| M1.1 Метамодель | Завершена | G1 structure и learning review: accepted |
| M1.2 Skeleton matrix | Завершена | G2 structure/domain review: accepted; 15 треков, 155 clusters |
| M1.3 Выбор пилота | Завершён | B2 принят; structure и domain/learning review: accepted |
| M1.4 Blueprint пилота | Завершён | G3 domain и learning/level review: accepted; 10 modules, 19 capabilities, 69 LevelOutcomes |
| Внешнее консолидированное review M0–M1.4 | Принято после исправлений | C-01–C-26 закрыты; 0 open blocker/major/minor/note; resolution verdict `accepted` |
| M1.5 Первый thin slice | Завершён | Шесть материалов `evolvable-api-contracts` приняты после пользовательской, технической и human-readability проверки |
| M1.6 Provisional-калибровка | Завершена | C-1–C-11 и N-1/N-3 закрыты; после контрастного G4b стандарт стабилизирован и принят отдельным gate |
| M1.7 Контрастный slice | Завершён | G4b принят; 12/12 изменяемых findings закрыты, C-11 закрыт решением; шесть runtime-материалов имеют `status: accepted` |
| Стабилизация редакционного стандарта | Завершена | Два независимых профиля: verdict `accepted`, 0 blocker/major/minor; четыре notes закрыты оркестраторским acceptance-проходом |
| M1.8.0 Аудит покрытия и очередь B2 | Завершён | Подтверждены 10 modules, 19 capabilities, 69 outcomes и 104 relationships; следующим принят Service Architecture/S06 |
| M1.8.1 Service Architecture/S06 | Завершён | G5 accepted; 5 artifacts, 26 relationships, Architecture L1–L3 и Verification L1–L2 |
| M1.8.2 Обновление B2 delivery plan | Завершён | Два независимых профиля: `accepted`, 0 blocker/major/minor; подтверждены 17 artifacts, 130 relationships и выбор Service Verification/S10 |
| M1.8.3 Service Verification/S10 | Завершён | G6 принят после закрытия 2 minor и disposition 6 notes; 5 artifacts, 25 relationships, первое покрытие Compatibility L1 |
| M1.8.4 Обновление B2 delivery plan | Завершён | Два независимых профиля подтвердили 22 artifacts, 155 relationships, 42/27 outcomes, состояния 0/5/5/0 и выбор Transactional Persistence/S07; B3 readiness принят как внутренний gate M1.8.5 |
| M1.8.5 Transactional Persistence/S07 | Завершён | G7 принят после закрытия 2 minor и 5 notes; 5 artifacts, 22 relationships, пять новых outcomes и раздельное evidence Transaction L3 / Idempotency L3 |
| M1.8.6 Обновление B2 delivery plan | Завершён | Два независимых профиля подтвердили 27 artifacts, 177 relationships, 47/22 outcomes, состояния 0/6/4/0 и выбор Background Workflows/S09; 1 minor и локальные notes закрыты |
| M1.8.7 Background & Message-driven Workflows/S09 | Завершён | G8 принят после закрытия 1 minor и 3 notes; 5 artifacts, 11 relationships, Workflow L2/L3 и проверенная RabbitMQ/aio-pika recovery-модель |
| M1.8.8 Обновление B2 delivery plan | Завершён | Подтверждены 32 artifacts, 188 relationships, 49/20 outcomes, состояния 0/7/3/0 и выбор Identity-aware Boundaries/S05; A3 readiness вынесен в Gate 0 M1.8.9 |
| M1.8.9 Identity-aware Boundaries/S05 | Завершён | G9 принят после закрытия 1 minor и 1 локального note; 5 artifacts, 15 relationships, Identity L1–L3 и проверенная RS256/trusted-context/object-authorization модель |
| M1.8.10 Обновление B2 delivery plan | Завершён | Два независимых профиля подтвердили 37 artifacts, 203 relationships, 52/17 outcomes и состояния 0/8/2/0; C-1–C-4 закрыты, следующим принят bounded S14 operation-cost admission package |
| M1.8.11 Operation-cost admission/S14 | Завершён | G10 принят после закрытия C-1–C-7 и disposition C-8/C-9; 5 artifacts, 13 relationships, Abuse L1–L3 без Abuse L4, quota/rate или SSRF overclaim |
| M1.8.12 Обновление B2 delivery plan | Завершён | G11 подтвердил 42 artifacts, 216 relationships, 55/14 outcomes и состояния 0/8/2/0; C-1–C-5 закрыты, следующим принят Application Caching/S15 |
| M1.8.13 Application Caching/S15 | Завершён | G12 принят после закрытия C-1–C-12; 5 artifacts, 11 relationships, Cache L2/L3 с bounded freshness и one-process coalescing без Cache L4/distributed overclaim |
| M1.8.14 Обновление B2 delivery plan | Завершён | G13 подтвердил 47 artifacts, 227 relationships, 57/12 outcomes и состояния 0/8/2/0; C-1/C-2 закрыты, следующим принят Safe Service Evolution/S11 |
| M1.8.15 Safe Service Evolution/S11 | Завершён | G14 принят после закрытия C-1–C-9; 5 artifacts, 13 relationships, Delivery L1–L3 с измеренным stop/recovery и честной границей одно-процессной модели без Delivery L4/B6/B7 overclaim |
| M1.8.16 Обновление B2 delivery plan | Завершён | G15 принят как явное однопрофильное исключение: независимый mechanical profile и orchestrator risk assessment подтвердили 52 artifacts, 240 relationships, 58/11 outcomes, состояния 0/9/1/0 и bounded выбор External Integration/S08; correction groups закрыты |
| M1.8.17 External Integration/S08 | Завершён | G16 принят как явное однопрофильное исключение: профиль A независимо воспроизвёл Gate 0; 5 artifacts, 9 relationships, External L1/L2 и правдивая Pricing client boundary без L3/L4, A3/B5 или полного S08 completion |
| M1.8.18 B2 breadth-pass refresh | Завершён | G17 принят как явное однопрофильное исключение: подтверждены 57 artifacts, 249 relationships, 58/11 outcomes и states 0/10/0/0; breadth-pass завершён как own content entry 10/10 при five-genre flow 9/10 и module completion 0/10; следующим принят consolidation dossier без нового coverage |
| M1.8.19 B2 consolidation dossier | Завершён | G18 принят как явное однопрофильное исключение после закрытия M-1/N-1; зафиксированы 10 routes, 10 not-ready module gates, 27 debt records и readiness 11 самостоятельных проектов без нового coverage; следующим принят bounded HTTP Runtime/S01 package с отдельным B1/A3 Gate 0 |
| M1.8.20 HTTP Runtime/S01 | Завершён | G19 принят как явное однопрофильное исключение после закрытия A-1/A-2; 4 artifacts, 10 relationships, собственные index/interview/kata/project-spec и Trace L1/L2 execution без production L3, supporting coverage или module completion |
| M1.8.21 Post-S01 consolidation refresh | Завершён | G20 принят как явное однопрофильное исключение без correction-pass; подтверждены 61 artifact, 259 relationships, 58/11 outcomes, полный пятижанровый flow 10/10 и 10 not-ready module gates; D19/D20 закрыты только в content-части, следующим принят один B3 boundary intake |
| M1.9.0 B3 transaction/isolation boundary intake | Завершён | G21 принят после двух независимых профилей и закрытия C-1–C-6; выбрано одно store-level действие вокруг write skew и `REPEATABLE READ → SERIALIZABLE`, без runtime evidence, Gate 0, semantic IDs или coverage; следующим назначен bounded capability blueprint кластера transactions/concurrency |
| M1.9.1 B3 transactions/concurrency reference blueprint | Завершён | G22 принят после двух независимых профилей и закрытия одного minor; приняты 1 module, 3 capabilities, 10 outcomes, 3 сценария и 11 ролевых связей без coverage/Gate 0/runtime evidence; reference не становится обязательной семифайловой нормой, следующим назначен единый breadth-pass остальных 10 кластеров |
| M1.9.2 B3 полный capability breadth-pass | Завершён | G23 принят после двух независимых профилей и correction-pass C-1/C-2; приняты 11 modules, 23 capabilities, 70 outcomes, 13 scenarios и 79 ролевых связей без coverage/Gate 0/runtime evidence; первым deep slice выбран SQ01, SE01 остаётся вторым кандидатом |
| M1.9.3 B3 SQL result correctness/SQ01 | Завершён | G24 принят после двух независимых профилей и correction-pass C-1–C-3/C-5–C-7; приняты 5 artifacts, 30 relationships к 8 targets и глубокий маршрут SQL composition + grouped/window results L1–L3 без заявления proficiency или ImplementationReference |
| M1.9.4 B3 schema-evolution boundary intake/SE01 | Завершён | G25 принят после двух независимых профилей и correction-pass C-1–C-8; выбран переход `amount_rub → amount_minor` через сосуществование и backfill без runtime evidence или coverage; следующим разрешён M1.9.5 с обязательным Gate 0 до authoring |
| M1.9.5 B3 schema evolution/SE01 | Завершён | G26 принят после двух независимых профилей и correction-pass C-1–C-3; приняты 5 artifacts и 30 relationships к 8 targets, служебный Gate 0 evidence вынесен побайтово в sidecar-файлы; это второй и последний заранее запланированный глубокий B3 slice без заявления proficiency, ImplementationReference или module completion |
| M1.9.6 B3 phase close-out | Завершён | G27 принят после двух независимых профилей и correction-pass C-1–C-4; подтверждены 11 modules, 23 capabilities, 70 outcomes, 13 scenarios, 10 accepted artifacts и 60 relationships. Первый авторский проход B3 закрыт; девять модулей остаются blueprint-only, module completion и proficiency не заявлены, BR01 не запускается автоматически |
| M2.0 Выбор следующей вертикали | Завершён | После двухпрофильного G28 и correction-pass C-1–C-6 следующей вертикалью принят B5 Distributed Systems & System Design. Первый проход ограничен boundary intake, одним breadth-pass, одним или двумя deep slices и обязательным close-out; следующий пакет только planning intake, без blueprint, coverage или Gate 0 |
| M2.1 B5 boundary intake | Завершён | После двухпрофильного G29 принят предметный контур B5, prerequisites A1/A3, границы B2/B3/B6/B7/C1, три screening-кандидата и C1 decision-record lens. Semantic entities, coverage, Gate 0 и deep-slice selection не создавались; следующим разрешён один capability breadth-pass |
| M2.2 B5 capability breadth-pass | Завершён | После двухпрофильного G30 и correction-pass C-1/C-2/C-4 приняты 6 modules, 17 capabilities, 51 outcomes, 11 scenarios и 34 role links без coverage или proficiency. Первым deep slice выбран stale-authority/fencing вокруг TO01/CL01; конкретный substrate подтверждается Gate 0 M2.3 |
| M2.3 B5 stale authority / fencing | Завершён | G31 принят после двух независимых профилей и correction-pass C-1–C-5; приняты 5 artifacts и 35 relationships к 11 targets. Хронология честно сохраняет финальный rerun после authoring; acceptance не означает proficiency, production readiness или module completion. Следующим назначен только фазовый выбор между вторым контрастным slice и обязательным close-out |
| M2.4 Выбор второго B5 slice | Завершён | G32 принят двумя независимыми профилями без correction-pass: выбран обязательный close-out после одного deep slice. CA01/ME01 не признаны бесполезными, но readiness и превышение ценности над стоимостью не подтверждены; второе authoring не запускается |
| M2.5 B5 phase close-out | Завершён | G33 принят после correction-pass C-1/C-2: подтверждены 6 modules, 17 capabilities, 51 outcomes, 11 scenarios, 34 role links и 5 artifacts / 35 relationships. Первый B5-pass закрыт после одного deep slice без module completion или proficiency; следующим разрешён только program-level depth checkpoint |
| M3.0 Program depth checkpoint | Завершён | G34 принят двумя независимыми профилями без correction-pass: остановлен текущий детальный authoring после B2/B3/B5. Следующий режим — использование существующих маршрутов и learner execution; C1/B7/B6 и ещё девять треков сохраняются как ролевая карта и backlog без автоматической очереди authoring |
| M3.1 Program authoring close-out | Завершён | G35 принят после двух независимых профилей и correction-pass C-1: текущая authoring-фаза закрыта, один честный input `задача / доступная среда / первый результат` сохранён. Project-spec не выбран, learner execution и доступность среды не подтверждены |
| P1 Module-state audit | Завершён | Введён отдельный authoring gate, не зависящий от прохождения программы пользователем: из 27 модулей B2/B3/B5 закрыты для текущего authoring scope 10, partial — 3, blueprint-only — 14. Остальные 12 вертикалей остаются track-skeleton-only без вымышленных module definitions |
| P5 Публичный README и лицензирование | Завершён | README объясняет матрицу, маршруты, уровни, state и Load state; содержание лицензировано по CC BY 4.0, `tools/` и самостоятельный исполняемый код — по MIT; правообладатель `Shestakov Dmitriy <6reduk@gmail.com>` |
| P6 Pre-publication validation | Завершён | Три независимых профиля и точечные повторные проверки закрыли два major и пять minor; принят publication-validator и кандидат очищенного snapshot без внешней записи |
| Пилотная вертикаль | Принята | B2 Backend & API Engineering |
| GitHub-репозитории | Не созданы | Создавать только после утверждения blueprint |

## Ближайший milestone

`M0 — Blueprint accepted` завершён 2026-08-13.

P1 module-state audit и P2 migration завершены. Каноническое состояние модулей —
`10 closed-for-authoring / 3 partial / 14 blueprint-only / 0 not-started`.
P3 создал [машинный current-state manifest](current-state.yaml) и
[load-state инструкцию](LOAD-STATE.md). P4 упаковал переносимый
[authoring toolkit](../../authoring/README.md). P5 подготовил публичный README,
раздельную лицензию и notice. Следующий bounded пункт подготовки публикации —
P6 завершил независимый audit и сформировал кандидат очищенного snapshot.
Следующий bounded пункт — P7: создать GitHub-репозиторий и выполнить внешнюю
публикацию после подтверждения owner, имени и visibility. Learner execution и
подтверждение proficiency остаются вне scope репозитория.
