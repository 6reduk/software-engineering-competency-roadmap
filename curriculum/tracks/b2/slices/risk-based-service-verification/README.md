---
id: b2.index.risk-based-service-verification
kind: index
title: Проверка сервиса по рискам
owner_track: b2
module: b2.module.service-verification
coverage:
  - target: b2.capability.verify-service-behavior
    role: reference
  - target: b2.capability.verify-contract-compatibility
    role: reference
status: accepted
updated: 2026-08-20
language: ru
last_verified: 2026-08-20
versions:
  fastapi: 0.136.3
  starlette: 1.3.1
  pydantic: 2.13.4
---

# Проверка сервиса по рискам

В Orders service зелёные проверки бизнес-правил, входной Pydantic-модели и обработчика операции. Тем не менее новый клиент не может подсветить ошибку формы: собранное приложение возвращает стандартный ответ FastAPI вместо обещанного публичного формата. Зелёный набор подтверждал отдельные части системы, но ни одна проверка не запускала механизм, который сломан, — регистрацию обработчика исключения и формирование фактического HTTP-ответа.

Этот slice учит связывать риск с механизмом отказа и выбирать самую дешёвую границу проверки, на которой этот механизм действительно присутствует. Название «unit», «integration» или «end-to-end» само по себе такой связи не доказывает.

## Сквозная ситуация и ущерб для клиента

Новый клиент вызывает `POST /orders` с `Accept: application/problem+json`. Для доставки `mode="scheduled"` обязательны `window.start` и `window.end`. В следующем запросе отсутствует конец окна:

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

Публичный контракт требует HTTP `422`, `Content-Type: application/problem+json` и согласованное тело:

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

Клиент ветвится по HTTP-статусу и стабильному `type`, а `errors[].pointer` использует для подсветки поля. Он не разбирает текст `detail` и внутреннюю форму FastAPI/Pydantic.

В дефектной сборке обработчик `RequestValidationError`, переводящий внутреннюю ошибку в этот Problem Details, не зарегистрирован. Реальный запрос получает `422 application/json` с framework-specific полем `detail`. Клиент теряет машинно читаемый тип и указатель поля, хотя локальные проверки остаются зелёными.

## Маршрут

1. [Правдивые границы проверки](learn/truthful-test-boundaries.md) — разберите цепочку «риск → механизм → граница → сигнал → стоимость → остаточный риск» и четыре разные границы на одном запросе.
2. [Интервью: зелёные тесты, сломанный контракт](interview/green-tests-broken-contract.md) — проверьте способность выбирать следующую проверку и перестраивать набор проверок сервиса без догматичной пирамиды.
3. [Kata: обнаружить регрессию error contract](kata/detect-orders-error-contract-regression.md) — создайте минимальную систему, посейте один дефект сборки и добавьте проверки, которые его обнаруживают и локализуют.
4. [Проект: verification portfolio Orders service](project-spec/orders-verification-portfolio.md) — перестройте набор проверок одного сервиса по критическим путям и ожиданиям двух клиентов, измеримо убрав дублирование.

Engineering brief объясняет модель. Interview выявляет качество рассуждения, но не подтверждает навык исполнения. Kata даёт ограниченную практику на одном дефекте. Проект проверяет решение уровня одного сервиса и намеренно шире kata.

## Что желательно знать заранее

- базовые HTTP status/media type semantics;
- заданный Orders error contract из [S03](../evolvable-api-contracts/README.md);
- различие application/domain/adapters из [S06](../service-architecture-boundaries/learn/change-isolation-service-boundaries.md);
- идея risk-based проверки failure paths из [S08](../runtime-concurrency-lifecycle/project-spec/resilient-fanout-service.md).

Ссылки дают подробный контекст, но для начала достаточно рабочей истории и контракта выше.

## Ожидаемый результат

После маршрута инженер может:

- объяснить, почему зелёная проверка части системы не подтверждает внешнее поведение;
- связать конкретный пользовательский риск с механизмом отказа;
- выбрать самую дешёвую границу, где механизм не подменён;
- построить сигнал, который одновременно ловит регрессию и помогает локализовать её;
- отличить исполняемую проверку клиентского ожидания от снимка схемы;
- убрать медленное или хрупкое дублирование без потери подтверждения критических путей;
- назвать стоимость и остаточный риск выбранного набора.

Трассировка маршрута относится к проверке поведения сервиса (`b2.capability.verify-service-behavior`) и совместимости контракта (`b2.capability.verify-contract-compatibility`). Новое покрытие этого пакета — умение на L1 поддерживать заданную [проверку совместимости контракта](../../level-outcomes.md#b2capabilityverify-contract-compatibility); остальные результаты L1–L3 уже встречались в принятых slices и здесь получают собственный маршрут Service Verification.

## Актуальность технической базы

Поведение проверено по официальной документации и воспроизводимому baseline FastAPI 0.136.3, Starlette 1.3.1 и Pydantic 2.13.4 на 2026-08-20. На дату проверки опубликована FastAPI 0.141.1. Используемый механизм — `RequestValidationError`, default validation response и регистрация application-level exception handler — в проверенных официальных материалах не изменяет вывод slice. При обновлении закрепите версии и повторите wire-level checks: имя теста или зелёная схема не являются доказательством совместимости новой связки.

## Границы slice

Это не общий курс test design, не каталог фреймворков и не универсальная пирамида тестов. Здесь не проектируются заново Orders API, migration ошибок, service architecture, runtime cancellation, CI/CD и межкомандные quality gates. ASGI-проверка внутри процесса запускает собранное приложение, но не доказывает production network, proxy, deployment configuration и реальные клиентские версии.
