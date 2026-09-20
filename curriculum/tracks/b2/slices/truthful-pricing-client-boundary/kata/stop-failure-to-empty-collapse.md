---
id: b2.kata.stop-failure-to-empty-collapse
kind: kata
title: Kata — прекратить подмену сбоя пустым результатом
owner_track: b2
module: b2.module.external-service-integration
coverage:
  - target: b2.level-outcome.integrate-external-services-l1-use-defined-client
    role: practice
  - target: b2.level-outcome.integrate-external-services-l1-use-defined-client
    role: assess
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

# Восстановить правдивое «предложений нет»

Покупатель запросил цену p-7. Pricing вернул повреждённый JSON, а Quote API ответил 200 и пустым списком. Сервис продолжает работать, но сообщает неверный факт о предложении. Требование команды: сохранить корректные пустые ответы и перестать маскировать технические отказы.

Вы применяете **заданный client contract** и исправляете один дефект. Клиентский адаптер (client adapter) — переводчик HTTP Pricing во внутренний результат Quote. Предметное отсутствие (business absence) подтверждается валидными данными; сбой интеграции (integration failure) означает невозможность получить или понять ответ. Pricing — зависимость (dependency), а не источник гарантированно правильных Python-объектов.

Готового scaffold, репозитория или реализации адаптера нет. Участник сам создаёт минимальный стенд в своём отдельном репозитории либо использует свою реализацию, уже соответствующую заданному договору. Создание стенда — подготовка, не оценка самостоятельного архитектурного выбора L2. В этой kata оценивается применение известных исходов [External L1](../../../level-outcomes.md). Структуру модулей и библиотечный boilerplate оценка не предписывает.

## Один договор Quote/Pricing

Quote API обслуживает `GET /quotes?item_id=p-7` и делает ровно один `GET /v1/offers?item_id=p-7` к Pricing. Это чтение предложения без резервирования, списания и другой бизнес-записи. Адрес Pricing задаёт конфигурация среды: `http://127.0.0.1:<выделенный ОС порт>`. Путь постоянный; допустимый item_id соответствует `p-[0-9]{1,6}` и передаётся как query parameter. Внешний input не задаёт scheme/host/port. Correlation ID связывает записи Quote и заголовок Pricing `X-Request-ID`, но не является ключом идемпотентности. Режим отказа выбирает лаборатория вне caller input.

Успех Pricing — только status 200 и media type `application/json`; параметры вроде `charset=utf-8` не меняют этот тип. Полное предложение выглядит так:

```json
{"item_id":"p-7","offers":[{"offer_id":"o-1","amount_minor":12500,"currency":"RUB"}]}
```

Это цена 12500 в минимальных денежных единицах, не floating-point сумма. Весь объект и каждое предложение имеют обязательные поля; дополнительные поля запрещены этим локальным договором. offer_id — непустая строка, amount_minor — integer ≥0 без преобразования из string/bool, currency — RUB. item_id должен совпадать с запросом. Пустой успех — ровно тот же предметный ответ с явным `offers: []`; отсутствие поля и null не означают отсутствие предложения.

Quote возвращает `200 application/json` и `{"item_id":"p-7","outcome":"offers","offers":[...]}` для полного результата; многоточие здесь обозначает **единственное предложение из примера**, а не сокращённую схему. Для пустого результата полный ответ — `{"item_id":"p-7","outcome":"no_offers","offers":[]}`. Для отказа тело `{"error":"pricing_unavailable","reason":"<category>"}`, без поля offers. Category и HTTP status заданы матрицей; это локальный договор, не новая универсальная error taxonomy.

