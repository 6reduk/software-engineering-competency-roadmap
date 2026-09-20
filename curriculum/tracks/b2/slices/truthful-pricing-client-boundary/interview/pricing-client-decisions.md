---
id: b2.interview.pricing-client-decisions
kind: interview
title: Интервью — решения на границе Pricing
owner_track: b2
module: b2.module.external-service-integration
coverage:
  - target: b2.level-outcome.integrate-external-services-l1-use-defined-client
    role: probe
  - target: b2.level-outcome.integrate-external-services-l2-design-typical-client-boundary
    role: probe
status: accepted
updated: 2026-09-08
language: ru
last_verified: 2026-09-08
versions:
  python: 3.14.0
  fastapi: 0.137.1
  starlette: 1.3.1
  httpx: 0.28.1
  pydantic: 2.12.5
---

# Почему покупатель видит «предложений нет»

Команда Quote API получает жалобу: покупатель не видит предложений, хотя Pricing лишь временно отвечает повреждёнными данными. Клиентский адаптер — переводчик внешнего HTTP-ответа во внутренний результат сервиса — при любой неудаче возвращает []. Интервью исследует, как инженер применяет заданный договор, а затем самостоятельно проектирует такой перевод.

Pricing — внешняя зависимость (dependency). Подтверждённый пустой ответ означает предметное отсутствие (business absence). Невозможность получить или разобрать ответ — сбой интеграции (integration failure). Успешный разговор ещё не доказывает практическое освоение: здесь только probes [External L1/L2](../../../level-outcomes.md). Для исполнения нужны [kata](../kata/stop-failure-to-empty-collapse.md) и [проект](../project-spec/integrate-one-pricing-operation.md).

## Данные для разговора

Quote получает `GET /quotes?item_id=p-7` и делает одно read-only чтение `GET /v1/offers?item_id=p-7`. Адрес Pricing задаёт среда, пользователь передаёт только item_id по правилу `p-[0-9]{1,6}`. Success contract: 200 application/json, обязательные item_id и offers; identity должна совпасть. Полный объект:

```json
{"item_id":"p-7","offers":[{"offer_id":"o-1","amount_minor":12500,"currency":"RUB"}]}
```

offer_id — непустая строка, amount_minor — integer ≥0 без coercion, currency — RUB; дополнительные поля запрещены локально. Явное offers=[] при item_id=p-7 допустимо; null, отсутствие поля, другой item_id и строковая сумма недопустимы.

Quote возвращает 200 с item_id, outcome=offers или no_offers и массивом offers. Для технических отказов тело application/json `{"error":"pricing_unavailable","reason":"<category>"}`, без offers: 502 для http/media/decoding/schema/transport, 504 для timeout. Любой status Pricing кроме 200 вне success contract. В частности, 503 с телом offers=[] остаётся http failure. Media type проверяется без параметра charset; JSON под text/html — media failure. Повреждённые bytes `{"offers":` — decoding failure.

Baseline: Python 3.14.0, FastAPI 0.137.1, Starlette 1.3.1, HTTPX 0.28.1, Pydantic 2.12.5. Pricing — реальный loopback HTTP; Quote вызывается через ASGI с явно запущенным lifespan. HTTPX phase timeouts по 100 мс, наблюдаемый Quote response <500 мс на каждую операцию; drain и cleanup ≤1 с. Это ограниченный учебный опыт. В timeout mode Pricing молчит 350 мс до headers; в transport mode закрывает socket до ответа.

## 1. Применение договора L1: три пустоты

В трёх ответах Pricing: A — 200 JSON с item_id=p-7 и offers=[]; B — 200 JSON без offers; C — 503 JSON с offers=[]. Как должен ответить Quote? Follow-up: почему один `.get("offers", [])` не подходит всем трём?

<details>
<summary>Ответ и ориентир интервьюера</summary>

A даёт 200 outcome=no_offers: это подтверждённое отсутствие. B — 502 reason=schema: обязательный факт отсутствует. C — 502 reason=http: status уже исключил success path. Default-empty уничтожает оба различия. Сильный L1 применяет конкретные строки и порядок проверок; слабый ответ «любая ошибка — 500» тоже не выполняет заданный договор.

</details>

## 2. Применение договора L1: где остановился ответ

