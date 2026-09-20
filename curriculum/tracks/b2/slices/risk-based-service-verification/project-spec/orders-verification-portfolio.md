---
id: b2.project-spec.orders-verification-portfolio
kind: project-spec
title: Проектная спецификация — verification portfolio Orders service
owner_track: b2
module: b2.module.service-verification
coverage:
  - target: b2.level-outcome.verify-service-behavior-l3-design-service-strategy
    role: integrate
  - target: b2.level-outcome.verify-service-behavior-l3-design-service-strategy
    role: assess
  - target: b2.level-outcome.verify-contract-compatibility-l3-build-consumer-evidence
    role: integrate
  - target: b2.level-outcome.verify-contract-compatibility-l3-build-consumer-evidence
    role: assess
status: accepted
updated: 2026-08-20
language: ru
last_verified: 2026-08-20
versions:
  fastapi: 0.136.3
  starlette: 1.3.1
  pydantic: 2.13.4
---

# Проектная спецификация: verification portfolio Orders service

Вы владеете одним небольшим Orders service. Его test suite вырос по мере изменений: одни и те же assertions повторяются в model, handler, HTTP и deployment-like checks; часть широких checks медленная или нестабильная, но никто не может объяснить, какой риск потеряется при удалении. Одновременно новая регрессия error mapping прошла сквозь зелёный набор.

Выполните в отдельном репозитории один service-level milestone: перестройте набор проверок по критическим путям и механизмам отказа, свяжите его с ожиданиями двух представительных клиентов и измеримо удалите хотя бы одну доказанно дублирующуюся медленную или хрупкую проверку без потери значимого подтверждения.

Это не расширенная версия kata. Kata обнаруживает и локализует один известный handler defect. Проект исследует portfolio всего одного сервиса, несколько механизмов и реальное решение об удалении дублирования.

## Канонический error contract

Новый клиент отправляет `POST /orders` с `Accept: application/problem+json`. Для `delivery.mode="scheduled"` отсутствует `window.end`:

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

Ответ обязан иметь HTTP `422`, `Content-Type: application/problem+json` и тело:

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

Не меняйте этот контракт. Историческую миграцию error formats из S03 повторно проводить не нужно.

## Два представительных клиента

Зафиксируйте inventory минимум следующих consumers и их версии/владельцев в пределах проекта:

1. **Регулярно обновляемый новый client.** Для invalid scheduled order использует HTTP status, стабильный `type` и `errors[].pointer`; `detail` показывает человеку, но не разбирает программно.
2. **Legacy operations script.** Для успешного `POST /orders` использует `201` и `order_id`; на invalid request прекращает автоматизацию по HTTP `422`, но не читает Problem Details extensions.

Проверяйте только реально используемые части. Не копируйте все assertions нового client в legacy check. Если в своей реализации вы добавляете другое подтверждённое ожидание, запишите источник и влияние на решение о release/migration.

## Единственный milestone

### Цель

Получить risk-based verification portfolio одного Orders service, который:

- покрывает существенные success/error paths на границах, где присутствуют их механизмы;
- различает local/application, adapter/component и assembled HTTP/contract evidence;
- обнаруживает несколько seeded failures и помогает локализовать механизм;
- связан с semantic expectations двух consumers;
- после измерения становится дешевле или стабильнее без потери critical-path evidence.

### Наблюдаемые deliverables

1. Небольшой работающий Orders service и воспроизводимые команды запуска.
2. Inventory критических paths и failure modes с обоснованием существенности.
3. Карта `risk → mechanism → truthful boundary → signal/localization → cost → residual risk` для каждого выбранного риска.
4. Consumer inventory с версиями/владельцами, используемыми частями контракта и semantic checks.
5. Исходный portfolio и результаты контрольного прогона.
6. Набор нескольких seeded failures из разных mechanisms и матрица обнаружения/локализации.
7. Заранее объявленный measurement envelope, результаты до/после и raw summary.
8. Удаление либо понижение scope минимум одной доказанно дублирующейся slow/flaky check.
9. Итоговый portfolio и подтверждение сохранённого critical-path evidence повторной fault injection.
10. Короткий decision record.

## Inventory рисков, а не типов тестов

Включите только реально существующие в реализации paths. Минимальный набор должен различать:

- успешное создание заказа;
- invalid scheduled window и публичный Problem Details;
- хотя бы одно business/application rejection, отличное от Pydantic input failure;
- mapping одного реального adapter, если сервис его содержит;
- application assembly/HTTP mapping.

Для каждого риска заполните таблицу до изменения suite:

