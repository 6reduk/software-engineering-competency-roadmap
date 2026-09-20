---
id: ela.metamodel
kind: metamodel-index
status: accepted
updated: 2026-08-14
---

# Метамодель программы

Метамодель определяет минимальный язык, на котором описывается программа. Её задача — обеспечить однозначный ownership, навигацию от общего к частному и переиспользование материалов без копирования по ролям и уровням.

## Документы

- [Сущности](entities.md)
- [Связи и инварианты](relationships-and-invariants.md)
- [Идентификаторы](identifiers.md)
- [Минимальные метаданные](metadata.md)
- [Реестр ID aliases](../../registry/id-aliases.yaml)
- [Реестр репозиториев](../../registry/repositories.yaml)

## Центральная модель

```text
RoleView ──requires──▶ Capability ◀──owns── Track
                          │
                   has LevelOutcome
                          │
                   covered by Artifact
                          │
          learn / interview / kata / project-spec
```

`Capability` — каноническая единица компетенции. Остальные представления ссылаются на неё.
