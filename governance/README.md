---
id: program.index.governance
kind: index
title: "Governance и audit trail программы"
status: accepted
owner: orchestrator
updated: 2026-09-20
language: ru
---

# Governance и audit trail программы

Каталог хранит два разных класса информации. Их нельзя читать как документы
одинаковой нормативной силы.

## Текущее нормативное состояние

Текущие решения определяют:

- [current-state manifest](state/current-state.yaml) — машинный вход Load state;
- [статус программы](state/STATUS.md) — актуальный этап;
- [состояние модулей](state/MODULE-STATE.md) — authoring-state модулей;
- [журнал решений](decisions.md) — принятые решения и superseded-записи;
- [открытые вопросы](state/OPEN-QUESTIONS.md) — незакрытые решения;
- [план публикации](planning/publication-and-continuity-todo.md) — текущая
  последовательность P0–P8.

При расхождении исторического документа с этими источниками применяется более
позднее принятое решение, на которое ссылается manifest.

## Исторический audit trail

- [Reviews](reviews/README.md) сохраняют независимые findings, verdict и
  ограничения конкретного snapshot.
- [Work packages](work-packages/README.md) сохраняют назначенный scope,
  Ownership, Gate 0 и handoff конкретного прохода.

Они публикуются целиком, чтобы можно было проверить происхождение решений и
продолжить работу без истории чата. Это **исторические ненормативные записи**:

- `status: review` в старом отчёте не описывает текущий статус программы;
- отклонённая идея или старый threshold не становится действующим правилом;
- reviewer verdict не заменяет отдельное acceptance-решение;
- Gate 0 автора не доказывает learner execution или production readiness.

## Политика публичной истории

Публичная Git-история начинается с проверенного очищенного snapshot после P6.
Локальные pre-publication commits не отправляются автоматически. Содержимое
reviews/work packages входит в snapshot, но прежняя локальная цепочка коммитов —
только после отдельного all-commit privacy audit.
