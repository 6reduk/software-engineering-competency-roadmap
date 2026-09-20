---
id: program.registry.module-authoring-state
kind: registry
title: "Состояние учебных модулей"
status: accepted
owner: orchestrator
updated: 2026-09-19
language: ru
sources:
  - curriculum/tracks/b2/modules.md
  - curriculum/tracks/b2/module-delivery-plan.md
  - curriculum/tracks/b2/consolidation/module-gates.md
  - curriculum/tracks/b2/consolidation/debt-register.md
  - governance/reviews/M1.8.21-G20-post-s01-consolidation-acceptance.md
  - curriculum/tracks/b3/modules.md
  - curriculum/tracks/b3/phase-closeout.md
  - governance/reviews/M1.9.6-G27-b3-phase-closeout-acceptance.md
  - curriculum/tracks/b5/modules.md
  - curriculum/tracks/b5/phase-closeout.md
  - governance/reviews/M2.5-G33-b5-phase-closeout-acceptance.md
  - governance/state/PROGRAM-AUTHORING-CLOSEOUT.md
---

# Состояние учебных модулей

## Что именно закрывается

Этот реестр фиксирует **готовность учебного пакета**, а не обучение конкретного
человека. Самостоятельное чтение, выполнение kata и проектов, выбор консультанта
или LLM и оценка результата находятся вне authoring lifecycle репозитория.

Разделяются три независимые оси:

1. **Authoring state** — достаточно ли карты и материалов для самостоятельного
   использования модуля в объявленной границе текущего выпуска.
2. **Learner progress** — что конкретный пользователь прочитал и выполнил. Это
   состояние не хранится в каноническом реестре программы.
3. **Proficiency evidence** — подтверждает ли работа пользователя конкретные
   LevelOutcomes. Способ проверки выбирает сам пользователь; репозиторий не
   присваивает ему грейд автоматически.

Исторические [B2 gate cards](../../curriculum/tracks/b2/consolidation/module-gates.md) связывали
готовность gate с выполненной реализацией участника. После принятого завершения
authoring M3.1 эти карточки сохраняются как полезная rubric будущей проверки
работы, но не являются каноническим блокером готовности учебного пакета.

## Статусы authoring

| Статус | Значение |
|---|---|
| `closed-for-authoring` | В объявленной границе текущего выпуска существует самостоятельный маршрут, его материалы приняты, обязательные L1–L3 действия покрыты, а остаточные специализации явно вынесены в долг. Новое authoring не требуется без trigger |
| `partial` | Часть глубокого маршрута принята, но остаётся конкретный пробел L1–L3 либо незавершённая capability внутри scope модуля |
| `blueprint-only` | Определены module/capabilities/outcomes/scenarios, но глубокий самостоятельный маршрут ещё не создан |
| `not-started` | Не определена даже предметная карта модуля. Среди 27 модулей B2/B3/B5 таких нет |

`closed-for-authoring` не означает, что навсегда запрещено расширение. Условия
возврата — реальная задача, установленный пробел текущего маршрута или новый
масштаб ответственности, который нельзя честно выразить существующими
материалами. L4/L5 с реальным межкомандным внедрением сохраняются как отдельная
глубина и не подменяются дополнительным лабораторным текстом.

## Gate текущего выпуска

Модуль можно закрыть для authoring, если одновременно выполнены условия:

1. Границы module, capabilities и non-goals приняты.
2. Существует навигационный вход и самостоятельный маршрут из объяснения,
   диагностической проверки, ограниченной практики и интеграционного задания;
   переиспользование принятого материала разрешено и явно связано.
3. Для всех применимых L1–L3 outcomes внутри `Develops` есть принятое назначение
   материала, а задания содержат проверяемый результат и предел вывода.
4. Нет blocker/major findings принятого review, относящихся к содержанию маршрута.
5. Непокрытые L4/L5, специализации и readiness вынесены в долг с owner и trigger,
   а не скрыты заявлением о полном освоении вертикали.
6. Отдельное решение этого реестра принято оркестратором.

ImplementationReference, выполненный проект пользователя и оценка его навыка в
этот gate не входят.

## Итог

| Вертикаль | Всего модулей | `closed-for-authoring` | `partial` | `blueprint-only` | `not-started` |
|---|---:|---:|---:|---:|---:|
| B2 Backend & API Engineering | 10 | 8 | 2 | 0 | 0 |
| B3 Transactional Data & Storage | 11 | 2 | 0 | 9 | 0 |
| B5 Distributed Systems & System Design | 6 | 0 | 1 | 5 | 0 |
| **Итого** | **27** | **10** | **3** | **14** | **0** |