Pricing вернул 200 text/html с синтаксически правильным JSON. В другом запросе headers не пришли до ReadTimeout. Как различить причины? Follow-up: будет ли корректный Python dict доказательством проверки этих двух ситуаций?

<details>
<summary>Ответ и ориентир интервьюера</summary>

Первый случай нарушает договор media type, второй не дал полного HTTP response вовремя. Quote отвечает соответственно 502/media и 504/timeout. Нельзя рисовать status 200 в timeout trace, если его не получали. Готовый dict начинается после HTTP и decoding, поэтому не подтверждает ни media validation, ни реальный timeout. Нужен response/failure на границе HTTP-клиента.

</details>

## 3. Применение договора L1: успех после отказа

После timeout тест получил ожидаемый 504 и завершился. Pricing ещё выполняет 350-мс обработчик. Достаточен ли зелёный assertion? Follow-up: какие наблюдения нужны до следующего режима?

<details>
<summary>Ответ и ориентир интервьюера</summary>

Нет. Нужно дождаться active Pricing handlers=0 ≤1 с и отсутствия незавершённой client work. На том же клиенте после снятия отказа проверить full/empty, затем закрытие lifespan/client, server thread и порта. Timeout завершает локальное ожидание, не доказывает остановку удалённой работы. Слабый ответ смотрит только status либо создаёт новый клиент и теряет проверку восстановления прежнего.

</details>

## 4. Переход к L2: внутренние результаты

Два инженера предлагают: «все ошибки через exceptions» и «все результаты через tagged union». Как выбрать для небольшого Quote? Follow-up: где должны остаться HTTPX exception types?

<details>
<summary>Признаки сильного рассуждения</summary>

Оба подхода допустимы. Нужно проследить места вызова, показать отдельные варианты offers/no_offers/failure и невозможность молчаливого провала в []. В варианте с исключениями ожидаемые integration failures ограничены собственными типами; broad catch не должен поглотить их. В union вызывающий код должен рассматривать failure ветвь, а не считать её пустым успехом. HTTPX types переводятся на клиентской границе; публичный Quote contract не зависит от их текста. Сильное L2-решение обосновано небольшим реальным путем вызова и изменением, которое оно локализует, а не названием паттерна.

</details>

## 5. L2: read-only не означает «повторять всегда»

Pricing только читает. Коллега добавляет retries=3 ради доступности. Приемлемо ли это здесь? Follow-up: что могло бы обосновать пересмотр?

<details>
<summary>Признаки сильного рассуждения</summary>

Это нарушает заданную one-attempt модель. Read-only уменьшает риск повторного бизнес-эффекта, но не отменяет время, нагрузку и возможность другого результата чтения. Здесь retries=0, нет loop, redirects и auth resend. Пересмотр требует нового требования доступности, классификации временных отказов, выделенного budget и согласования scope; malformed/schema failure сам по себе повтором не исправляется. L2 доказывает решение счётчиками attempts и server receipts на каждый request ID, а не только записью конфигурации.

</details>

## 6. L2: чему именно доверяем

Base URL берётся из окружения; пользователь предлагает передать `http://evil.test:9999/x` как item_id либо query base_url. Какую проверку проведёте? Follow-up: можно ли написать в отчёте «SSRF закрыт»?

<details>
<summary>Признаки сильного рассуждения</summary>

URL-подобный item_id отклоняется до HTTPX; дополнительный base_url не выбирает authority. Нужны отрицательные примеры, 422 и нулевые попытки для неверного item_id, а для допустимого ID с base_url — одна попытка в конфигурационный адрес. SSRF не доказан: DNS rebinding, redirect/egress policies и arbitrary callbacks здесь не исследуются. Сильный ответ удерживает границу проверки и не строит security platform ради одной операции.

</details>

## 7. L2: честность измерений

HTTPX настроен на timeout=100 мс. Автор отчёта называет это end-to-end deadline 100 мс. Как проверить утверждение? Follow-up: почему наш порог Quote <500 мс не делает его верным?

<details>
<summary>Признаки сильного рассуждения</summary>

HTTPX различает ожидания connect/read/write/pool; read timeout относится к ожиданию очередных данных. Эти интервалы не являются общей длительностью операции. Здесь measured Quote latency — время от отправки ASGI-запроса до полного ответа в малом конечном профиле; <500 мс — экспериментальный acceptance threshold. Он ничего не доказывает для trickle streaming или очереди. Сильный ответ отделяет конфигурацию, фактическое измерение и предел вывода, не добавляя новый deadline propagation курс.

