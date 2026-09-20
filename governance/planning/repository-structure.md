---
id: program.plan.public-repository-structure
kind: plan
title: "Публичная структура репозитория и карта миграции"
status: accepted
owner: orchestrator
updated: 2026-09-19
language: ru
---

# Публичная структура репозитория и карта миграции

## Назначение

Документ задаёт целевую структуру публичного репозитория и однозначную карту
переноса. Он не выполняет перенос и не создаёт вторые копии канонических
документов. До отдельного принятия этой карты текущие пути остаются source of
truth.

Структура разделяет четыре разных вида содержимого:

- `curriculum/` — то, чем пользуется читатель учебного плана;
- `governance/` — архитектура программы, её состояние, решения и аудиторский
  след;
- `authoring/` — правила воспроизводимого создания и проверки материалов;
- `tools/` — исполняемые проверки и команды восстановления состояния.

Обучение конкретного пользователя и подтверждение его навыков в эти каталоги не
входят и не становятся состоянием программы.

## Фактическая исходная точка

На момент проектирования в репозитории 504 Markdown-файла. Основные каталоги:

| Путь | Файлов | Назначение сейчас |
|---|---:|---|
| `docs/` | 10 | концепция программы, стандарты и workflow |
| `matrix/` | 23 | 15 track cards, ролевое резюме и planning intakes |
| `metamodel/` | 5 | сущности, идентификаторы и инварианты |
| `pilot/` | 109 | B2/B3/B5 catalogs, routes и учебные slices |
| `registry/` | 2 | aliases и внешние repositories |
| `reviews/` | 233 | независимые профили, consolidation и acceptance |
| `routes/` | 3 | два ролевых входа |
| `work-packages/` | 116 | bounded authoring packages и Gate 0 records |

В Markdown обнаружено более 2200 локальных ссылок. Поэтому ручной перенос и
частичный compatibility layer запрещены: они с высокой вероятностью создадут
две версии истины или незаметно разорвут traceability.

## Целевая структура

```text
/
├── README.md
├── LICENSE
├── NOTICE.md
├── curriculum/
│   ├── program/
│   ├── roles/
│   └── tracks/
│       ├── catalog/
│       ├── b2/
│       ├── b3/
│       └── b5/
├── governance/
│   ├── architecture/
│   │   └── metamodel/
│   ├── state/
│   ├── planning/
│   │   └── intakes/
│   ├── work-packages/
│   ├── reviews/
│   └── registry/
├── authoring/
│   ├── standards/
│   ├── workflow/
│   ├── agents/
│   └── skills/
└── tools/
```

`README.md`, `LICENSE` и `NOTICE.md` остаются в корне как публичная стартовая
точка. Остальные корневые документы после миграции должны иметь ровно одно
каноническое место в одном из четырёх каталогов.

## Карта старых и новых путей

### Учебный план

| Старый путь | Новый путь | Правило |
|---|---|---|
| `docs/01-vision-and-scope.md` | `curriculum/program/vision-and-scope.md` | один файл |
| `docs/02-track-map.md` | `curriculum/program/track-map.md` | один файл |
| `docs/03-level-model.md` | `curriculum/program/level-model.md` | один файл |
| `docs/04-learning-flow.md` | `curriculum/program/learning-flow.md` | один файл |
| `docs/07-diagnostic-and-routing.md` | `curriculum/program/diagnostic-and-routing.md` | один файл |
| `docs/08-audience-and-use-cases.md` | `curriculum/program/audience-and-use-cases.md` | один файл |
| `routes/README.md` | `curriculum/roles/README.md` | один файл |
| `routes/backend-distributed-systems.md` | `curriculum/roles/backend-distributed-systems.md` | один файл |
| `routes/architecture-technical-leadership.md` | `curriculum/roles/architecture-technical-leadership.md` | один файл |
| `matrix/role-summary.md` | `curriculum/roles/role-summary.md` | один файл |
| `matrix/README.md` | `curriculum/tracks/README.md` | один файл |
| `matrix/tracks/*.md` | `curriculum/tracks/catalog/*.md` | все 15 track cards |
| `pilot/b2/**` | `curriculum/tracks/b2/**` | дерево целиком |
| `pilot/b3/**` | `curriculum/tracks/b3/**` | дерево целиком |
| `pilot/b5/**` | `curriculum/tracks/b5/**` | дерево целиком |

Имена B2/B3/B5 сохраняются: это стабильные коды вертикалей, а не признак
временного pilot lifecycle. Слово `pilot` после принятия authoring close-out в
публичной навигации больше не требуется.

### Архитектура и управление программой

| Старый путь | Новый путь | Правило |
|---|---|---|
| `docs/06-information-architecture.md` | `governance/architecture/information-architecture.md` | один файл |
| `metamodel/**` | `governance/architecture/metamodel/**` | дерево целиком |
| `STATUS.md` | `governance/state/STATUS.md` | текущее состояние программы |
| `MODULE-STATE.md` | `governance/state/MODULE-STATE.md` | канонические authoring states |
| `OPEN-QUESTIONS.md` | `governance/state/OPEN-QUESTIONS.md` | открытые решения и долг верхнего уровня |
| `PROGRAM-AUTHORING-CLOSEOUT.md` | `governance/state/PROGRAM-AUTHORING-CLOSEOUT.md` | фазовый close-out |
| `DECISIONS.md` | `governance/decisions.md` | журнал решений |
| `EXECUTION-PLAN.md` | `governance/planning/execution-plan.md` | исторический и текущий план |
| `PUBLICATION-AND-CONTINUITY-TODO.md` | `governance/planning/publication-and-continuity-todo.md` | план публикации |
| `REPOSITORY-STRUCTURE.md` | `governance/planning/repository-structure.md` | эта карта после принятия |
| `matrix/intakes/**` | `governance/planning/intakes/**` | дерево целиком |
| `pilot/M1.3-pilot-selection.md` | `governance/planning/M1.3-pilot-selection.md` | историческое решение |
| `work-packages/**` | `governance/work-packages/**` | дерево целиком |
| `reviews/**` | `governance/reviews/**` | дерево целиком, если разрешено privacy-аудитом |
| `registry/**` | `governance/registry/**` | дерево целиком |

