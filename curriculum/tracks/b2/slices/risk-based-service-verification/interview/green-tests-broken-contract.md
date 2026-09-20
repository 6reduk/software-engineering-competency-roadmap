---
id: b2.interview.green-tests-broken-contract
kind: interview
title: Интервью — зелёные тесты, сломанный HTTP-контракт
owner_track: b2
module: b2.module.service-verification
coverage:
  - target: b2.level-outcome.verify-service-behavior-l1-test-local-behavior
    role: probe
  - target: b2.level-outcome.verify-service-behavior-l2-select-test-boundaries
    role: probe
  - target: b2.level-outcome.verify-service-behavior-l3-design-service-strategy
    role: probe
  - target: b2.level-outcome.verify-contract-compatibility-l1-maintain-contract-check
    role: probe
  - target: b2.level-outcome.verify-contract-compatibility-l2-detect-breaking-change
    role: probe
  - target: b2.level-outcome.verify-contract-compatibility-l3-build-consumer-evidence
    role: probe
status: accepted
updated: 2026-08-20
language: ru
last_verified: 2026-08-20
versions:
  fastapi: 0.136.3
  starlette: 1.3.1
  pydantic: 2.13.4
---

# Интервью: зелёные тесты, сломанный HTTP-контракт

Материал оценивает ход рассуждения, а не знание названий тестов. Interview даёт роль `probe`: даже сильный разговорный ответ не заменяет исполненную kata или service-level project.

## История системы

Новый клиент вызывает `POST /orders` с `Accept: application/problem+json`. Для `delivery.mode="scheduled"` обязательны `window.start` и `window.end`. Клиент отправляет:

```json
{
  "customer_id": "c-42",
  "items": [{"product_id": "p-7", "quantity": 1}],
  "delivery": {
    "mode": "scheduled",
    "window": {"start": "2026-08-21T10:00:00Z"}
  }
}
```

Он ожидает HTTP `422`, `Content-Type: application/problem+json` и:

```json
{
  "type": "https://api.example.test/problems/invalid-delivery-window",
  "title": "Invalid delivery window",
  "status": 422,
  "detail": "The delivery window is incomplete",
  "errors": [
    {"pointer": "#/delivery/window/end", "code": "required"}
  ]
}
```

Клиент принимает решение по status и `type`, а pointer использует для подсветки формы. Текст `detail` он не разбирает.

Все текущие проверки зелёные:

- domain/application tests проверяют правила заказа;
- прямой тест Pydantic-модели подтверждает, что неполное окно отклоняется;
- router/handler unit test использует близкий mock/fake и не запускает фактические exception handlers, serialization и HTTP response.

В собранном приложении handler для `RequestValidationError` не зарегистрирован либо зарегистрирован не для того exception type. Фактический ответ — `422 application/json` с framework-specific `detail`.

## Основной вопрос

Почему все проверки зелёные и какая минимальная следующая проверка даст правдивый сигнал до rollout?

<details>
<summary>Ожидаемое сильное рассуждение</summary>

Зелёные сигналы относятся к другим утверждениям: domain rule корректно, модель отвергает input, mapper/handler работает при прямом вызове. Они не собирают приложение и не запускают выбор exception handler, поэтому дефект невозможен внутри их границ.

Минимальный следующий check вызывает собранное FastAPI application через ASGI/HTTP path точным запросом и наблюдает status, нормализованный media type и используемые клиентом семантические поля. Он не обязан запускать proxy и deployment: для дефекта wiring достаточно in-process application. Прямой вызов serializer или полный OpenAPI snapshot снова не воспроизведут mechanism.

</details>

## Последовательные follow-ups

### 1. Сформулируйте риск и механизм, не называя тип теста

<details>
<summary>Ожидаемый ответ</summary>

Риск: новый клиент не распознает исправимую ошибку и не подсветит `delivery.window.end`. Механизм: request validation создаёт `RequestValidationError`; composition root должен сопоставить exception с handler; handler формирует Problem Details; response serialization отправляет status, headers и body. Seeded defect находится в регистрации/type matching, а не в бизнес-правиле.

</details>

### 2. Какие две проверки лучше всего локализуют отказ?

<details>
<summary>Ожидаемый ответ</summary>

Быстрый component check подтверждает, что точный invalid input создаёт validation error для отсутствующего `window.end`. Assembled HTTP check подтверждает публичный ответ. Если первая зелёная, а вторая красная, область поиска — assembly, exception mapping или serialization. Повторение полного body assertion на каждом уровне локализацию не улучшает.

</details>

### 3. Что именно проверять в HTTP-ответе и чего не закреплять?

<details>
<summary>Ожидаемый ответ</summary>

Проверять реальный HTTP status `422`, media type `application/problem+json`, стабильные `type`, `title`, `status` и наличие `errors` с нужными pointer/code. Не закреплять порядок JSON-полей, внутренние `loc/msg/type` Pydantic и точное строковое представление заголовка с несущественными параметрами. `detail` — человекочитаемый текст, а не программный код.

</details>

### 4. Как назвать стоимость и остаточный риск решения?

<details>
<summary>Ожидаемый ответ</summary>

Один in-process HTTP check медленнее model test, но дешёв относительно deployment E2E и хорошо локализуется в паре с component check. Он не включает proxy, TLS, сетевой stack, production configuration и настоящий код клиента. Если эти механизмы имеют существенный риск, нужны отдельные проверки; автоматически расширять текущий test не следует.

