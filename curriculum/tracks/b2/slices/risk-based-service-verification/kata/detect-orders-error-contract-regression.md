---
id: b2.kata.detect-orders-error-contract-regression
kind: kata
title: Kata — обнаружить регрессию error contract Orders API
owner_track: b2
module: b2.module.service-verification
coverage:
  - target: b2.level-outcome.verify-service-behavior-l1-test-local-behavior
    role: practice
  - target: b2.level-outcome.verify-service-behavior-l1-test-local-behavior
    role: assess
  - target: b2.level-outcome.verify-service-behavior-l2-select-test-boundaries
    role: practice
  - target: b2.level-outcome.verify-service-behavior-l2-select-test-boundaries
    role: assess
  - target: b2.level-outcome.verify-contract-compatibility-l1-maintain-contract-check
    role: practice
  - target: b2.level-outcome.verify-contract-compatibility-l1-maintain-contract-check
    role: assess
  - target: b2.level-outcome.verify-contract-compatibility-l2-detect-breaking-change
    role: practice
  - target: b2.level-outcome.verify-contract-compatibility-l2-detect-breaking-change
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

# Kata: обнаружить регрессию error contract Orders API

Вы создаёте маленький Orders service и намеренно оставляете в нём один дефект сборки. Цель — не написать много тестов и не исправить бизнес-контракт, а показать, почему исходные зелёные проверки давали ложную уверенность, затем выбрать минимальные checks, которые воспроизводимо ловят и локализуют дефект.

Готового репозитория, scaffold и эталонной реализации нет. Минимальную систему создаёт участник. Спецификация фиксирует наблюдаемое поведение и способ посеять отказ, но не структуру файлов и не код решения.

## История и контракт клиента

Новый клиент вызывает `POST /orders` с `Accept: application/problem+json`. Для `delivery.mode="scheduled"` обязательны `window.start` и `window.end`. Используйте точный invalid request:

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

Ожидаемый ответ:

```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json
```

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

Клиент использует status и `type` для выбора реакции, pointer — для подсветки поля. Он не анализирует текст `detail` или внутренний Pydantic payload.

## Минимальная исходная система

Создайте:

- FastAPI application factory или эквивалентную точку сборки;
- `POST /orders` с минимальными входными моделями для приведённого body;
- правило, отклоняющее `scheduled` без `window.end`;
- преобразование validation error в указанный Problem Details;
- минимальный success path без БД, auth и внешних сервисов.

До seeded defect добейтесь, чтобы один реальный HTTP request подтверждал обещанный контракт. Это контрольный прогон: иначе нельзя отличить специально посеянную регрессию от незаконченного scaffold.

## Исходные зелёные, но недостаточные проверки

Оставьте зелёными три класса проверок:

1. domain/application test для известного правила заказа;
2. прямой Pydantic model/component test, который отклоняет invalid request;
3. router/handler unit test с mock/fake, вызывающий mapping слишком близко и не проходящий через фактическую таблицу exception handlers, сериализацию и HTTP response.

Названия и внутреннюю организацию выберите сами. В отчёте укажите, какое узкое утверждение доказывает каждая проверка.

## Посейте ровно один дефект

В composition root собранного приложения не зарегистрируйте handler для `RequestValidationError` либо зарегистрируйте mapping для другого exception type. Не меняйте validation rule, публичный контракт и client expectation.

Ожидаемое дефектное поведение: собранное приложение использует default FastAPI error path и возвращает `422 application/json` с framework-specific `detail`. Три исходные проверки остаются зелёными.

Если выбранный вариант не даёт именно этот разрыв на закреплённых версиях, не подменяйте контракт другим дефектом. Сначала проверьте тип фактического exception и способ сборки приложения.

## Задача

1. До добавления новых tests объясните ложную уверенность через цепочку: риск → mechanism → отсутствующая boundary → неверно расширенный зелёный сигнал.
2. Добавьте минимальные checks, падающие при seeded defect и проходящие после восстановления обещанного поведения.
3. Сохраните полезные быстрые tests; не заменяйте весь набор одним большим E2E.
4. Обеспечьте локализацию: результат должен отличать validation-rule failure от application assembly/HTTP mapping failure.
5. Поддержите заданную client contract check вместе с исправлением.
6. Напишите короткую decision note: риск, механизм, выбранные boundaries, сигналы, стоимость и остаточный риск.

## Наблюдаемые результаты

- команда запуска всех checks;
- контрольный, дефектный и исправленный прогоны;
- точный invalid request в тестовых данных;
- component check validation rule;
- assembled ASGI/HTTP check status, media type и semantic body;
- consumer-facing assertions только на реально используемые status/`type`/pointer;
- таблица результатов, позволяющая локализовать причину;
- decision note без готового production recipe.

Рекомендуемая диагностическая матрица должна получиться из фактов, а не быть заранее подогнана:

