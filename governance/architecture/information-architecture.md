---
artifact: information-architecture
status: accepted
updated: 2026-08-15
---

# Архитектура знаний и репозиториев

## Zoom-модель

```text
Program
└── Track
    └── Cluster
        └── Capability
            └── Topic (только когда полезен как самостоятельная единица)
                └── Artifact: learn / interview / kata / project-spec / implementation-reference / index
```

Это основная ось предметной навигации. `Module` не является ещё одним уровнем этой иерархии: он собирает законченный учебный пакет вокруг 1..N capabilities, а artifacts принадлежат основному module и могут покрывать несколько capabilities/topics. Группы foundation / engineering / data-ml / leadership допустимы только как оформление индекса и не образуют сущность `Domain`.

Каждый устойчивый уровень имеет короткий индекс. Агенту или человеку не требуется загружать весь трек: сначала читается индекс текущего уровня, затем выбранный cluster/capability и только относящиеся к задаче modules и artifacts.

## Предлагаемая единица репозитория

Один репозиторий на устойчивую вертикаль, а не на библиотеку и не на тип артефакта. Например, FastAPI — модуль Backend & API Engineering, а не отдельная программа. Внутри вертикали теория, интервью, мини-задачи и каталог проектов расположены рядом.

```text
ela-python-engineering/
├── README.md
├── TRACK.yaml
├── roadmap/
├── modules/
│   └── iterators-generators/
│       ├── README.md
│       ├── learn/
│       ├── interview/
│       ├── katas/
│       └── projects/
└── sources/
```

Самостоятельная реализация каждого достаточно крупного проекта получает отдельный репозиторий. Blueprint хранит глобальную карту, стандарты, реестр репозиториев и статус.

## Метаданные артефакта

Канонический минимальный контракт определён в [`governance/architecture/metamodel/metadata.md`](metamodel/metadata.md). Пример для учебного артефакта:

```yaml
id: b1.learn.iterator-protocol
kind: learn
title: Протокол итерации Python
owner_track: b1
module: b1.module.iteration-protocols
coverage:
  - target: b1.capability.apply-iteration-protocol
    role: teach
status: drafting
updated: 2026-08-15
language: ru
```

Идентификаторы в примере иллюстративны до детализации B1. Метаданные должны оставаться минимальными. Новое поле добавляется только если уже существует реальный сценарий его использования; freshness по умолчанию наследуется от Module, а version-sensitive artifact может задать `last_verified` и `versions` как override.

## Статусы

`proposed → accepted → drafting → review → published → maintenance`

Для устаревшего материала дополнительно используется `needs-update`; для заменённого — `superseded` со ссылкой на замену.
