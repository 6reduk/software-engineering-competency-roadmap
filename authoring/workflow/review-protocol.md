---
artifact: review-protocol
status: accepted
updated: 2026-08-14
---

# Протокол независимого ревью

## Принцип

Автор и reviewer — разные агенты. Reviewer не редактирует артефакт, а возвращает findings. Основной агент сопоставляет замечания, принимает решения и вносит изменения. Это предотвращает конфликтующие правки и сохраняет единое авторство.

Review выполняется после bounded work package, а не после каждого файла. Иначе стоимость координации превысит пользу.

## Роли ревью

### Structure reviewer

Проверяет границы, декомпозицию, навигацию, дублирование, prerequisites и соответствие метамодели.

### Subject-matter reviewer

Проверяет техническую корректность, достаточную глубину, edge cases, первичные источники и отсутствие устаревших практик.

### Learning/interview reviewer

Проверяет полезность как конспекта, ясность ментальной модели, качество вопросов, практических заданий и соответствие ожидаемому уровню. В отдельном compression-pass удаляет энциклопедические повторы: каждый абзац должен помогать объяснить, применить, диагностировать или выбрать решение.

Для обычного пакета достаточно двух независимых reviewers. Третий подключается для высокорисковых тем или release gate.

## Формат finding

```yaml
severity: blocker | major | minor | note
artifact: path-or-id
criterion: correctness | scope | structure | level | practice | freshness
finding: что обнаружено
evidence: почему это проблема
recommendation: минимальное исправление
```

## Правила принятия

- `blocker` — пакет не принимается;
- `major` — исправляется до acceptance либо оформляется явное решение с обоснованием;
- `minor` — может быть перенесён в backlog;
- `note` — рекомендация без обязательства.

Количество замечаний не является метрикой качества reviewer. Дублирующиеся findings объединяются. Противоречия разрешаются через цели программы, primary sources и decision log, а не голосованием агентов.

## Review gates

| Gate | Проверяется | Обязательные reviewers |
|---|---|---|
| G1 Meta-model | Однозначность сущностей и ownership | Structure + learning |
| G2 Skeleton matrix | Покрытие и границы треков | Structure + domain |
| G3 Pilot blueprint | Capabilities и уровни | Domain + learning |
| G4 Thin slice | Полный learning flow | Domain + learning/interview |
| G4b Contrast slice | Переносимость шаблонов на другой тип материала | Structure + learning/interview |
| G5 Module | Качество bounded content package | Domain + один релевантный reviewer |
| G6 Track release | Целостность, навигация, freshness | Все три роли |

## Завершение review

Для каждого gate сохраняются:

- scope и версия проверяемого пакета;
- findings;
- решение по каждому blocker/major;
- список внесённых изменений;
- итог `accepted`, `accepted-with-debt` или `rework`.
