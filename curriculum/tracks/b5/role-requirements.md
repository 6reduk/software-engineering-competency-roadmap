---
artifact: b5-role-requirements-blueprint
title: "Ролевые требования B5"
owner_track: b5
status: accepted
updated: 2026-09-17
language: ru
---

# Ролевые требования B5

[Обе RoleViews](../../roles/role-summary.md) используют одни capabilities. Таблицы задают принятые требования этого blueprint. `required` — обязательная база выбранной специализации; `deepening` — дополнительная глубина; `conditional` — требование только при явно названной ответственности. Отсутствующая связь означает «не задано». L1 не перечислены отдельно: выбранное поведение L2/L3 предполагает объяснение применимой истории, но не создаёт дополнительных role links или evidence.

<a id="backend"></a>

## Backend / Distributed Systems

[Исходная проекция](../../roles/backend-distributed-systems.md).

| Категория | LevelOutcome | Предметное основание категории и условие |
|---|---|---|
| required | `b5.level-outcome.model-partial-failures-l3-defend-tradeoff` | Владелец backend разбирает неизвестный исход запроса, поэтому обязан защищать диагноз при неполном следе. |
| required | `b5.level-outcome.choose-read-guarantees-l2-define-bounded-model` | Backend задаёт обещание чтения своего клиентского пути; ограниченный договор является базой реализации. |
| required | `b5.level-outcome.reconstruct-causal-order-l2-define-bounded-model` | Backend должен самостоятельно сопоставлять события нескольких исполнителей для корректной диагностики. |
| conditional | `b5.level-outcome.exclude-stale-actors-l3-defend-tradeoff` | При владении механизмом lease/ownership backend обязан защищать исключение старого исполнителя у ресурса. |
| deepening | `b5.level-outcome.assess-leadership-guarantees-l2-define-bounded-model` | Оценка quorum-модели расширяет backend-глубину; реализация consensus не входит в общий baseline. |
| conditional | `b5.level-outcome.choose-state-placement-l2-define-bounded-model` | При ответственности за распределённое хранение backend самостоятельно задаёт размещение и путь подтверждения. |
| conditional | `b5.level-outcome.plan-shard-ownership-transfer-l3-defend-tradeoff` | При ownership sharding/rebalancing backend отвечает за записи через старый маршрут и защиту перехода. |
| required | `b5.level-outcome.define-delivery-contract-l2-define-bounded-model` | Backend обязан задать область acknowledgement и replay своего потока до интеграции обработчика. |
| required | `b5.level-outcome.bound-repeat-effects-l3-defend-tradeoff` | Backend отвечает за повторный эффект при неизвестном ответе и должен защитить пределы дедупликации. |
| required | `b5.level-outcome.control-retry-propagation-l3-defend-tradeoff` | Backend владеет прекращением каскада повторов и должен защищать его при перегрузке и неизвестном результате. |
| required | `b5.level-outcome.bound-cache-staleness-l2-define-bounded-model` | Backend обязан определить свежесть клиентского пути при потере invalidation и недоступности источника. |
| required | `b5.level-outcome.control-system-load-l3-defend-tradeoff` | Backend должен защищать полезный прогресс подсистемы при каскаде нагрузки, не присваивая платформенный autoscaling. |
| required | `b5.level-outcome.compose-state-and-publication-l2-define-bounded-model` | Backend обязан связать локальный commit с durable intent публикации в своём потоке изменений. |
| conditional | `b5.level-outcome.choose-cross-system-atomicity-l2-define-bounded-model` | При ответственности за многосервисную бизнес-операцию backend задаёт её промежуточные и неизвестные состояния. |
| conditional | `b5.level-outcome.assess-regional-capacity-l2-define-bounded-model` | При ответственности за регионально распределённую подсистему backend задаёт модель её оставшейся мощности. |
| required | `b5.level-outcome.preserve-mixed-version-contract-l2-define-bounded-model` | Backend обязан задавать допустимые сочетания producers/readers для изменения своего взаимодействия. |
| required | `b5.level-outcome.design-distinguishing-histories-l3-defend-tradeoff` | Backend обязан защитить вывод о гарантии своей подсистемы при неполном следе, а не предъявлять только зелёный запуск. |

<a id="architecture"></a>

## Architecture / Technical Leadership

[Исходная проекция](../../roles/architecture-technical-leadership.md).