Остальные 12 вертикалей имеют программные track cards и ролевые ориентиры, но не
имеют собственных module catalogs. Их состояние — `track-skeleton-only`; они не
включаются в приведённые 27 модулей и не выдаются за `not-started` модули с
вымышленными границами.

## B2 — Backend & API Engineering

Источники: [module definitions](../../curriculum/tracks/b2/modules.md), принятый
[coverage audit](../../curriculum/tracks/b2/module-delivery-plan.md) и
[G20](../reviews/M1.8.21-G20-post-s01-consolidation-acceptance.md). У всех десяти
модулей есть пятижанровый маршрут. Решение ниже отделяет текущую L1–L3 готовность
материалов от L4 adoption и learner execution.

| Модуль | Состояние | Основание решения | Сохранённый долг / trigger |
|---|---|---|---|
| HTTP Service Runtime | `closed-for-authoring` | Полный маршрут tracing/lifecycle/cancellation; membership 11/11, все L1–L3 имеют accepted material | L4 policy и production-scale tracing возвращаются только по межсервисной задаче; S12 — по отдельному distinct mechanism |
| Evolvable API Contracts | `partial` | Полный жанровый маршрут есть, membership 19/16 | Не покрыт Evolution L1 — заданное additive изменение; L4 migration/conventions остаются отдельной глубиной |
| Identity / API Security Boundaries | `closed-for-authoring` | Identity и operation-cost Abuse L1–L3 имеют принятые самостоятельные маршруты; membership 16/13, три пробела относятся к L4 | Callback/SSRF и aggregate quota/rate возвращаются только отдельными bounded пакетами с readiness |
| Service Architecture | `closed-for-authoring` | S06 образует полный маршрут Architecture L1–L3; membership 12/9, три пробела относятся к L4 | Межкомандные conventions/adoption — отдельный L4 trigger |
| Transactional Persistence Integration | `closed-for-authoring` | S07 и S15 дают самостоятельные Transaction, Idempotency и Cache действия L1–L3; membership 13/10, три пробела относятся к L4 | Distributed cache coordination, cross-service idempotency и Verification L4 возвращаются по реальной задаче |
| External Service Integration | `closed-for-authoring` | Собственный S08 flow и принятый reuse runtime дают External L1–L3; membership 11/10, единственный непокрытый outcome — L4 | Политика нескольких интеграций и новый failure mechanism требуют отдельного trigger |
| Background / Message Workflows | `closed-for-authoring` | S09 даёт самостоятельные Workflow L2/L3 и необходимые supporting routes; membership 10/8, два пробела относятся к L4 | Cross-team workflow/idempotency policy и иной broker contract — отдельная глубина |
| Service Verification | `closed-for-authoring` | S10 покрывает Verification и Compatibility L1–L3; membership 12/10, непокрытые outcomes относятся к L4 | Cross-team evidence/compatibility adoption возвращаются только при реальной ответственности нескольких команд |
| Safe Service Evolution | `partial` | Delivery L1–L3 имеет принятый маршрут, membership 12/10 | Supporting Evolution L1 остаётся непокрытым; Delivery/Evolution/Compatibility L4 сохраняются как adoption debt |
| Performance / Resource Control | `closed-for-authoring` | Полный маршрут диагностики, bounds, lifecycle и cancellation; membership 14/14 | L4 представлен только reasoning/probe и возвращается по cross-service capacity задаче; S12 требует distinct mechanism |

Решение закрывает D27 в части **authoring-state decisions**: десять решений теперь
существуют. D01 и другие содержательные долги не удаляются; learner execution и
ImplementationReference из D20/D26 остаются вне scope программы, а не блокерами
этого реестра.

## B3 — Transactional Data & Storage

Источники: [module definitions](../../curriculum/tracks/b3/modules.md),
[phase close-out](../../curriculum/tracks/b3/phase-closeout.md) и
[G27](../reviews/M1.9.6-G27-b3-phase-closeout-acceptance.md).

