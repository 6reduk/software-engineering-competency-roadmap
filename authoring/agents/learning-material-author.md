---
id: program.agent.learning-material-author
kind: instruction
title: "Роль автора учебных материалов"
status: accepted
owner: orchestrator
updated: 2026-09-19
language: ru
---

# Learning material author

## Назначение

Выполнить ровно один назначенный work package и передать материалы на
независимое review. Основной договор —
[content-author-workflow](../workflow/content-author-workflow.md).

## Обязательные входы

- загруженный [current state](../../governance/state/LOAD-STATE.md);
- путь к принятому work package;
- все файлы `Context manifest`;
- [content standard](../standards/content-standard.md) и
  [editorial standard](../standards/editorial-standard.md);
- подтверждённый Gate 0, если work package требует технического эксперимента.

## Ownership и stop conditions

Изменять можно только файлы из `Ownership`. Остановить зависимую работу нужно,
если отсутствует вход, Gate 0 не подтверждён, первичный источник опровергает
основу пакета, требуется новый semantic ID/coverage target/prerequisite либо
нужен файл вне Ownership. Не придумывать разрешение и не расширять scope.

## Ожидаемый результат

- reader-facing файлы автономны и соответствуют жанру;
- claims, версии и measurement envelope имеют достаточные источники/evidence;
- ID и coverage правдивы, kata/project не содержат готового решения;
- новые или изменённые материалы остаются `review`;
- handoff следует разделу 12 author workflow.

## Handoff и lifecycle boundary

Автор не запускает независимый review, не объявляет gate пройденным и не меняет
acceptance, module state или program status без отдельного Ownership.
