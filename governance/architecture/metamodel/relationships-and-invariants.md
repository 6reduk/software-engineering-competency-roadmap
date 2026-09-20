---
id: ela.metamodel.relationships
kind: metamodel
status: accepted
updated: 2026-08-15
---

# Связи и инварианты

## Типизированные связи

| Откуда | Связь | Куда | Смысл |
|---|---|---|---|
| Program | contains | Track | Реестр вертикалей |
| Program | exposes | RoleView | Ролевые проекции |
| Track | groups | Cluster | Навигационная классификация |
| Track | owns | Capability | Каноническое владение |
| Module | develops | Capability | Capability входит в пакет |
| Capability | has | LevelOutcome | Наблюдаемое проявление уровня |
| Capability | requires | Capability | Жёсткий prerequisite |
| Capability | relates-to | Capability | Необязательная связь |
| Capability | uses | Topic | Необходимая ментальная модель |
| Artifact | covers | Capability/LevelOutcome | Объясняет, проверяет или закрепляет |
| Artifact | explains | Topic | Раскрывает знание |
| RoleView | requires | Track/LevelOutcome | Summary или authoritative requirement |
| ImplementationReference | implements | ProjectSpec | Связь со спецификацией |
| ImplementationReference | references | ExternalProjectImplementation | Locator внешней реализации |

## Cardinality

1. Track содержит 1..N clusters и владеет 1..N capabilities.
2. Capability имеет ровно один primary cluster и 0..N related clusters.
3. Module имеет ровно один owner track, развивает 1..N owned capabilities и может ссылаться на 0..N external capabilities.
4. Capability может входить в 0..N modules.
5. Content Artifact имеет ровно один primary module. `index` может принадлежать track/cluster без module.
6. Capability имеет 0..N LevelOutcomes на каждый применимый уровень.
7. LevelOutcome принадлежит ровно одной capability и одному уровню.

## Coverage

`Artifact → Capability/LevelOutcome` получает роль:

- `explain` — формирует ментальную модель;
- `probe` — выявляет reasoning, гипотезы и границы понимания, но само по себе не является достаточным evidence proficiency;
- `assess` — проверяет действие или решение в контексте, способном дать требуемое outcome evidence;
- `practice` — тренирует навык;
- `integrate` — объединяет capabilities;
- `reference` — показывает внешний пример/источник.

Coverage capability без outcome означает общее покрытие и не доказывает уровень. Evidence в LevelOutcome — наблюдаемый результат работы; coverage — назначение учебного artifact.

Interview artifact обычно получает `probe`. Он может проверять качество reasoning для L1–L4, но L4/L5 proficiency требует evidence реального масштаба, adoption/migration и последствий; словесный ответ не заменяет execution evidence.

## Ownership

1. Capability имеет ровно один owner track.
2. Topic и Artifact имеют один primary owner track.
3. Чужие сущности переиспользуются ссылками, а не копируются.
4. RoleView не владеет capabilities/artifacts.
5. ProjectSpec и ImplementationReference принадлежат треку; ExternalProjectImplementation — внешнему repository.
6. При споре owner выбирается по основному инженерному вопросу capability.

## Уровни и RoleView

1. Уровень описывает поведение, не сложность текста или редкость факта.
2. Outcome содержит evidence criteria.
3. Необязательно заполнять L1–L5 полностью.
4. Рост уровня обычно увеличивает самостоятельность, неопределённость, масштаб и последствия.
5. Hiring-тег не хранится в каждой capability.
6. Track-level target в RoleView — навигационный summary и не наследуется всеми capabilities.
7. Authoritative role requirement задаётся списком конкретных LevelOutcome IDs. Отсутствие требования означает «не задано», а не нулевой уровень.

## Структура

1. Hard-prerequisite graph не содержит циклов.
2. Индекс zoom-уровня перечисляет непосредственных детей и ключевые cross-links.
3. Topic выделяется, только если независимо ищется, переиспользуется или обновляется.
4. Module имеет scope/non-goals; WorkPackage остаётся процессным понятием без обязательного ID.
5. Один Artifact может покрывать несколько capabilities.
6. Technology-specific материал отделяется от устойчивой концепции при разных циклах обновления.

## Изменение ownership

Перенос capability:

1. фиксируется в decision log;
2. старый ID получает redirect в глобальном alias registry blueprint;
3. входящие ссылки обновляются;
4. история не переписывается;
5. заменённый материал получает `superseded` при необходимости.