| Риск и ущерб | Механизм | Самая дешёвая правдивая граница | Сигнал и локализация | Стоимость | Остаточный риск |
|---|---|---|---|---|---|
| Новый client не разбирает validation error | Request validation → handler registration → Problem mapping | Assembled ASGI + consumer semantic assertions | Component green / HTTP red указывает на assembly/mapping | Измерить | Proxy/deployment/client binary вне границы |

Первая строка задаёт обязательный пример, но не готовый portfolio. Остальные строки зависят от выбранной реализации. Названия `unit/integration/E2E` можно добавить как навигацию, но они не заменяют mechanism analysis.

## Границы, которые должны отвечать на разные вопросы

- **Local/application checks** подтверждают business rules и координацию без несущественного I/O.
- **Adapter/component checks** подтверждают validation, persistence/external mapping или serializer как отдельный механизм.
- **Assembled HTTP checks** проходят через production-like app factory, routing, exception handlers и response serialization.
- **Consumer contract checks** выражают реально используемые ожидания нового client и legacy script.

Один check может играть две роли, если это явно доказано. Например, assembled HTTP request может одновременно проверять handler registration и semantic expectation нового client. Не создавайте копию только ради отдельной строки таблицы.

## Seeded failures для проверки локализации

Используйте минимум три отказа из разных механизмов. Обязателен исходный S10 defect:

1. handler `RequestValidationError` отсутствует либо зарегистрирован для другого exception type;
2. validation rule или component mapping неверно обрабатывает отсутствие `window.end`;
3. публичный mapper меняет стабильный `type`, pointer или media type при сохранённом status;
4. опционально — реальный adapter искажает используемое business value;
5. опционально — application operation выбирает неверный business outcome.

Выберите 3–4 cards, сформулируйте ожидаемый signal pattern до внесения отказа и не храните fault как постоянную production branch. Проектная спецификация не задаёт код fault injection.

Сильная локализация — не мгновенное имя строки, а различающийся pattern. Например, validation component red + HTTP red указывает на правило/mapping раньше assembly; component green + HTTP red — на wiring/HTTP boundary.

## Measurement envelope

До измерения письменно выберите:

- точный набор checks и измеряемую популяцию прогонов;
- machine/runtime baseline и закреплённые версии;
- warm-up, число повторов или длительность наблюдения;
- выбранные seeded failures и одинаковый порядок до/после;
- точку измерения: wall-clock suite duration, отдельная check duration, повторяемость flaky failure, число дублирующих semantic assertions или время локализации;
- порог принятия и причину его выбора;
- способ убедиться, что critical-path evidence не потеряно.

Используйте минимум одну метрику стоимости и одну метрику качества evidence. Например: длительность выбранного набора плюс число правильно обнаруженных и локализованных карточек отказов (`fault cards`); либо частота нестабильных падений на фиксированном числе прогонов плюс время локализации. Значения и threshold выбирает участник до прогона. Они относятся только к этому сервису и этому envelope, а не являются production SLO или универсальным процентом test types.

После удаления/понижения scope повторите тот же workload и fault cards. Простое уменьшение числа тестов не считается улучшением.

## Требование к удалению дублирования

Выберите хотя бы одну slow/flaky check и ответьте:

1. Какой риск и механизм она единственная якобы подтверждает?
2. Какие assertions механически повторяются на более дешёвых границах?
3. Какой более широкий механизм реально добавляется?
4. Можно ли сохранить этот механизм одним представителем, а combinations перенести ниже?
5. Какие fault cards ловятся до и после?

Допустимы удаление, сокращение данных/вариантов или перевод в реже запускаемый профиль. Недопустимо объявлять проверку дублирующейся только по похожему имени или одинаковому happy path.

## Decision record

Зафиксируйте:

- критические риски и consumer expectations;
- минимум две альтернативы portfolio;
- выбранные boundaries и уникальный механизм каждой;
- исходную и итоговую стоимость в объявленном envelope;
- удалённую/пониженную check и доказательство отсутствия потери evidence;
- false positives, false confidence и диагностичность;
- остаточные риски, включая production network/deployment и неизвестных consumers;
- trigger пересмотра: новый critical path, escaped defect, изменение client expectation или рост стоимости/flakiness;
- release/migration decision для текущей версии Orders service на основании двух consumer checks.

## Review criteria