| Строка | Вход клиента Pricing | Значение после адаптера | Внешний Quote result |
|---|---|---|---|
| full | 200 JSON, полное предложение выше | Предложения получены | 200, outcome=offers |
| empty | 200 JSON, `{"item_id":"p-7","offers":[]}` | Предложений нет | 200, outcome=no_offers |
| malformed | 200 JSON, bytes `{"offers":` | Ошибка декодирования | 502, reason=decoding |
| media | 200 text/html, полный JSON из примера | Нарушен media type | 502, reason=media |
| schema | 200 JSON, `{"item_id":"p-7"}` | Нарушена схема | 502, reason=schema |
| server | 503 JSON, `{"offers":[]}` | HTTP failure | 502, reason=http |
| timeout | Сон Pricing 350 мс до headers; HTTPX ReadTimeout | Ответ не получен вовремя | 504, reason=timeout |
| transport | Закрытие socket до ответа; HTTPX RemoteProtocolError | Не получен полный HTTP response | 502, reason=transport |
| identity | 200 JSON, `{"item_id":"p-8","offers":[]}` | Ответ не относится к товару | 502, reason=schema |
| null | 200 JSON, `{"item_id":"p-7","offers":null}` | Нарушена схема | 502, reason=schema |
| coercion | 200 JSON, полный пример с amount_minor="12500" | Строка вместо integer | 502, reason=schema |

Все JSON-строки таблицы используют `application/json; charset=utf-8`, кроме явно указанного text/html. Проверка status предшествует разбору данных: 503 не становится успехом из-за похожего тела. Любой status кроме 200 вне success contract; например, 204 и 404 здесь относятся к http failure, пока иной договор явно не согласован.


## Один дефект, который надо обнаружить

Сначала подтвердите control full/empty на корректном пути. Затем внесите **одну** мутацию: в общей ветви известных integration failures верните результат no_offers с пустым массивом. Не меняйте Pricing, схему, timeout, адрес, one-attempt настройки или внешние ожидания. Это моделирует распространённый collapse failure→empty без необходимости портить девять независимых обработчиков.

Дефект обязан воспроизводиться и для malformed JSON: 200 JSON с bytes `{"offers":` приводит к 200 no_offers Quote. Этот результат — ошибочный, даже если проверка воспроизведения ожидает его и поэтому сама зелёная. Целевые assertions по контракту должны на дефекте падать. Исходный и исправленный профили используют одинаковые данные и expectations.

Вам задан внутренний договор применения: успешный список передаётся как offers/no_offers; известный failure сохраняет одну из категорий http/media/decoding/schema/timeout/transport. Исправьте только место, где failure превращается в пустой результат, и корректно обработайте известные варианты в вызывающем коде. Не проектируйте общую retry/resilience architecture. Неожиданные программные исключения также нельзя выдавать за отсутствие.

## Контур опыта и доказательства

Используйте FastAPI Quote, общий HTTPX AsyncClient в lifespan и локальный HTTP Pricing; ASGITransport допустим на входе Quote, но lifespan запускается явно. Исходящий HTTP transport настоящий. Закреплены `AsyncHTTPTransport(retries=0)`, `follow_redirects=False`, `trust_env=False`, отсутствие application retry loop и HTTP auth resend. Один вызов не имеет remote side effect. Отсутствие повторов — сознательное решение этого ограниченного опыта, а не запрет retry для всех read-only операций.

Проверяйте последовательно по три операции каждой строки, с concurrency=1 на стороне Quote caller. Control: full/empty, всего 6; defect: все 11 строк, 33; fixed: те же 33; recovery: full/empty, 6. Затем три URL-подобных item_id (`http://evil.test:9999/x`, `//evil.test`, `p-7?host=evil`) должны получить 422 без outbound attempts. Дополнительный query `base_url=http://evil.test` при допустимом item_id не должен менять authority; этот четвёртый negative check делает одну легитимную попытку. Получаются 82 входящих проверки и 79 исходящих попыток. Это тест trusted configuration, не доказательство SSRF protection.

HTTPX connect/read/write/pool timeout — по 100 мс. Измеряйте время от отправки запроса к Quote через ASGI до полного ответа, требуйте <500 мс для **каждой** операции. Это порог наблюдения конечного loopback-профиля, не общий deadline для произвольной сети: read timeout относится к ожиданию очередных данных, а streaming trickle здесь не моделируется. В каждом опыте запишите фактическую duration; фиксированной интенсивности RPS и нагрузочного p95 этот набор не задаёт.

