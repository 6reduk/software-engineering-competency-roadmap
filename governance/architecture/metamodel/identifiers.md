---
id: ela.metamodel.identifiers
kind: metamodel
status: accepted
updated: 2026-08-15
---

# Идентификаторы

ID стабилен при перемещении файла, понятен человеку, не зависит от порядка публикации и пригоден для cross-repository links.

## Корневые ID

```text
ela     # Program
a1..c1 # Track, например b2
```

Это допустимые стабильные исключения из общего формата.

## Общий формат

```text
<owner>.<kind>.<slug>
```

Примеры:

```text
ela.role-view.backend-distributed
b2.cluster.api-contracts
b2.module.reliable-http-api
b2.capability.evolve-api-contracts
b2.level-outcome.evolve-api-contracts-l4-cross-team-migration
b2.topic.http-idempotency
b2.learn.http-idempotency
b2.interview.http-idempotency
b2.kata.idempotent-create-endpoint
b2.project-spec.reliable-api
b2.implementation-reference.reliable-api-example-01
```

Допустимые `kind`:

- `role-view`;
- `cluster`;
- `module`;
- `capability`;
- `level-outcome`;
- `topic`;
- `learn`;
- `interview`;
- `kata`;
- `project-spec`;
- `implementation-reference`;
- `index`;
- `metamodel` и `review` для blueprint governance documents.

Значение metadata `kind` совпадает с kind-сегментом ID. Abstract `Artifact` и внешний проект не получают отдельный local kind/ID.

## LevelOutcome ID

Capability допускает несколько outcomes на уровень. ID outcome строится как:

```text
<track>.level-outcome.<capability-slug>-<level>-<outcome-slug>
```

Level входит в ID outcome, поскольку является частью его identity, но не включается в ID capability/topic/artifact.

## Slug

- lowercase ASCII;
- слова разделяются `-`;
- описывает смысл, а не технологию, если сущность technology-independent;
- версия библиотеки не включается;
- ID не меняется при редакционном переименовании title.

## Ссылки

Внутри репозитория используются относительные Markdown links и semantic ID. Cross-repository reference:

```yaml
id: b3.capability.manage-transaction-boundaries
repository: b3
path: capabilities/manage-transaction-boundaries.md
```

Поле `repository` содержит ID записи из глобального `governance/registry/repositories.yaml` blueprint. URL не выводится из naming convention.

В `ImplementationReference` внешний project repository адресуется отдельным полем `locator`; оно не участвует в этом cross-repository contract и может содержать URL или другой устойчивый внешний locator.

## Alias и supersession

Глобальный alias registry находится в `governance/registry/id-aliases.yaml` blueprint:

```yaml
- alias: b2.capability.old-name
  redirected_to: b2.capability.new-name
  changed_at: 2026-08-14
```

- при перемещении файла ID сохраняется;
- при исправлении границы старый ID становится alias;
- при смысловой замене старый entity получает `superseded_by`;
- `governance/registry/id-aliases.yaml` является единственным authoritative источником aliases;
- tombstone старой сущности может денормализованно содержать `redirected_to` только для удобства чтения;
- ID не переиспользуется для другой сущности.

## Языковые rendition

Языковые версии являются renditions одной semantic entity. Они используют один semantic ID, а конкретная публикация адресуется составным ключом `<semantic-id, language>`, например `b2.learn.http-idempotency@ru`.

Связь перевода указывает исходную rendition:

```yaml
translation_of:
  id: b2.learn.http-idempotency
  language: ru
  revision: 2026-08-14
```

Язык не входит в semantic ID; уникальность rendition проверяется по паре `(id, language)`.