| Состояние | Validation component | Assembled HTTP | Вывод |
|---|---|---|---|
| Контрольное | green | green | Контракт воспроизводим |
| Seeded handler defect | green | red | Правило живо; исследовать assembly/mapping |
| Исправленное | green | green | Целевая регрессия обнаруживается до исправления |

## Acceptance criteria

- [ ] Исходная рабочая история и client damage описаны до списка tests.
- [ ] Endpoint, invalid body и полный Problem Details совпадают со спецификацией выше.
- [ ] До fault injection существует зелёный контрольный HTTP-прогон.
- [ ] Посеян ровно один defect регистрации/type matching exception handler.
- [ ] Исходные application/model/handler tests остаются зелёными на дефекте.
- [ ] Новая проверка проходит через production-like application assembly, а не отдельное test app с вручную подключённым handler.
- [ ] На дефекте падают status/media type/body assertions фактического ответа.
- [ ] Проверяется наличие `errors` с `#/delivery/window/end` и `required`, а не полный byte snapshot.
- [ ] Комбинация signals отличает validation failure от assembly/mapping failure.
- [ ] Полезные быстрые tests сохранены; один E2E не заменяет весь набор.
- [ ] Decision note называет стоимость и предел in-process ASGI evidence.

Acceptance criteria наблюдают действия Verification L1/L2 и Compatibility L1/L2: участник добавляет точную regression/contract check, сам выбирает границы, обнаруживает несовместимый response и объясняет ограничение evidence.

## Non-goals

- готовый код handler, test или application factory;
- база данных, очереди, auth, Docker, Kubernetes и production deployment;
- изменение Orders API или миграция старого error format;
- полный E2E через proxy/network;
- snapshot всего OpenAPI/response;
- portfolio всего сервиса — это отдельный проект.

## Подсказки

<details>
<summary>Подсказка 1 — найдите отсутствующий механизм</summary>

Нарисуйте путь `request → validation exception → handler lookup → mapping → response`. Отметьте, до какого узла доходит каждая зелёная проверка. Следующая boundary должна включить первый непроверенный узел.

</details>

<details>
<summary>Подсказка 2 — не расширяйте scope без причины</summary>

Для handler registration достаточно ASGI-вызова собранного application внутри процесса. Реальную БД и network deployment можно исключить: они не порождают seeded defect. Важно не собрать специальное test app иначе, чем рабочее.

</details>

<details>
<summary>Подсказка 3 — сделайте падение семантическим</summary>

Сравнивайте status, media type и используемые клиентом поля. Нормализуйте media type; не закрепляйте порядок JSON keys и весь framework error payload.

</details>

<details>
<summary>Подсказка 4 — локализация требует разных вопросов</summary>

Одна проверка должна отвечать «правило отклоняет input?», другая — «собранное приложение превращает отказ в обещанный response?». Если обе повторяют один и тот же mapper call, они не разделяют причины.

</details>

## Вопросы после выполнения

### Почему новая HTTP check ловит defect, а handler unit test — нет?

<details>
<summary>Ориентир ответа</summary>

Она запускает composition root и реальный handler lookup для `RequestValidationError`. Unit test начинает выполнение после дефектной точки либо подставляет правильный handler напрямую, поэтому seeded defect внутри него невозможен.

</details>

### Какой остаточный риск остаётся?

<details>
<summary>Ориентир ответа</summary>

ASGI in-process check не включает proxy, TLS, сеть, deployment configuration и настоящий binary/client runtime. Кроме того, одна негативная contract check не доказывает все Orders paths. Нужно назвать, какие из этих рисков существенны здесь, а какие сознательно оставлены проекту или production verification.

</details>

### Почему не стоит удалить model/component check?

<details>
<summary>Ориентир ответа</summary>

Она быстрее проверяет combinatorial validation и разделяет причины. При будущем сбое матрица component/HTTP сразу укажет, сломано правило или wiring. Дублирование отсутствует, если checks отвечают на разные вопросы.

</details>

## Короткий словарь

- **Seeded defect** — намеренно внесённый известный дефект для проверки обнаружения и локализации.
- **Собранное приложение (`assembled application`)** — application, полученное через рабочую точку сборки с реальными routes и exception handlers.
- **Проверка контракта (`contract check`)** — исполняемая проверка status, media type и полей, которые использует конкретный клиент.
- **Остаточный риск (`residual risk`)** — существенный механизм вне выбранной границы, например production proxy/deployment.

## Техническая база

Закреплённые версии и default/custom exception-handler paths проверены 2026-08-20. Для сверки используйте [FastAPI — Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/), [FastAPI — Testing](https://fastapi.tiangolo.com/tutorial/testing/), [Pydantic — Validators](https://docs.pydantic.dev/latest/concepts/validators/) и [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html).
