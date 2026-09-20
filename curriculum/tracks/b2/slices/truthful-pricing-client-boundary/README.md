---
id: b2.index.truthful-pricing-client-boundary
kind: index
title: Правдивая граница клиента Pricing
owner_track: b2
module: b2.module.external-service-integration
coverage:
  - target: b2.capability.integrate-external-services
    role: reference
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

# Когда «предложений нет» должно быть правдой

Покупатель открывает карточку товара, Quote API обращается к Pricing и отвечает «предложений нет». Но Pricing вернул повреждённый JSON. Покупатель делает предметный вывод об ассортименте, хотя сервис лишь не смог понять технический ответ. Рабочая задача этого пакета — сохранить различие между отсутствием предложения и невозможностью узнать ответ.

Внешний сервис, от которого зависит Quote, называется **зависимостью (dependency)**. **Клиентский адаптер (client adapter)** переводит её HTTP-ответ в понятный вызывающему сервису результат. **Предметное отсутствие (business absence)** означает подтверждённый корректным ответом пустой список. **Сбой интеграции (integration failure)** означает, что данные не получены или не прошли договорённые проверки. Ни один сбой не доказывает отсутствие.

## Что вы будете делать

История ограничена одним read-only `GET /v1/offers?item_id=p-7` от Quote к Pricing. Успех — 200 JSON с совпадающим item_id и обязательным массивом offers. Явный пустой массив приводит к `200 outcome=no_offers`; невалидный ответ, 5xx и transport failure — к 502, timeout — к 504. Эти коды — договор лаборатории. Quote имеет один endpoint `GET /quotes?item_id=p-7`, а URL Pricing задаёт среда. Одна **попытка (attempt)** — один исходящий HTTP request; автоматических повторов нет.

Маршрут [модуля интеграции внешних сервисов](../../modules.md) развивает [одно инженерное действие](../../capabilities.md): использовать или самостоятельно определить клиентскую границу с явными исходами и ресурсным владельцем.

| Материал | Зачем открыть | Что предъявить после работы |
|---|---|---|
| [Разбор ответа](learn/response-to-domain-outcome.md) | Понять цепочку transport → HTTP → decoding → validation → domain | Объяснение, почему только проверенный пустой массив означает отсутствие |
| [Интервью](interview/pricing-client-decisions.md) | Проверить применение договора и самостоятельные решения | Рассуждение с контрпримером и способом проверки |
| [Kata](kata/stop-failure-to-empty-collapse.md) | Применить заданные исходы и исправить один failure→empty defect | Исходный и исправленный trace всех строк, attempts и cleanup |
| [Самостоятельный проект](project-spec/integrate-one-pricing-operation.md) | Выбрать внутренние типы и интегрировать одну dependency | Рабочий HTTP path, полная матрица, решение и измерения |

Learn объясняет [L1 и L2](../../level-outcomes.md), interview только исследует рассуждение. Kata даёт практику и оценку применения заданного client contract L1. Project требует автономного выбора внутреннего result/error model и интеграции L2. YAML пяти accepted-материалов содержит 9 relationships к capability и двум outcomes; они входят в accepted coverage каталога, но не подтверждают proficiency конкретного участника.

## Что нужно до начала

Нужно уметь читать HTTP status/headers/JSON, пользоваться Python exceptions и async context manager, различать строку и integer, создавать и закрывать общий HTTP client. Resource lifecycle — [hard prerequisite](../../prerequisites.md), а не новая тема для зачёта здесь. Сетевая конфигурация принадлежит среде; read-only смысл операции известен до решения о retry.

Для восстановления контекста полезны [ограниченная конкурентность](../runtime-concurrency-lifecycle/learn/bounded-concurrency-pool-saturation.md) и [устойчивый fan-out](../runtime-concurrency-lifecycle/project-spec/resilient-fanout-service.md). Там один запрос порождает четыре вызова; здесь намеренно только один. [Правдивая граница проверки](../risk-based-service-verification/learn/truthful-test-boundaries.md) объясняет, почему тест должен включать механизм отказа. Детали задания и критерии каждого шага приведены прямо в соответствующем файле.

## Общая лабораторная рамка