Эта проекция относится к Architecture / Technical Leadership с выбранной углублённой специализацией B5 (`depth`); она не задаёт универсальный профиль любого Technical Lead. Здесь `required` означает способность на уровне модели выбрать, защитить или отвергнуть класс решения. Реализовывать протокол согласования (consensus), координатор транзакций или топологию нескольких регионов в каждом проекте не требуется.

По [решению оркестратора](../../../governance/reviews/M2.2-G30-b5-capability-breadth-pass-resolution.md) оценка согласования и лидерства, выбор межсистемной атомарности и оценка региональной мощности остаются `required L3`. Проверка применимости к конкретной системе может привести к аргументированному решению «механизм не нужен»; способность обосновать такой выбор входит в базу выбранной специализации.

| Категория | LevelOutcome | Предметное основание категории и условие |
|---|---|---|
| required | `b5.level-outcome.model-partial-failures-l2-define-bounded-model` | Для согласования границы гарантии архитектору обязательна самостоятельная модель отказов участников. |
| required | `b5.level-outcome.choose-read-guarantees-l3-defend-tradeoff` | Архитектор отвечает за конфликт свежести и доступности между участниками, поэтому защита компромисса обязательна. |
| deepening | `b5.level-outcome.reconstruct-causal-order-l3-defend-tradeoff` | Выбор усиленного порядка углубляет архитектурный анализ цены координации сверх базового чтения истории. |
| required | `b5.level-outcome.exclude-stale-actors-l3-defend-tradeoff` | Архитектор обязан определить authority и цену остановки при смене владельца, иначе договор эффектов неполон. |
| required | `b5.level-outcome.assess-leadership-guarantees-l3-defend-tradeoff` | Выбор места согласования и допустимого прекращения progress является обязательным системным решением архитектора. |
| required | `b5.level-outcome.choose-state-placement-l3-defend-tradeoff` | Архитектор защищает независимость отказов и цену копий, поэтому сравнение placement обязательно. |
| deepening | `b5.level-outcome.plan-shard-ownership-transfer-l3-defend-tradeoff` | Подробный выбор переноса горячего шарда углубляет проектирование состояния сверх общего договора placement. |
| required | `b5.level-outcome.define-delivery-contract-l3-defend-tradeoff` | Архитектор выбирает связь независимых потребителей, поэтому обязан защитить цену удержания и область порядка. |
| required | `b5.level-outcome.bound-repeat-effects-l2-define-bounded-model` | Архитектор обязан самостоятельно определить scope бизнес-идентичности, чтобы разделить ответственность участников. |
| deepening | `b5.level-outcome.control-retry-propagation-l2-define-bounded-model` | Детализация владельца retry и poison-work policy полезна для углубления анализа общего потока. |
| deepening | `b5.level-outcome.bound-cache-staleness-l3-defend-tradeoff` | Разбор гонки заполнения углубляет выбор между доступностью и свежестью, не требуя владеть каждой cache-интеграцией. |
| required | `b5.level-outcome.control-system-load-l3-defend-tradeoff` | Архитектор обязан выбрать межсистемную границу деградации и цену справедливости для участников. |
| required | `b5.level-outcome.compose-state-and-publication-l3-defend-tradeoff` | Архитектор обязан защитить границу outbox/CDC и цену сопровождения без обещания сквозного exactly-once. |
| required | `b5.level-outcome.choose-cross-system-atomicity-l3-defend-tradeoff` | Архитектор выбирает границу атомарности и цену необратимых эффектов, поэтому сравнение с компенсацией обязательно. |
| required | `b5.level-outcome.assess-regional-capacity-l3-defend-tradeoff` | Архитектор обязан защитить locality и резерв при неопределённом спросе; это не передаёт ему B7-допуск. |
| required | `b5.level-outcome.preserve-mixed-version-contract-l3-defend-tradeoff` | Архитектор защищает период совместимости и необратимость эффектов между независимо меняющимися системами. |
| required | `b5.level-outcome.design-distinguishing-histories-l2-define-bounded-model` | Архитектор обязан самостоятельно задать различающие истории, чтобы требование гарантии было проверяемым. |

Backend: 11 required, 1 deepening, 5 conditional. Architecture: 13 required, 4 deepening, 0 conditional. Всего 34 ссылки: 24 required, 5 deepening, 5 conditional. Категории применяются по ответственности, а не ради равного количества: условия backend специализации не становятся универсальной архитектурной реализацией механизмов.

Backend не получает ownership платформы, SRE-процесса или организационной стратегии. Architecture выбирает модель и границы гарантии, а не обязана реализовывать каждый механизм. Эти требования не доказывают proficiency и не повышаются автоматически до summary L4/L5.