- [ ] Scope ограничен одним Orders service.
- [ ] Endpoint, invalid request и Problem Details совпадают с каноническим контрактом.
- [ ] Inventory содержит критические paths/failure modes, а не только список tests.
- [ ] Каждый существенный риск связан с mechanism, boundary, signal, cost и residual risk.
- [ ] Новый client и legacy operations script имеют разные, реально используемые semantic expectations.
- [ ] Consumer inventory/versions и checks связаны с release/migration decision.
- [ ] Local/application, adapter/component и HTTP/contract evidence не подменяют друг друга.
- [ ] Минимум три seeded failures разных mechanisms воспроизводимы и локализуются pattern-ом signals.
- [ ] Envelope, thresholds и порядок измерения объявлены до результатов.
- [ ] Есть сравнимые до/после показатели стоимости и качества evidence.
- [ ] Минимум одна slow/flaky check удалена или сужена после доказательства дублирования.
- [ ] Повторная fault injection подтверждает сохранение critical-path evidence.
- [ ] Нет универсальных процентов test pyramid, CI platform optimization и cross-team governance.
- [ ] Decision record содержит alternatives, costs, residual risks и trigger пересмотра.
- [ ] ImplementationReference не зарегистрирована до самостоятельной реализации и review.

Эти критерии подтверждают service-wide Verification L3. Compatibility L3 заявляется потому, что milestone связывает inventory и semantic expectations минимум двух consumers с checks и release/migration decision, а не потому, что существует один HTTP example.

## Вопросы защиты

### Чем проект отличается от kata?

<details>
<summary>Ориентиры ответа</summary>

Kata работает с одним заранее известным handler defect и минимальной парой checks. Проект строит portfolio всего одного сервиса, моделирует несколько failure mechanisms, связывает два consumer expectations с решением и измеримо удаляет дублирование. Исправить только S10 regression недостаточно.

</details>

### Как доказано, что удалённая check была дублирующейся?

<details>
<summary>Ориентиры ответа</summary>

Нужно показать механизм и assertions до удаления, затем одинаковые fault cards и critical paths до/после. Оставшийся набор должен обнаружить существенные faults и сохранить приемлемую локализацию, а выбранная метрика стоимости — улучшиться в заранее объявленном envelope.

</details>

### Почему consumer checks различаются?

<details>
<summary>Ориентиры ответа</summary>

Новый client использует `type` и pointer; legacy script — `201/order_id` и status `422`. Копирование полного Problem Details assertion в legacy test не добавило бы evidence. Совместимость всегда относится к конкретному ожиданию и версии consumer.

</details>

### Какие риски portfolio намеренно не закрывает?

<details>
<summary>Ориентиры ответа</summary>

In-process ASGI не доказывает proxy/network/deployment; представители не доказывают ожидания неизвестных consumers; fault cards не исчерпывают production failures. Сильный ответ связывает существенный остаточный риск с будущей проверкой или явным решением, а не обещает полную уверенность.

</details>

## Non-goals

- общий benchmark testing frameworks;
- оптимизация CI platform или test infrastructure нескольких сервисов;
- performance engineering Orders service;
- production rollout и organization-wide quality gates;
- L4 cross-team adoption/process;
- готовая архитектура, эталонный portfolio или solution code.

## ImplementationReference

Отсутствует до самостоятельного выполнения проекта и независимого review. Спецификация задаёт наблюдаемый milestone, но не является готовой реализацией.

## Короткий словарь

- **Verification portfolio** — набор проверок одного сервиса, связанный с рисками, механизмами, стоимостью и остаточными рисками.
- **Semantic check** — проверка используемого клиентом смысла, а не полного снимка схемы или ответа.
- **Measurement envelope** — заранее заданные популяция прогонов, версии, длительность/повторы, fault cards, точка измерения и threshold.
- **Карточка отказа (`fault card`)** — заранее описанный способ нарушить конкретный механизм и ожидаемый сигнал, по которому проверяют обнаружение и локализацию сбоя.
- **Critical-path evidence** — результаты, подтверждающие существенный путь и способ его нарушения в пределах названной границы.
- **ImplementationReference** — ссылка на самостоятельно выполненный и проверенный проект, а не эталонное решение.

## Связанный контекст

- [Совместимость и consumer expectations S03](../../evolvable-api-contracts/learn/compatible-api-change.md)
- [Business/application/adapter evidence S06](../../service-architecture-boundaries/learn/change-isolation-service-boundaries.md)
- [Risk-based failure-path verification S08](../../runtime-concurrency-lifecycle/project-spec/resilient-fanout-service.md)

Версионно-зависимый S10 mechanism проверен 2026-08-20 по [FastAPI — Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/), [Starlette — Test Client](https://www.starlette.io/testclient/) и [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html).