На каждом request ID сохраните начало исходящей попытки, приём Pricing, response status/media/bytes либо тип transport exception, решение адаптера, status и JSON Quote, elapsed time. Считайте attempts на HTTP-client boundary и независимо server receipts; одного счётчика вызовов wrapper недостаточно для выводов о hidden retry. Для каждой допустимой операции требуется 1/1. Отдельно считайте false_absence только среди девяти failure rows: ложное отсутствие — их результат no_offers. На defect ожидается 27/27, после исправления — 0/27; full и empty проверяются отдельно и должны сохраняться во всех профилях.

После каждой строки измеряйте drain ≤1 с: active Pricing handlers=0, незавершённой client work нет. Timeout не означает, что Pricing уже остановился: его 350-мс работа должна закончиться до переключения режима. Recovery идёт на том же клиенте без правки данных. После всех запросов закройте lifespan ≤1 с, проверьте client.is_closed, завершите Pricing thread/server и проверьте закрытие порта ≤1 с. Полностью прочитанные responses освобождены; контролируемые ресурсы имеют одного владельца. Не требуется повторный эксперимент по размеру пула.

Авторский опыт на этом baseline дал 79 attempts/79 receipts, 27 ложных отсутствий на defect и 0 на fixed; recovery 6/6. В итоговом прогоне общий цикл до client close занял 1769.16 мс, максимум отдельного Quote response — 117.71 мс, максимальный drain — 254.86 мс, client close — 0.07 мс, server cleanup с port check — 126.36 мс. Это ориентир воспроизводимости; собственные измерения участника обязательны. Probe исполнялся из stdin без сохранения файлов, готовой реализации не предоставляется.


## Что передать на проверку

Сохраните команды запуска и очистки своего стенда, точные версии и конфигурацию клиента. Отчёт должен показывать отдельно control, defect, fixed и recovery, а не только последний зелёный запуск.

Для каждой строки приведите request ID и цепочку Pricing response/failure → adapter outcome → Quote status/body. Приложите исходные записи и их сводку: число операций, attempts, receipts, false_absence, длительности, состояние client work и ресурсов. Покажите, что новая regression check падает на seeded defect и проходит после его удаления. Если проверка ожидает ошибочное поведение для демонстрации, подпишите это как reproduction check, не как выполнение контракта.

Короткая записка объясняет, где терялось различие и почему исправление не уничтожило valid empty. Включите остаточный риск: ASGI вход Quote не проверяет production proxy/TLS, а один finite response profile не подтверждает поведение произвольной сети.

## Критерии оценки L1

| Что проверяется | Почему это нужно | Принимаемое evidence |
|---|---|---|
| Выполнение известных исходов | Сам факт ошибки ещё не означает правильный mapping | Все 11 строк с фиксированным Quote status/body |
| Сохранение пустого успеха | «Всегда 502» тоже устраняет ложное отсутствие, но ломает функцию | Full и empty проходят до, на дефекте и после |
| Один seeded defect | Несколько изменений не позволяют связать исправление с причиной | Разница исходного/исправленного состояния только в collapse failure→empty |
| Реальная клиентская граница | Готовый mock результата скрывает decoding defect | HTTPX получает status/media/bytes; timeout/transport действительно возникают |
| Одна попытка | Замаскированный retry меняет договор и нагрузку | Per-ID attempts=receipts=1; retries=0 и нет loop |
| Завершение работы | 504 сам по себе не освобождает remote work | Drain/client/server/port checks в заданных bounds |
| Воспроизводимость | Один случайный зелёный ответ не является регрессией | Команда, версии, control/defect/fixed/recovery и сохранённые записи |

Ошибки применения не компенсируются дополнительными тестами других возможностей. 404/204 с пустым телом — полезные дополнительные edge checks по заданному правилу status; их не смешивают со знаменателем основной матрицы. Missing offers, null и чужой item_id уже включены в обязательные строки.

## Подсказки по мере необходимости

<details>
<summary>1. Найдите место появления ложного факта</summary>

Выберите один malformed request ID и сопоставьте вход HTTPX и выход Quote. Где впервые появляется пустой список, которого не было в корректном ответе Pricing? Начните с этого перехода, а не с числа retries.

</details>

<details>
<summary>2. Разделите допуски к интерпретации</summary>

Полный ответ транспорта, допустимый status, media type, JSON parsing, schema и identity отвечают на разные вопросы. Ошибка раннего этапа не разрешает делать вывод более позднего предметного этапа.