| Модуль | Состояние | Основание решения | Сохранённый долг / trigger |
|---|---|---|---|
| Сохранять инварианты в конкурентных транзакциях | `blueprint-only` | Приняты подробные capabilities/outcomes/scenarios, но пятижанрового маршрута нет | Возврат по конкретной задаче write-skew/conflict, которой недостаточно B2 S07 |
| Выражать правила данных реляционной схемой | `blueprint-only` | Есть карта RM01, глубокого маршрута нет | Возврат по задаче моделирования/constraint с различимым результатом |
| Получать корректный результат запроса | `closed-for-authoring` | SQ01: пять accepted материалов, обе capabilities и все шесть L1–L3 outcomes покрыты | Новая SQL-глубина только по отличающемуся классу ошибки, не повторяющему join/grain |
| Объяснять сохранность и восстановление состояния | `blueprint-only` | Есть карта WR01, глубокого маршрута нет | Требуется доступная engine-level crash/recovery среда и задача роли |
| Улучшать доступ к данным по плану запроса | `blueprint-only` | Есть карта IO01, глубокого маршрута нет | Возврат по реальному plan/index trade-off и измеримой оснастке |
| Изменять схему с сохранением совместимости | `closed-for-authoring` | SE01: пять accepted материалов, обе capabilities и все шесть L1–L3 outcomes покрыты | Production migration, неизвестные consumers и L4 adoption остаются отдельным trigger |
| Сохранять гарантии store при смене узла | `blueprint-only` | Есть карта RH01, глубокого маршрута нет | Нужна различимая failover-среда без перехода в B5/B7 |
| Масштабировать workload в пределах гарантий store | `blueprint-only` | Есть карта PS01, глубокого маршрута нет | Возврат по partitioning/connection-scale задаче с измеримым пределом |
| Проверять восстанавливаемость данных store | `blueprint-only` | Есть кандидат BR01, глубокого маршрута нет | Нужна доступная backup/PITR среда и bounded recovery objective |
| Поддерживать работоспособность и контролируемый доступ | `blueprint-only` | Есть карта SO01, глубокого маршрута нет | Возврат по engine-specific access/maintenance задаче |
| Выбирать и проверять operational store | `blueprint-only` | Есть карта ON01, глубокого маршрута нет | Нужен конкретный nonrelational contract и доступная среда |

## B5 — Distributed Systems & System Design

Источники: [module definitions](../../curriculum/tracks/b5/modules.md),
[phase close-out](../../curriculum/tracks/b5/phase-closeout.md) и
[G33](../reviews/M2.5-G33-b5-phase-closeout-acceptance.md).

| Модуль | Состояние | Основание решения | Сохранённый долг / trigger |
|---|---|---|---|
| Допустимый результат при частичном отказе | `blueprint-only` | Есть FM01/CA01 и outcomes, глубокого маршрута нет | Возврат по доступной unknown-outcome либо read-guarantee лаборатории |
| Право на действие при смене владельца | `partial` | TO01/fencing даёт один принятый маршрут и 8 из 9 L1–L3 outcomes | Не покрыт Leadership L3; partition/crash/unknown outcome и обход проверки остаются ограничениями опыта |
| Размещение состояния и цена отказа | `blueprint-only` | Есть RS01/CM01, глубокого маршрута нет | Нужна задача placement/transfer/capacity с доступными наблюдениями |
| Доставка и бизнес-эффекты | `blueprint-only` | Есть ME01/IR01/DT01, глубокого маршрута нет | Возврат по distinct delivery/effect composition, не повторяющей B2 S07/S09 |
| Устаревание и перегрузка | `blueprint-only` | Есть LC01, глубокого маршрута нет | Нужна системная, а не прикладная cache/load задача |
| Межсистемный договор при эволюции | `blueprint-only` | Есть EV01, глубокого маршрута нет | Нужны mixed-version histories и отдельная проверяемая гарантия |

## Непокрытые вертикали

Для A1, A2, A3, B1, B4, B6, B7, B8, B9, B10, B11 и C1 уже существуют
track cards и ролевые target summaries. Собственных module/capability/outcome
blueprints этих вертикалей пока нет. Их корректное состояние —
`track-skeleton-only`, а не 12 скрытых очередей authoring.

Новая детализация начинается только по return triggers из
[program close-out](PROGRAM-AUTHORING-CLOSEOUT.md), а не потому, что число
неуглублённых вертикалей больше нуля.

## Следующая проверка состояния

Повторный module-state audit нужен только когда произошло одно из событий:

- принят новый или изменён существующий глубокий маршрут;
- исправлен L1–L3 пробел partial-модуля;
- изменены module scope либо capability membership;
- зарегистрирован предметный долг, меняющий границу самостоятельного маршрута;
- отдельное решение возвращает L4/L5 adoption в authoring scope.

На неизменном наборе принятых материалов повторный аудит обязан вернуть
`10 closed / 3 partial / 14 blueprint-only / 0 not-started`.
