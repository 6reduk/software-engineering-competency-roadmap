---
id: b2.kata.extract-order-cancellation-policy
kind: kata
title: Kata — выделить policy отмены заказа
owner_track: b2
module: b2.module.service-architecture
coverage:
  - target: b2.level-outcome.design-service-architecture-l1-follow-existing-boundaries
    role: practice
  - target: b2.level-outcome.design-service-architecture-l1-follow-existing-boundaries
    role: assess
  - target: b2.level-outcome.design-service-architecture-l2-structure-typical-feature
    role: practice
  - target: b2.level-outcome.design-service-architecture-l2-structure-typical-feature
    role: assess
  - target: b2.level-outcome.verify-service-behavior-l1-test-local-behavior
    role: practice
  - target: b2.level-outcome.verify-service-behavior-l1-test-local-behavior
    role: assess
  - target: b2.level-outcome.verify-service-behavior-l2-select-test-boundaries
    role: practice
  - target: b2.level-outcome.verify-service-behavior-l2-select-test-boundaries
    role: assess
status: accepted
updated: 2026-08-19
language: ru
---

# Kata: выделить policy отмены заказа

Orders service отвечает на `GET /orders/{order_id}/cancellation-eligibility`. В исходной системе FastAPI router получает ORM order, прямо проверяет `status == CREATED`, вызывает Carrier API и возвращает JSON. Тесты подменяют session, ORM query и конкретный метод HTTP client.

Продукт меняет правило: клиент `PREMIUM` может отменить `PACKED`, если Carrier сообщает, что handoff ещё не начался. Операция только вычисляет eligibility и не пишет данные. Нужно провести изменение, сохранив прежнее HTTP-поведение и не превращая упражнение в переписывание сервиса.

## Владелец scaffold

Участник самостоятельно создаёт минимальный starting scaffold по описанию ниже. Готового repository, структуры файлов и эталонного решения нет. Вы выбираете функции, protocols/interfaces или объекты и объясняете выбор.

Исходный scaffold должен быть намеренно связанным:

- один FastAPI endpoint;
- order с `id`, `status`, `customer_tier` хранится через выбранный минимальный ORM/in-memory imitation;
- Carrier dependency возвращает `handoff_started`;
- router содержит query, policy, downstream call и response mapping;
- tests проверяют вызовы внутренних ORM/HTTP деталей;
- старое правило разрешает только `CREATED`.

Зафиксируйте внешний контракт scaffold в README: ответы для eligible, ineligible и order-not-found. Конкретные status/body выбираются до рефакторинга и затем не меняются.

## Задача

1. Добавьте regression checks прежнего HTTP behavior.
2. Проведите S06 policy change.
3. Выделите минимально достаточные business, application и adapter boundaries.
4. Напишите business-behavior tests для комбинаций status/tier/handoff без FastAPI, DB и сети.
5. Подмените хотя бы один persistence или Carrier adapter fake/in-memory реализацией без изменения application/domain code.
6. Добавьте отдельную проверку mapping реального adapter, который подменяли.
7. Оставьте короткое rationale: исходная боль, выбранная граница и намеренно не введённые abstractions.

Минимальная таблица поведения:

| Status | Tier | Handoff started | Eligibility |
|---|---|---:|---|
| `CREATED` | любой | не требуется для решения | разрешена |
| `PACKED` | `PREMIUM` | false | разрешена |
| `PACKED` | `PREMIUM` | true | запрещена |
| `PACKED` | не `PREMIUM` | любое | запрещена |
| иной | любой | любое | запрещена |

## Наблюдаемые результаты

- прежние endpoint checks проходят без изменения внешнего контракта;
- policy tests не импортируют FastAPI, ORM и HTTP client и падают при возврате старого правила;
- application test запускается с fake/in-memory adapter;
- смена production adapter на fake не требует правки application/domain code;
- adapter check отдельно подтверждает преобразование внешнего ответа во внутренний факт;
- направление импортов не заставляет domain зависеть от adapters;
- rationale перечисляет оставленную связанность и trigger следующего разделения.

Acceptance не требует совпадения с авторской архитектурой, числа файлов или классов. Проверяется поведение и направление зависимостей.

## Non-goals

- готовое решение или обязательная структура каталогов;
- универсальный repository, base service, DI container;
- DB transaction, commit, refund, outbox или событие;
- timeout/retry/pool/cancellation Carrier client — используйте [уже разобранную boundary](../../runtime-concurrency-lifecycle/kata/stop-orphan-work-and-pool-exhaustion.md);
- изменение API contract;
- production deployment и ImplementationReference.

## Критерии самопроверки

- [ ] Исходная история и HTTP behavior описаны до критериев решения.
- [ ] До/после использует один и тот же S06 substrate.
- [ ] Старые случаи и новая таблица policy проверены.
- [ ] Business tests работают без framework runtime и I/O.
- [ ] Минимум один adapter реально заменён без изменения application/domain code.
- [ ] Fake и production mapping проверяются разными тестами.
- [ ] Domain не импортирует FastAPI/ORM/HTTP client.
- [ ] Composition wiring не выдан за доказательство изоляции.
- [ ] Rationale называет минимум одну отвергнутую альтернативу.
- [ ] Намеренно не введённые abstractions и trigger пересмотра записаны.

## Progressive hints

<details>
<summary>Подсказка 1 — найдите причины изменения</summary>

Отметьте отдельно: получение фактов, принятие решения, координацию и HTTP mapping. Посмотрите, какие из них меняются из-за S06, а какие только мешают тесту.

</details>

<details>
<summary>Подсказка 2 — начните с чистого решения</summary>

Добейтесь, чтобы решение из выданной таблицы вычислялось обычным вызовом Python без session и client.

</details>

<details>
<summary>Подсказка 3 — контракт из нужды operation</summary>

Опишите только возможность получить нужный order или handoff fact. Не копируйте весь API ORM/Carrier и не проектируйте generic repository.

</details>

<details>
<summary>Подсказка 4 — разделите доказательства</summary>

Один тест с fake проверяет operation. Другой проверяет, что реальный adapter правильно переводит ORM/HTTP данные. Endpoint check защищает внешний ответ.

</details>

## Вопросы после выполнения

### Что именно стало дешевле менять?

<details>
<summary>Что должен раскрыть ответ</summary>

Назовите обязанности и tests, затронутые S06 до и после. Сильный ответ показывает локализацию policy change, а не уменьшение числа строк или увеличение числа layers.

</details>

### Почему вы не ввели остальные abstractions?

<details>
<summary>Что должен раскрыть ответ</summary>

Для каждой отсутствующей abstraction нет текущей независимой причины изменения или альтернативной реализации. Должен быть назван trigger пересмотра, например вторая операция с тем же capability или transaction requirement.

</details>