</details>

<details>
<summary>3. Проверьте симметричную ошибку</summary>

После исправления проверьте настоящий empty. Если он стал ошибкой вместе со всеми остальными, вы перестали лгать об отказе, но сломали корректное отсутствие. Нужны обе стороны различия.

</details>

## Вопросы после выполнения

### Почему null не просто другая запись пустого массива?

<details>
<summary>Ответ</summary>

Договор разрешает массив и требует его присутствия. null имеет иной тип. Принимая его как пустой список без изменения договора, вы снова применяете default-empty и скрываете нарушение внешних данных.

</details>

### Follow-up: почему успешный unit-test готового no_offers не подтверждает исправление?

<details>
<summary>Ответ</summary>

Он начинает после разбора HTTP-ответа, где и возникает дефект. Внутри такой проверки malformed bytes не могут попасть в настоящий адаптер, поэтому её зелёный сигнал не отличает исходную систему от исправленной.

</details>

### Почему retry не входит в ваше исправление?

<details>
<summary>Ответ</summary>

Задан один read-only вызов и известные исходы. Повтор меняет число попыток и время ответа, а подмена failure пустотой останется возможной и после последней попытки. Эта kata требует применить уже выбранную политику, не заменить её.

</details>

## Границы и словарь

Не добавляйте fan-out, pool tuning, circuit breaker, retries, authentication, БД, arbitrary callback URL, SSRF или verification portfolio всего сервиса. Не требуется публиковать ImplementationReference. Самостоятельный выбор внутренней модели и её защита относятся к [проекту L2](../project-spec/integrate-one-pricing-operation.md).

- **Decoding** — превращение HTTP JSON bytes в значения.
- **Schema validation** — проверка обязательных полей, типов и ограничений.
- **Attempt** — один исходящий HTTP request.
- **Seeded defect** — намеренно внесённая известная ошибка для проверки обнаружения.
- **False absence** — no_offers, полученное из failure row.
- **Drain** — ожидание завершения начатой работы до смены режима.
- **Cleanup** — закрытие принадлежащих стенду ресурсов.
- **Coercion** — автоматическое приведение типа внешнего значения.

## Источники и применимость

Проверено 2026-09-08 на Python 3.14.0, FastAPI 0.137.1, Starlette 1.3.1, HTTPX 0.28.1 и Pydantic 2.12.5; транзитивные httpcore 1.0.9 и AnyIO 4.11.0. Это исполненный baseline. Обнаруженные stable версии: [Python 3.14.7](https://www.python.org/downloads/), [FastAPI 0.141.1](https://pypi.org/project/fastapi/), [Starlette 1.6.0](https://pypi.org/project/starlette/), [Pydantic 2.13.5](https://pypi.org/project/pydantic/); [HTTPX 0.28.1](https://pypi.org/project/httpx/) остаётся stable, 1.0.dev6 — предварительная версия. Новые версии не исполнялись. Python baseline отстаёт на несколько patch releases; перед переносом повторите матрицу, strict validation и закрытие ресурсов. Эти pins не являются рекомендацией для production.

- [HTTPX transports](https://www.python-httpx.org/advanced/transports/) объясняет transport retries и границу request/response; ASGITransport не запускает lifespan автоматически.
- [HTTPX timeouts](https://www.python-httpx.org/advanced/timeouts/) различает connect/read/write/pool ожидания; одинаковые значения не составляют общий deadline.
- [HTTPX exceptions](https://www.python-httpx.org/exceptions/) задаёт классы транспортных отказов и timeout.
- [FastAPI lifespan](https://fastapi.tiangolo.com/advanced/events/) описывает создание общего ресурса до yield и закрытие после.
- [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/) объясняет ограничение автоматического приведения типов; фактическое отклонение строковой суммы проверяется отдельной строкой.
- [RFC 9110, safe methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.1) задаёт read-only смысл GET; реальная операция Pricing дополнительно обязана не создавать бизнес-запись.

Численные пороги относятся к конечному локальному опыту, а не к production SLO. TLS, proxy, DNS, SSRF, disconnect и насыщение пула этим опытом не доказываются.