</details>

## 8. L2: различающее evidence

Известны control 6, defect 33, fixed 33, recovery 6 операций. Каждый широкий профиль имеет 11 строк по 3. Девять строк — failures. Какие счётчики помогут принять исправление? Follow-up: что не так с одной суммарной долей success?

<details>
<summary>Признаки сильного рассуждения</summary>

На defect ожидаются 27 ложных no_offers среди 27 failure operations; fixed обязан дать 0/27. Full и empty оцениваются отдельно: исправление «всегда ошибка» не проходит. На каждый допустимый request ID — одна outbound attempt и один receipt Pricing, плюс входной response/failure, решение адаптера и Quote result. Три отклонённых URL-like IDs и одна проверка игнорируемого base_url дают 82 входящих/79 исходящих за полный опыт. Общий success rate смешивает корректные пустые ответы с ложными и не показывает механизм.

</details>

## Как оценивать разговор

| Наблюдение | Вывод |
|---|---|
| Применяет заданные строки, различает malformed/media/schema и показывает cleanup | Сильное reasoning L1 |
| Сам выбирает внутреннее представление, владельца клиента и место mapping; обосновывает one-attempt и границу опыта | Сильное reasoning L2 |
| Называет retry/circuit breaker, но не объясняет ошибочное no_offers | Тема подменена механизмами устойчивости |
| Уверенно рассказывает, но не имеет выполненного проекта | Proficiency не подтверждено |

Не считайте термины и не выводите L3/L4 из длины ответа. Здесь не исследуются degraded-dependency ownership, cross-team policy, fan-out и saturation. Интервьюер может попросить участника указать конкретную запись его опыта, но готовый ответ из details не заменяет её.

## Локальный словарь

- **Decoding** — разбор полученных JSON bytes.
- **Schema validation** — проверка формы, типов и ограничений результата.
- **Tagged union** — несколько вариантов результата с явным признаком варианта.
- **Attempt** — один исходящий HTTP request.
- **Authority** — host и port в URL назначения; scheme также задаёт конфигурация.
- **Drain** — ожидание завершения уже начатой контролируемой работы.
- **Evidence** — наблюдения конкретного исполнения, на которых основан вывод.
- **Coercion** — автоматическое приведение, например string к integer.

## Источники и применимость

Проверено 2026-09-08 на Python 3.14.0, FastAPI 0.137.1, Starlette 1.3.1, HTTPX 0.28.1 и Pydantic 2.12.5; транзитивные httpcore 1.0.9 и AnyIO 4.11.0. Это исполненный baseline. Обнаруженные stable версии: [Python 3.14.7](https://www.python.org/downloads/), [FastAPI 0.141.1](https://pypi.org/project/fastapi/), [Starlette 1.6.0](https://pypi.org/project/starlette/), [Pydantic 2.13.5](https://pypi.org/project/pydantic/); [HTTPX 0.28.1](https://pypi.org/project/httpx/) остаётся stable, 1.0.dev6 — предварительная версия. Новые версии не исполнялись. Python baseline отстаёт на несколько patch releases; перед переносом повторите матрицу, strict validation и закрытие ресурсов. Эти pins не являются рекомендацией для production.

- [HTTPX transports](https://www.python-httpx.org/advanced/transports/) объясняет transport retries и границу request/response; ASGITransport не запускает lifespan автоматически.
- [HTTPX timeouts](https://www.python-httpx.org/advanced/timeouts/) различает connect/read/write/pool ожидания; одинаковые значения не составляют общий deadline.
- [HTTPX exceptions](https://www.python-httpx.org/exceptions/) задаёт классы транспортных отказов и timeout.
- [FastAPI lifespan](https://fastapi.tiangolo.com/advanced/events/) описывает создание общего ресурса до yield и закрытие после.
- [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/) объясняет ограничение автоматического приведения типов; фактическое отклонение строковой суммы проверяется отдельной строкой.
- [RFC 9110, safe methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.1) задаёт read-only смысл GET; реальная операция Pricing дополнительно обязана не создавать бизнес-запись.

Численные пороги относятся к конечному локальному опыту, а не к production SLO. TLS, proxy, DNS, SSRF, disconnect и насыщение пула этим опытом не доказываются.
