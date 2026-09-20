---
id: program.validation.pre-publication-p6
kind: review
title: "P6: pre-publication validation"
status: accepted
owner: orchestrator
updated: 2026-09-20
language: ru
sources:
  - README.md
  - LICENSE
  - NOTICE
  - requirements-validation.txt
  - governance/state/current-state.yaml
  - governance/state/MODULE-STATE.md
  - governance/state/STATUS.md
  - governance/decisions.md
  - governance/planning/publication-and-continuity-todo.md
  - tools/validate_state.py
  - tools/validate_publication.py
---

# P6: pre-publication validation

## Решение

Текущий snapshot признан кандидатом на внешнюю публикацию после создания
коммита, содержащего этот отчёт и переход state на P7. Внешняя запись, создание
GitHub-репозитория, push и tag в P6 не выполняются.

Локальная pre-publication Git-история не входит в кандидат. По D-085 публичная
история должна начаться с отдельного очищенного snapshot; reviews, work packages
и evidence входят в него как исторический ненормативный audit trail.

## Независимые профили

Перед correction-pass выполнены три независимых read-only профиля:

| Профиль | Первичный результат | Найдено |
|---|---|---|
| Privacy / security / publication hygiene | `CONDITIONAL` | Решение о review-архиве; предупреждение для исполняемого evidence |
| Structure / navigation | `CONDITIONAL` | Drafting RoleView был назван готовым roadmap; одна битая anchor-ссылка |
| State / governance / reproducibility | `CONDITIONAL` | Неясный basis commit, незакреплённый PyYAML, неполный validator, неоднозначный RoleView lifecycle |

Correction-pass зафиксирован коммитом
`70181b46618411200647d99a7261cf33ea2ab8a7`. Все три профиля повторили
точечную проверку и вернули `PASS` без остаточных findings.

## Исправленные границы

- D-085 фиксирует публикацию полного audit trail и начало публичной Git-истории
  с очищенного snapshot.
- `governance/README.md`, `reviews/README.md` и `work-packages/README.md`
  отделяют нормативное текущее состояние от исторических записей.
- Корневой README честно называет два RoleView черновыми проекциями и содержит
  только разрешающиеся ссылки.
- `manifest_origin` ссылается на P3/D-082 без заявления публичного SHA из
  локальной истории.
- `requirements-validation.txt` закрепляет `PyYAML==6.0.3`; Load state содержит
  команду установки.
- State-validator проверяет D-079–D-085, P5/STATUS, license/notice, RoleView и
  governance boundaries.
- Historical `probe.py` не изменён; соседнее предупреждение требует отдельного
  одноразового контейнера. Его SHA-256 остался
  `ed81b839c79f7e014f872991653ef65d2d0524d744f00cfa514bd91ebca3fd2b`.

## Проверки кандидата

| Область | Результат |
|---|---|
| State | Два последовательных запуска дают идентичный `STATE_OK`; validator не меняет дерево |
| Layout и ссылки | `MIGRATION_LAYOUT_OK`; отсутствуют stale и broken local links |
| YAML и IDs | Front matter/YAML разбираются с запретом повторных ключей; semantic IDs уникальны |
| Markdown | Fences/details сбалансированы; conflict markers и trailing whitespace отсутствуют |
| Privacy | Не обнаружены secrets, private keys, credentials, внутренние URL, конкретные локальные home paths или чужие email |
| Лицензирование | CC BY 4.0 применяется к содержанию; MIT — к tools и самостоятельному исполняемому коду; разрешённый правообладатель указан в LICENSE/NOTICE |
| Governance | Module state `10/3/14/0`, шесть debt groups, G35, D-084/D-085 и P6→P7 согласованы |
| Clean release archive | Validator и Load state повторяются из отдельного `git archive` кандидат-коммита с закреплённым PyYAML; архив содержит тот же tracked tree без `.git` |

Проверки выполняет `python tools/validate_publication.py`; он вызывает state и
layout validators, проверяет UTF-8, YAML keys/IDs, privacy-маркеры, разрешённый
email, license, RoleView и audit-trail contracts. Git cleanliness проверяется до
и после запуска отдельно.

## Ограничения

- Поиск секретов снижает риск, но не является юридической или forensic
  гарантией отсутствия любой чувствительной информации.
- Локальный `git clone` на этой Windows-конфигурации не смог запустить
  `git-upload-pack`; вместо него проверен созданный Git самим чистый release
  archive того же commit tree. Git metadata не входила в эту проверку.
- Старые reviews/work packages могут содержать отменённые решения; их
  ненормативность является частью опубликованного контракта.
- P6 не проверяет внешнюю GitHub-аутентификацию, имя/visibility будущего
  репозитория или доступность URL — это входы P7.
- Публикация не подтверждает learner execution, proficiency, production
  readiness или полноту всех 15 вертикалей.

## Handoff P7

Перед внешней записью владелец подтверждает GitHub owner, имя репозитория и
visibility. Затем создаётся новая публичная история из кандидат-коммита без
переноса локальных родителей, выполняются push/tag и проверка удалённого README,
LICENSE, default branch и точного SHA.

SHA кандидат-коммита не записывается внутрь самого коммита во избежание
самоссылки. Он сообщается в P6 handoff и используется как исходный tree для
очищенного snapshot P7.
