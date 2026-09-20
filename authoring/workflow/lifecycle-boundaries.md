---
id: program.standard.authoring-lifecycle-boundaries
kind: standard
title: "Границы жизненного цикла учебных материалов"
status: accepted
owner: orchestrator
updated: 2026-09-19
language: ru
---

# Lifecycle boundaries

## Состояния и переходы

| Этап | Допустимый результат | Чего этап не доказывает |
|---|---|---|
| Planning | Bounded objective, Ownership, constraints и stop conditions | Готовность среды, корректность содержания или разрешение на authoring |
| Gate 0 | Пригодность конкретной среды и проверяемость технической основы | Production readiness, среду ученика или качество будущего материала |
| Authoring | Файлы Ownership в `review` и проверяемый handoff | Независимость проверки или acceptance |
| Independent review | Findings и verdict в отдельном review artifact | Автоматическое исправление или acceptance автором |
| Correction | Закрытие назначенных findings с сохранением инвариантов | Повторный полный review или acceptance |
| Acceptance | Решение оркестратора с dispositions и границами claims | Learner execution, proficiency, module closure или release |
| Module-state audit | Готовность учебного пакета в объявленном authoring scope | Прохождение программы конкретным человеком |
| Publication | Доступный воспроизводимый snapshot | Истинность будущих пользовательских реализаций |

Переход выполняется только отдельным разрешённым действием. Нельзя повышать
статус потому, что механические проверки прошли или следующий этап кажется
очевидным.

## Общие инварианты

- `Ownership` — верхняя граница допустимых изменений, а не требование изменить
  каждый перечисленный файл.
- Автор и независимый reviewer не являются одной ролью в одном gate.
- Reviewer не редактирует проверяемые материалы.
- Correction-pass закрывает только назначенные findings и explicit dispositions.
- Acceptance, program status и module state меняет только оркестратор в явно
  разрешённом scope.
- Coverage описывает связь материала с целью, а не proficiency пользователя.
- Gate 0 предшествует технически зависимому authoring; провал stop condition
  запрещает зависимую часть authoring.
- Learner execution и подтверждение навыков находятся вне authoring lifecycle.

## Универсальный handoff

Каждая роль передаёт:

1. точный набор созданных и изменённых файлов;
2. проверенные утверждения и ограничения evidence;
3. сохранённые инварианты;
4. открытые вопросы и долг;
5. следующий допустимый lifecycle-переход, не объявляя его выполненным.
