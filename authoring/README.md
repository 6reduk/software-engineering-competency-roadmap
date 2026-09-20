---
id: program.index.authoring-toolkit
kind: index
title: "Набор инструкций для продолжения authoring"
status: accepted
owner: orchestrator
updated: 2026-09-19
language: ru
---

# Authoring toolkit

Этот каталог позволяет продолжить создание и проверку учебных материалов из
чистого контекста. Он не зависит от конкретного LLM-провайдера и не содержит
локальную память, секреты или настройки рабочей машины.

Начинать нужно с [load state](../governance/state/LOAD-STATE.md). Текущий
манифест определяет единственное разрешённое следующее действие; наличие skill
само по себе не разрешает запуск соответствующей работы.

## Канонические правила

- [Content standard](standards/content-standard.md) — глубина и единица
  содержания.
- [Editorial standard](standards/editorial-standard.md) — понятность,
  терминология, измерения и источники.
- [Author workflow](workflow/content-author-workflow.md) — work package,
  Ownership, проверки и handoff.
- [Review protocol](workflow/review-protocol.md) — независимость, findings и
  gate outcomes.
- [Lifecycle boundaries](workflow/lifecycle-boundaries.md) — границы authoring,
  review, correction и acceptance.

## Роли

| Роль | Инструкция | Что производит |
|---|---|---|
| Автор | [learning-material-author](agents/learning-material-author.md) | Только результаты назначенного work package в `review` |
| Технический reviewer | [technical-reviewer](agents/technical-reviewer.md) | Независимый report с техническими findings |
| Learning/editorial reviewer | [learning-editorial-reviewer](agents/learning-editorial-reviewer.md) | Независимый report о понятности, уровнях и практике |
| Оркестратор | [orchestrator](agents/orchestrator.md) | Один bounded следующий шаг, dispositions и отдельное acceptance-решение |

## Skills

| Skill | Когда применять |
|---|---|
| [author-learning-package](skills/author-learning-package/SKILL.md) | Создать или изменить учебный пакет по принятому work package |
| [review-learning-package](skills/review-learning-package/SKILL.md) | Выполнить независимое review без изменения авторских файлов |
| [correct-review-findings](skills/correct-review-findings/SKILL.md) | Закрыть только принятые findings в заданном Ownership |
| [audit-module-state](skills/audit-module-state/SKILL.md) | Пересчитать готовность учебных пакетов, не learner progress |
| [load-program-state](skills/load-program-state/SKILL.md) | Восстановить контекст и назвать ровно один следующий шаг |

Skills — инструкции выполнения, а не новые governance-решения. При конфликте
приоритет имеют явная задача пользователя, принятый current-state manifest,
назначенный work package и канонические стандарты в указанном порядке.