Python 3.14.0, FastAPI 0.137.1, Starlette 1.3.1, HTTPX 0.28.1, Pydantic 2.12.5. Quote вызывается через ASGI; Pricing отвечает по настоящему loopback HTTP. Ответы полностью читаются. HTTPX phase timeouts по 100 мс; наблюдаемый ответ Quote <500 мс на каждый запрос; drain и закрытие контролируемых ресурсов ≤1 с. Это учебные thresholds для малых тел и последовательных операций.

Контрольный healthy-профиль содержит 6 операций; дефектный и исправленный — по 33 (11 строк по 3); recovery — 6. Четыре negative checks доводят общее число входящих проверок до 82, outbound attempts — до 79. Отказы вводятся независимо: malformed JSON, media, schema, 503, timeout, socket close; дополнительно проверяются чужой item_id, null и coercion. После исправления все 27 failure operations должны остаться ошибками, а все valid-empty — отсутствием предложения. Детальная матрица и измерения есть в kata и project.

## Границы

Пакет использует Quote/Pricing контекст [S08](../../scenarios.md), но не закрывает канонический fan-out/slow-dependency сценарий целиком. S13 остаётся контекстом ограничения ресурсов. Здесь нет pool tuning, cancellation/disconnect exercise, service discovery, retries, circuit breaker, callback URL/SSRF, store или cross-team integration policy. Проверка реального HTTP decoding подтверждает integration action; она не заменяет отдельный курс проверки сервисов S10.

### Можно ли пройти только interview и считать L2 доказанным?

<details>
<summary>Ответ</summary>

Нет. Сильное объяснение выявляет понимание, но не показывает, что выбранный адаптер действительно получает HTTP bytes, сохраняет пустой успех, различает отказ и закрывает клиент. Для этого нужен результат самостоятельного проекта и его проверка.

</details>

## Короткий словарь

- **Decoding** — превращение полученных байтов JSON в значения языка; не проверка их предметного смысла.
- **Schema validation** — проверка обязательных полей, типов и ограничений после decoding.
- **Recovery** — здоровый ответ на том же клиенте после снятия отказа.
- **Cleanup** — завершение принадлежащей лаборатории работы и освобождение ресурсов.

## Источники и применимость

Проверено 2026-09-08 на Python 3.14.0, FastAPI 0.137.1, Starlette 1.3.1, HTTPX 0.28.1 и Pydantic 2.12.5; транзитивные httpcore 1.0.9 и AnyIO 4.11.0. Это исполненный baseline. Обнаруженные stable версии: [Python 3.14.7](https://www.python.org/downloads/), [FastAPI 0.141.1](https://pypi.org/project/fastapi/), [Starlette 1.6.0](https://pypi.org/project/starlette/), [Pydantic 2.13.5](https://pypi.org/project/pydantic/); [HTTPX 0.28.1](https://pypi.org/project/httpx/) остаётся stable, 1.0.dev6 — предварительная версия. Новые версии не исполнялись. Python baseline отстаёт на несколько patch releases; перед переносом повторите матрицу, strict validation и закрытие ресурсов. Эти pins не являются рекомендацией для production.

- [HTTPX transports](https://www.python-httpx.org/advanced/transports/) объясняет transport retries и границу request/response; ASGITransport не запускает lifespan автоматически.
- [HTTPX timeouts](https://www.python-httpx.org/advanced/timeouts/) различает connect/read/write/pool ожидания; одинаковые значения не составляют общий deadline.
- [HTTPX exceptions](https://www.python-httpx.org/exceptions/) задаёт классы транспортных отказов и timeout.
- [FastAPI lifespan](https://fastapi.tiangolo.com/advanced/events/) описывает создание общего ресурса до yield и закрытие после.
- [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/) объясняет ограничение автоматического приведения типов; фактическое отклонение строковой суммы проверяется отдельной строкой.
- [RFC 9110, safe methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.1) задаёт read-only смысл GET; реальная операция Pricing дополнительно обязана не создавать бизнес-запись.

Численные пороги относятся к конечному локальному опыту, а не к production SLO. TLS, proxy, DNS, SSRF, disconnect и насыщение пула этим опытом не доказываются.
