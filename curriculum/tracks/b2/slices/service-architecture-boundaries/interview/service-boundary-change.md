---
id: b2.interview.service-boundary-change
kind: interview
title: Interview — изменение границ Orders service
owner_track: b2
module: b2.module.service-architecture
coverage:
  - target: b2.level-outcome.design-service-architecture-l1-follow-existing-boundaries
    role: probe
  - target: b2.level-outcome.design-service-architecture-l2-structure-typical-feature
    role: probe
  - target: b2.level-outcome.design-service-architecture-l3-reshape-changing-service
    role: probe
  - target: b2.level-outcome.verify-service-behavior-l1-test-local-behavior
    role: probe
  - target: b2.level-outcome.verify-service-behavior-l2-select-test-boundaries
    role: probe
status: accepted
updated: 2026-08-19
language: ru
---

# Interview: изменение границ Orders service

Orders service предоставляет read-only `GET /orders/{order_id}/cancellation-eligibility`. Сейчас FastAPI router загружает ORM-модель, разрешает отмену только для `CREATED`, напрямую вызывает Carrier API, собирает ответ и тестируется моками FastAPI, ORM session и HTTP client.

Новое требование: клиент `PREMIUM` может отменить заказ `PACKED`, пока Carrier сообщает, что handoff ещё не начался. Операция ничего не записывает: нет commit, refund, события и удалённого side effect. Сохраните существующий HTTP behavior для прежних случаев.

## Основной вопрос

Как вы проведёте изменение так, чтобы решение можно было проверить без FastAPI, БД и сети, а persistence или Carrier adapter — заменить fake/in-memory реализацией без правки application/domain code?

<details>
<summary>Ориентиры сильного ответа</summary>

Кандидат сначала фиксирует старое поведение и путь изменения, а не называет Clean Architecture. Он отделяет чистую policy от application coordination, delivery mapping и внешних adapters; задаёт зависимости внутрь; оставляет wiring в composition root. Он предлагает минимальные порты по нуждам operation, business tests без I/O и отдельные integration checks mapping. Допускаются функции, protocols или небольшие objects.

</details>

## Последовательные follow-ups

### 1. Где именно вы видите coupling?

<details>
<summary>Ожидаемое рассуждение</summary>

Один policy change заставляет согласованно менять несколько обязанностей и моки implementation details. Кандидат перечисляет change surface до рефакторинга. «Router длинный» — симптом, не достаточный диагноз.

</details>

### 2. Какие входы принадлежат policy, а какие operation?

<details>
<summary>Ожидаемое рассуждение</summary>

Policy нужны status, tier и handoff state, а не ORM row или HTTP response. Operation получает order, решает, нужен ли Carrier fact, вызывает policy и возвращает прикладное решение. Способ оптимизации сетевого вызова допустимо выбрать по ограничениям, если он не просачивается в policy.

</details>

### 3. Нужны ли OrderRepository, CarrierGateway и DI container?

<details>
<summary>Ожидаемое рассуждение</summary>

Не обязательно. Нужен минимальный контракт там, где есть независимая причина изменения или требование подмены. Универсальный CRUD repository и container могут добавить стоимость без новой гарантии. Кандидат называет trigger, при котором abstraction окупится.

</details>

### 4. Как сохранить HTTP behavior?

<details>
<summary>Ожидаемое рассуждение</summary>

Зафиксировать targeted endpoint checks для прежних статусов, not-found и error mapping; delivery adapter переводит прикладной результат в тот же status/body. Фактическая HTTP boundary проверяется отдельно от policy. Полный пересказ FastAPI lifecycle не нужен.

</details>

### 5. Как мигрировать без big-bang rewrite?

<details>
<summary>Ожидаемое рассуждение</summary>

Characterization tests → чистая policy внутри текущего пути → application operation → один порт в точке давления → реальные adapters и wiring → S06. Каждый шаг сохраняет внешний контракт и имеет собственную проверку; старый путь удаляется после сравнения результатов.

</details>

### 6. Какие тесты докажут результат и чего они не докажут?

<details>
<summary>Ожидаемое рассуждение</summary>

Табличные policy tests доказывают комбинации CREATED/PACKED, tier и handoff без I/O. Application test с fake adapter доказывает координацию и заменяемость. ORM, Carrier HTTP и endpoint checks доказывают mapping реальных границ. Fake не доказывает production adapter; зелёный E2E плохо локализует причину.

</details>

### 7. Как наблюдаемо показать уменьшение change risk?

<details>
<summary>Ожидаемое рассуждение</summary>

Провести ещё одно маленькое изменение policy и перечислить затронутые обязанности/проверки до и после. Сильный результат локализован в policy/application tests и не требует согласованных правок router, ORM и HTTP client. Проценты и число файлов не нужны.

</details>

### 8. Что изменится, если eligibility начнёт записывать решение?

<details>
<summary>Ожидаемое рассуждение</summary>

Появится вопрос transaction boundary, commit/rollback и согласования side effects. Это S07 и отдельный пакет. Здесь достаточно назвать будущую границу; проектировать unit of work/outbox нельзя выдавать за часть текущего решения.

</details>

### 9. L4 follow-up: как распространить подход на несколько команд?

<details>
<summary>Граница ответа</summary>

Можно обсудить conventions, исключения, миграцию и обратную связь от нескольких use cases. Но ответ на интервью — только reasoning. Без межкомандного adoption/execution evidence он не подтверждает L4 и не входит в coverage этого материала.

</details>

## Rubric

| Уровень | Наблюдаемый ответ |
|---|---|
| L1 | Следует уже заданной границе, не вводит обратный import и предлагает локальный regression test, обнаруживающий целевую ошибку. Нуждается в подсказке, где провести boundary. |
| L2 | Самостоятельно разделяет policy, operation и adapters для типовой feature; объясняет dependency direction, выбирает policy/application/adapter tests и учитывает стоимость abstraction. |
| L3 | Начинает с evidence исходной боли, сравнивает минимум две альтернативы, строит incremental migration и предлагает повторное изменение как проверку уменьшения change surface. Удерживает transaction и L4 scope за границей. |

Количество названных patterns, layers и acronyms не повышает уровень. Interview имеет роль `probe`: даже сильное рассуждение не заменяет execution evidence kata или проекта.

## Частые слабые ответы

| Ответ | Какой пробел диагностирует |
|---|---|
| «Перепишем на Clean Architecture» | Нет локальной боли, migration plan и критерия эффекта |
| «Сделаем OrderService» | Название не разделяет причины изменения; возможен god object |
| «Замокаем DB и HTTPX» | Привязка к реализации вместо business behavior |
| «Каждой таблице нужен repository» | Механическое применение pattern без port need |
| «Все модели должны быть отдельными» | Количество типов подменяет анализ ownership и mapping |
| «DI решит coupling» | Wiring перепутан с dependency direction и данными |
| «Один E2E всё докажет» | Не разделены business и adapter evidence, слабая локализация отказа |