</details>

## Изменение условий

### 5. Дефект появляется только при сборке приложения

Любой прямой вызов handler и serializer проходит. Как меняется выбор?

<details>
<summary>Ожидаемый ответ</summary>

Граница обязана включать production-like app factory/composition root. Можно подменить БД и внешние сервисы, потому что они не участвуют в механизме, но нельзя собирать отдельное test application с вручную подключённым handler: это удалит дефект. Проверка должна получать приложение тем же способом, который регистрирует routes и exception handlers для запуска сервиса.

</details>

### 6. Несколько клиентов используют разные части error contract

Новый UI использует status, `type` и pointer. Legacy operations script для корректного заказа использует `201` и `order_id`, а при invalid request только останавливается по `422`; содержимое Problem Details он не читает. Какие checks нужны?

<details>
<summary>Ожидаемый ответ</summary>

Нужно вести inventory версий/ожиданий и проверять только реально используемые части. UI check подтверждает status, media type, `type` и pointer. Script check подтверждает `201/order_id` для успеха и `422` для invalid case; не надо копировать UI assertions. Schema diff может быть дополнительным ранним сигналом, но migration/release decision опирается на semantic checks двух представителей и известные остаточные риски.

</details>

### 7. HTTP check стал медленным и нестабильным

Команда предлагает либо удалить его, либо скопировать весь сценарий в один deployment E2E. Что исследовать?

<details>
<summary>Ожидаемый ответ</summary>

Сначала локализовать источник стоимости/flakiness и уникальный механизм проверки. Если instability приходит от ненужной БД или сети, их можно заменить, сохранив настоящий app assembly и exception path. Если несколько HTTP checks повторяют одни semantic assertions, оставить представителя для wiring и перенести combinatorial validation в component tests. Удаление допустимо после fault injection: оставшийся portfolio должен ловить те же критические seeded failures, а заранее выбранная метрика стоимости/локализации — улучшиться.

</details>

### 8. Как превратить исправление одной регрессии в strategy одного сервиса?

<details>
<summary>Ожидаемый ответ</summary>

Сначала составляют перечень критических путей и способов отказа сервиса, а также фиксируют ожидания представительных клиентов. Для каждого риска затем определяют:

- механизм отказа;
- самую дешёвую правдивую границу проверки;
- сигнал сбоя и способ локализации причины;
- стоимость проверки и остаточный риск.

После этого измеряют текущий набор проверок, вносят несколько отказов с разными механизмами, удаляют хотя бы одну доказанно медленную, нестабильную и дублирующую проверку и повторяют измерение в тех же условиях. Проценты unit/integration/E2E не являются целью.

</details>

## Rubric

| Уровень рассуждения | Наблюдаемые признаки |
|---|---|
| L1 | По заданному подходу формулирует HTTP assertions, которые ловят регрессию, и не закрепляет несущественные детали |
| L2 | Самостоятельно связывает риск с mechanism, выбирает границу сборки/HTTP, сохраняет локализующую component check и называет стоимость/остаточный риск |
| L3 | Перестраивает portfolio одного сервиса: inventory paths/consumers, разные mechanisms, измерение до/после, удаление duplication без потери critical-path evidence |

Количество тестов, перечисление `unit/integration/E2E` или знание конкретного framework не повышают уровень. Различие создают автономность, причинная связь, масштаб решения и проверяемое evidence.

## Слабые ответы и диагностируемые пробелы

- **«Добавлю больше unit-тестов».** Не названы риск, механизм и граница.
- **«Нужен E2E, он проверит всё».** Не учитываются стоимость, локализация и отсутствующие/лишние механизмы.
- **«Схема OpenAPI зелёная».** Смешаны описание и фактический wire behavior.
- **«Замокаем exception handler».** Из проверки удаляется seeded defect.
- **«Проверим весь JSON snapshot».** Контракт клиента смешан с несущественными деталями.
- **«Оставшийся риск нулевой».** Граница доказательства не осознана.
- **«Сделаем 70% unit tests».** Процент не связан с критическими failure modes.

## L4 follow-up: где заканчивается этот slice

Как согласовать общие verification expectations нескольких команд?

<details>
<summary>Признаки сильного ответа, но не L4 evidence</summary>

Нужны risk-based expectations, допустимые stack-specific реализации, ownership/exceptions, staged adoption и реальные release decisions минимум нескольких команд с feedback loop. Интервью и локальный Orders project могут подготовить reasoning, но не подтверждают cross-team adoption. Поэтому L4 coverage здесь не заявляется.

</details>

## Короткий словарь для интервьюера

- **Граница проверки (`test boundary`)** — интерфейс воздействия и наблюдения; здесь прямой вызов модели, собранное ASGI application или consumer-facing HTTP contract.
- **Покрытие механизма (`mechanism coverage`)** — присутствует ли в проверке причинная цепочка, способная породить исследуемый отказ.
- **Ложная уверенность (`false confidence`)** — зелёный сигнал, ошибочно расширенный на поведение за пределами проверенной границы.
- **Остаточный риск (`residual risk`)** — риск, который выбранный набор намеренно не подтверждает.

## Техническая база

Версионно-зависимый сценарий проверен 2026-08-20 на baseline из metadata. Основания: [FastAPI — Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/), [Starlette — Test Client](https://www.starlette.io/testclient/) и [RFC 9457 — Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html).