`governance/state/` получит в P3 новый current-state manifest. Он будет
единственной машинно читаемой точкой восстановления. `STATUS.md`,
`MODULE-STATE.md` и журналы останутся его нормативными источниками, но не будут
дублироваться в других каталогах.

### Методика authoring

| Старый путь | Новый путь | Правило |
|---|---|---|
| `docs/05-content-standard.md` | `authoring/standards/content-standard.md` | один файл |
| `docs/09-editorial-standard.md` | `authoring/standards/editorial-standard.md` | один файл |
| `docs/10-content-author-workflow.md` | `authoring/workflow/content-author-workflow.md` | один файл |
| `REVIEW-PROTOCOL.md` | `authoring/workflow/review-protocol.md` | один файл |

Каталоги `authoring/agents/` и `authoring/skills/` создаются в P4 на основе этих
принятых правил. Туда нельзя копировать машинную память, токены, настройки
конкретной среды или системные skills неизвестной лицензии.

### Инструменты

`tools/` создаётся только вместе с первым исполняемым validator или state-loading
helper. Пустой каталог и ручные копии команд не создаются. Инструменты не должны
содержать учебные ответы, runtime secrets или менять документы при проверке
неизменного snapshot.

## Что не переносится автоматически

До публичного snapshot отдельно проверяются:

- абсолютные локальные пути; сейчас найден как минимум один путь в Gate 0 record
  M1.8.20;
- имена пользователей, временные каталоги, команды окружения и локальные PID;
- содержимое review и evidence-файлов, которое могло быть допустимо локально,
  но не предназначено для публичного доступа;
- executable evidence с неизвестной лицензией или происхождением;
- ссылки на недоступные внешнему читателю ресурсы.

Удаление такого содержимого из последнего дерева недостаточно, если в GitHub
будет отправлена прежняя локальная история: старые commits всё равно сохранят
его. Поэтому по умолчанию публичная история начинается с одного проверенного
snapshot commit после P6. Полная локальная история публикуется только по
отдельному решению после privacy-аудита всех commits.

## Атомарный способ миграции

1. Создать отдельную ветку или временный worktree от чистого принятого commit.
2. Построить машинный manifest `old_path -> new_path` и проверить его
   биективность: каждый исходный файл встречается один раз, collisions нет.
3. Выполнить все перемещения через `git mv` в одном bounded change.
4. Для каждого локального Markdown destination:
   - разрешить старый target относительно старого положения source;
   - применить manifest к source и target;
   - вычислить новый относительный путь;
   - сохранить query/anchor без изменения.
5. Тем же manifest обновить path-valued YAML scalars, registry entries и явные
   repo-relative paths в тексте. Semantic IDs и coverage targets не менять.
6. Не создавать redirect-файлы по старым путям: Git хранит историю, а redirect
   создаст второй lifecycle и будет маскировать пропущенные ссылки.
7. Запустить полный validation. Только после PASS создать один migration commit.
8. При любой ошибке не выбирать отдельные правки из невалидной миграции, а
   отбросить временную ветку/worktree и повторить перенос из чистой точки.

Скрипт миграции должен поддерживать режим `--check`, который повторно строит
ожидаемый diff и возвращает нулевой diff на уже мигрированном snapshot.

## Критерии проверки миграции

Migration commit допустим только при одновременном выполнении условий:

1. Количество файлов до и после совпадает, кроме явно созданных README/tools
   артефактов следующего этапа.
2. Manifest полон, однозначен и не содержит двух targets для одного source или
   двух sources для одного target.
3. Все YAML/front matter разбираются; semantic IDs уникальны и их множество не
   изменилось.
4. Множество coverage triples `artifact / target / role` не изменилось.
5. Все локальные Markdown-ссылки и anchors разрешаются из нового положения.
6. Все source/path references в YAML и registries существуют.
7. Старые корневые каталоги `docs/`, `matrix/`, `metamodel/`, `pilot/`,
   `registry/`, `reviews/`, `routes/`, `work-packages/` отсутствуют.
8. Вне самой migration map нет ссылок на старые пути.
9. Нет абсолютных локальных путей, secrets, conflict markers, trailing
   whitespace и незапланированных бинарных файлов.
10. Повторный запуск `--check` ничего не записывает и оставляет чистый
    `git status`.
11. README из чистого checkout ведёт к обеим ролевым проекциям, всем 15 track
    cards, B2/B3/B5 content и current-state manifest.
12. Проверенный commit SHA записан в validation report P6.

## Lifecycle и принятие карты

Документ принят владельцем программы 2026-09-19. Принятие разрешает один
атомарный structure migration package, но не принимает README, лицензию, skills,
validators или публичный snapshot.

После принятия следующий bounded шаг — применить карту и подтвердить критерии
1–10. Только затем выполняется P3: создание current-state manifest и инструкции
`load state` уже на стабильных публичных путях.

## Результат применения

Карта применена 2026-09-19 одним structure migration package. Старые корневые
каталоги удалены, compatibility-копии не создавались. Semantic IDs и coverage
остались предметными идентификаторами и не менялись из-за расположения файлов.
Решение зарегистрировано как D-081; следующий этап — P3.
