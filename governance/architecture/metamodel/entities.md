---
id: ela.metamodel.entities
kind: metamodel
status: accepted
updated: 2026-08-14
---

# Сущности

## Program

Вся система Engineering Leadership & Architecture. Владеет глобальным видением, моделью уровней, реестром треков/репозиториев, role views и общими стандартами.

Source of truth: blueprint repository.

## RoleView

Проекция общей competency model на тип ответственности, например Backend / Distributed Systems.

Содержит ссылки на треки/capabilities, `core/depth/awareness`, навигационный target level, приоритетные outcomes и interview expectations. RoleView не владеет и не копирует учебное содержание.

Track-level target — только summary. После детализации authoritative являются требования к конкретным LevelOutcomes.

Source of truth: blueprint repository, `routes/`.

## Track

Устойчивая область инженерной ответственности с ясными mission и границами. Трек группирует capabilities и имеет один основной репозиторий. Он определяется задачами, а не названием библиотеки: FastAPI является частью B2, но не отдельным треком.

Source of truth: глобальная запись — blueprint; детальное содержание — track repository.

## Cluster

Крупная навигационная группа capabilities внутри трека. Cluster показывает структуру области, но не является проверяемой компетенцией и не получает уровни.

Каждая capability имеет один primary cluster и может ссылаться на related clusters.

Source of truth: track repository.

## Module

Стабильная завершённая единица учебной навигации/release. Module принадлежит ровно одному треку, развивает 1..N его capabilities, объединяет artifacts и может ссылаться на capabilities других треков.

Отличия:

- Cluster классифицирует предметную область;
- Module собирает завершённый учебный пакет;
- WorkPackage является временной процессной единицей review и не обязан становиться Module.

Source of truth: track repository.

## Capability

Минимальная каноническая единица профессиональной способности, подтверждаемая наблюдаемым действием.

Хорошо:

> Проектирует эволюционируемый HTTP API и проводит изменения без нарушения совместимости клиентов.

Плохо:

> REST API.

Capability имеет ровно один owner track и primary cluster, может использовать prerequisites других треков, иметь outcomes не для всех L1–L5 и покрываться несколькими artifacts/modules.

Source of truth: owner track repository.

## LevelOutcome

Наблюдаемое проявление capability на применимом уровне L1–L5. Capability может иметь 0..N outcomes на уровень; каждый outcome имеет semantic ID.

Содержит:

- действие;
- контекст и масштаб;
- ожидаемую самостоятельность;
- evidence criteria — наблюдаемые результаты работы, подтверждающие способность.

Evidence не является ссылкой на учебный artifact. Artifact может оценивать outcome через coverage link.

Source of truth: рядом с capability в owner track repository.

## Topic

Атомарная единица знания или ментальной модели, используемая capabilities. Topic отвечает на вопрос «что нужно понять», capability — «что инженер должен уметь сделать». Topic не получает hiring-grade и создаётся отдельно только при независимой ценности поиска, переиспользования или обновления.

Source of truth: owner track repository.

## Artifact

Конкретный материал, объясняющий, проверяющий или закрепляющий capabilities/topics.

Subtype kinds:

- `learn` — engineering brief;
- `interview` — вопрос, follow-up, rubric или scenario;
- `kata` — ограниченная практическая задача;
- `project-spec` — спецификация интеграционного проекта/этапа;
- `implementation-reference` — проверенная ссылка на внешнюю реализацию;
- `index` — навигационный документ.

Не каждой capability нужны все виды artifacts. `ProjectSpec` и `ImplementationReference` — subtype Artifact, а не отдельные конкурирующие модели.

Source of truth: track repository.

## ExternalProjectImplementation

Внешний проект и его история. Он не является управляемой сущностью учебной метамодели, не получает локальный semantic ID и не считается каноническим ответом.

Track repository хранит ImplementationReference с locator, revision и review metadata. Source of truth реализации — отдельный project repository автора.
