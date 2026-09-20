---
id: b2.project-spec.integrate-one-pricing-operation
kind: project-spec
title: Проект — самостоятельно интегрировать одну операцию Pricing
owner_track: b2
module: b2.module.external-service-integration
coverage:
  - target: b2.level-outcome.integrate-external-services-l2-design-typical-client-boundary
    role: integrate
  - target: b2.level-outcome.integrate-external-services-l2-design-typical-client-boundary
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

# Подключить Pricing и сохранить смысл ответа

Вы отвечаете за небольшое Quote API. Покупатель должен отличать ситуацию «продавец не предлагает товар» от ситуации «сервис не смог получить предложение». Pricing является внешней зависимостью (dependency): даже ответ с HTTP 200 может оказаться непригодным. Команда уже задала публичные исходы Quote, но ещё не выбрала внутреннее представление результата и ошибок клиентского адаптера — кода, переводящего ответ Pricing в понятные сервису варианты.

Нужно самостоятельно интегрировать **одну** read-only операцию и доказать её поведение. Предметное отсутствие (business absence) — валидный пустой результат. Сбой интеграции (integration failure) — невозможность получить или понять ответ по договору. Эти варианты должны оставаться различимыми на всём пути.

Проект выполняется участником в отдельном репозитории. Здесь нет scaffold, готового адаптера, архитектуры или эталонного решения. Заданы продуктовый договор, воспроизводимый контур и наблюдаемые результаты. Вы выбираете внутренние result/error types, границы их преобразования, организацию клиента и проверок; это самостоятельное действие [External L2](../../../level-outcomes.md). Простого исправления готового collapse из kata для него недостаточно.

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


## Неопределённость, которую предстоит разрешить

Внешние HTTP status/body менять нельзя, но внутренние типы не заданы. Решите, как вызывающий код узнаёт об absence, как отличает failure и где прекращается зависимость от HTTPX/Pydantic types. Сопоставьте хотя бы два допустимых варианта представления результата и объясните последствия на конкретном пути Quote.

Определите владельца общего HTTP client: когда создаётся, как переиспользуется, кто закрывает responses и сам клиент при нормальном завершении и ошибке. Пул имеет lifecycle даже без задачи подбора capacity. Общий client в lifespan — принятый substrate; внутреннюю организацию и проверки участник выбирает сам.

Решение one-attempt задано рамкой проекта, однако его нужно обосновать и проверить. Докажите, что операция не имеет remote side effect, automatic retries отключены и нет скрытого повторного вызова. Укажите условия будущего пересмотра: новый договор, известные transient failures, выделенный budget и согласование scope. В текущей реализации повторы не добавляются.

## Этапы результата

### 1. Договор стал наблюдаемым

Учебная цель — превратить описание внешних данных в работающий integration path. Результат этапа: Quote действительно отправляет HTTP request, получает и проверяет response Pricing, возвращает полный и пустой успех. Зафиксированы версии, trusted configuration, resource owner и связь request identity с payload. Реальный запрос к собранному Quote должен пройти через ваш настоящий адаптер.

Покажите внешнюю форму ответа и выбранные внутренние варианты. Рецензент должен видеть место, где wire contract — status, media type, поля и типы переданных данных — перестаёт быть деталями вызывающего сервиса.

### 2. Каждый отказ остался отказом

Учебная цель — самостоятельно построить границу, которая не теряет смысл при невалидных данных и частичном отказе взаимодействия. Результат этапа: полная матрица имеет наблюдения на всех трёх границах — HTTPX, adapter, Quote. Порядок ваших проверок обоснован примером, который нарушится при перестановке.

Для доказательства различающей силы проверок временно включите один collapse failure→empty, сохранив корректный код остального пути. Покажите исходную ошибку и падение контрактных expectations, затем уберите мутацию. Это контроль качества evidence проекта, а не замена автономной интеграции задачей kata. Репорт не может состоять только из unit-тестов готовых внутренних результатов.

### 3. Клиент восстановился и завершил работу

Учебная цель — подтвердить ресурсный договор, а не только получить правильные error codes. Результат этапа: здоровые full/empty после снятия отказа на том же клиенте, без правки данных; завершение работы и закрытие ресурса в объявленном времени. Timeout не считается доказательством отмены Pricing. Покажите отдельный drain и lifecycle closure.

### 4. Решение можно проверить и пересмотреть

Учебная цель — связать самостоятельный выбор с фактами и пределами. Передайте engineering decision: контекст, внутреннее представление, mapping matrix, владелец клиента, one-attempt decision, альтернативы, последствия, измерения, остаточные риски и trigger пересмотра. Другой инженер должен воспроизвести заявленные исходы вашими командами.

Организация этапов, структура файлов и последовательность коммитов остаются за вами. Не нужно вводить framework ради проверки этой операции.

## Контур опыта и доказательства

Используйте FastAPI Quote, общий HTTPX AsyncClient в lifespan и локальный HTTP Pricing; ASGITransport допустим на входе Quote, но lifespan запускается явно. Исходящий HTTP transport настоящий. Закреплены `AsyncHTTPTransport(retries=0)`, `follow_redirects=False`, `trust_env=False`, отсутствие application retry loop и HTTP auth resend. Один вызов не имеет remote side effect. Отсутствие повторов — сознательное решение этого ограниченного опыта, а не запрет retry для всех read-only операций.

Проверяйте последовательно по три операции каждой строки, с concurrency=1 на стороне Quote caller. Control: full/empty, всего 6; defect: все 11 строк, 33; fixed: те же 33; recovery: full/empty, 6. Затем три URL-подобных item_id (`http://evil.test:9999/x`, `//evil.test`, `p-7?host=evil`) должны получить 422 без outbound attempts. Дополнительный query `base_url=http://evil.test` при допустимом item_id не должен менять authority; этот четвёртый negative check делает одну легитимную попытку. Получаются 82 входящих проверки и 79 исходящих попыток. Это тест trusted configuration, не доказательство SSRF protection.

HTTPX connect/read/write/pool timeout — по 100 мс. Измеряйте время от отправки запроса к Quote через ASGI до полного ответа, требуйте <500 мс для **каждой** операции. Это порог наблюдения конечного loopback-профиля, не общий deadline для произвольной сети: read timeout относится к ожиданию очередных данных, а streaming trickle здесь не моделируется. В каждом опыте запишите фактическую duration; фиксированной интенсивности RPS и нагрузочного p95 этот набор не задаёт.

На каждом request ID сохраните начало исходящей попытки, приём Pricing, response status/media/bytes либо тип transport exception, решение адаптера, status и JSON Quote, elapsed time. Считайте attempts на HTTP-client boundary и независимо server receipts; одного счётчика вызовов wrapper недостаточно для выводов о hidden retry. Для каждой допустимой операции требуется 1/1. Отдельно считайте false_absence только среди девяти failure rows: ложное отсутствие — их результат no_offers. На defect ожидается 27/27, после исправления — 0/27; full и empty проверяются отдельно и должны сохраняться во всех профилях.

После каждой строки измеряйте drain ≤1 с: active Pricing handlers=0, незавершённой client work нет. Timeout не означает, что Pricing уже остановился: его 350-мс работа должна закончиться до переключения режима. Recovery идёт на том же клиенте без правки данных. После всех запросов закройте lifespan ≤1 с, проверьте client.is_closed, завершите Pricing thread/server и проверьте закрытие порта ≤1 с. Полностью прочитанные responses освобождены; контролируемые ресурсы имеют одного владельца. Не требуется повторный эксперимент по размеру пула.

Авторский опыт на этом baseline дал 79 attempts/79 receipts, 27 ложных отсутствий на defect и 0 на fixed; recovery 6/6. В итоговом прогоне общий цикл до client close занял 1769.16 мс, максимум отдельного Quote response — 117.71 мс, максимальный drain — 254.86 мс, client close — 0.07 мс, server cleanup с port check — 126.36 мс. Это ориентир воспроизводимости; собственные измерения участника обязательны. Probe исполнялся из stdin без сохранения файлов, готовой реализации не предоставляется.


## Пакет evidence участника

Передайте исходный код своего проекта, manifest точных версий и команды воспроизведения/cleanup. Команды не должны требовать ручной правки бизнес-данных между профилями. Отдельно сохраните raw observations и сводку по каждой строке и профилю, включая незавершённые операции или потерянные записи как неуспешную проверку, а не как нулевые ошибки.

Decision record должен объяснять хотя бы один отвергнутый внутренний вариант. Например, причина выбора union вместо exceptions должна ссылаться на то, как caller различает исходы, а не на универсальное превосходство паттерна. Строгое отклонение дополнительных полей зафиксировано для этой лаборатории; опишите, почему перенос на расширяемый vendor contract потребует пересмотра.

Выполните review с другим инженером либо отдельно запущенным reviewer и обработайте findings в своём репозитории. Приложите результат проверки и короткую ретроспективу: какое исходное предположение опроверглось наблюдениями. Это требование к самостоятельному проекту участника, не заявление о независимом review авторского материала.

## Review criteria L2

| Область | Что должно быть доказано | Что не считается достаточным |
|---|---|---|
| Самостоятельная интеграция | Внутренние варианты, mapping и owner выбраны и реализованы участником | Только исправление одного заданного catch |
| Предметная правдивость | Empty сохранён; все failure rows не дают отсутствие | Только общий success rate или «всегда error» |
| Клиентская граница | Настоящий HTTPX разбирает status/media/bytes и получает transport failures | Готовый mock adapter result |
| Identity и схема | Чужой товар, missing/null и строковая сумма отклонены | JSON parsing без validation |
| Retry decision | Read-only смысл + no-retry config + per-ID counters | Один конфигурационный скриншот |
| Lifecycle | Reuse, response release, drain, recovery и shutdown наблюдаются | Создание нового клиента после каждого отказа |
| Измерение | Population, duration, точка времени, bounds и raw records согласованы | Перенос числа p95 из другой лаборатории |
| Решение | Альтернатива, последствия и условия пересмотра привязаны к фактам | Перечень паттернов без пути исполнения |

Дополнительные edge checks для 204, 404, пустого тела при 200 или неверной currency можно предъявить отдельной популяцией. Для них действуют правила статуса и схемы выше. Не изменяйте знаменатели основной 11-строчной матрицы и не выдавайте дополнительные случаи за новое proficiency coverage.

## Вопросы защиты

### Как ваше представление не позволяет ошибке стать пустым успехом?

<details>
<summary>Ориентир сильного ответа</summary>

Покажите конкретные внутренние варианты и место их обработки в Quote. Проследите malformed response до 502 и empty до 200. Объясните, что произойдёт при добавлении нового failure type и какой check обнаружит пропущенную ветвь. И union, и ограниченные исключения допустимы, если ответ подтверждён исполнением.

</details>

### Почему вы доверяете измерению количества попыток?

<details>
<summary>Ориентир сильного ответа</summary>

Начало request на HTTP-client boundary и приём Pricing сопоставлены по ID; нет retry loop, redirects и auth resend, transport retries=0. Отсутствие лишних попыток проверено на failure rows, а не только healthy. Для connect failure server receipt может отсутствовать — такой случай нужно явно выделить, не приписывать ему полученный response. Основной transport row этой лаборатории закрывает соединение уже после приёма запроса.

</details>

### Follow-up: что способно изменить ваше one-attempt решение?

<details>
<summary>Ориентир сильного ответа</summary>

Новый продуктовый договор доступности, доказанная transient failure category и бюджет времени/нагрузки могут сделать bounded retry обоснованным. Read-only — лишь одно условие. Сначала нужно согласовать рамку и проверить повторение, не добавлять retry к текущему артефакту задним числом.

</details>

### Почему вы не объявляете клиент готовым к любой production dependency?

<details>
<summary>Ориентир сильного ответа</summary>

Проверены конечные малые ответы на loopback, один процесс и последовательные вызовы. TLS/proxy/DNS, arbitrary URLs, потоковая передача, overload и remote side effects не исследовались. Lifecycle локальных ресурсов не равен гарантии отмены удалённого мира. Сильный ответ называет этот предел рядом с измерением, а не прячет в общей оговорке.

</details>

## Non-goals и остаточный долг

Не строятся fan-out, deadline propagation, pool saturation experiment, cancellation/disconnect policy, circuit breaker, retries/hedging, service discovery, БД, idempotency store, SSRF platform, distributed tracing или multi-region deployment. Сценарии [S08/S13](../../../scenarios.md) дают контекст; их каноническая runtime-механика не повторяется. Test boundaries служат evidence интеграции, не отдельному Verification coverage.

External L3 degraded-dependency ownership и L4 cross-team policy не заявляются. Нет доказательства module completion и нет автоматической регистрации ImplementationReference; ссылка на самостоятельно выполненный проект появляется только после выполнения и review в соответствующем процессе.

## Словарь

- **Client adapter** — переводчик протокола Pricing во внутренние исходы Quote.
- **Business absence** — подтверждённое отсутствие предложения.
- **Integration failure** — техническая невозможность получить или понять ответ.
- **Decoding** — преобразование JSON bytes в значения Python.
- **Schema validation** — проверка структуры, типов и ограничений.
- **Attempt** — один исходящий HTTP request; повтор — новая попытка.
- **Lifecycle** — создание, использование и закрытие общего клиента.
- **Drain** — завершение начатой работы до смены режима или shutdown.
- **Engineering decision** — запись выбора, альтернатив, последствий и условий пересмотра.
- **Wire contract** — фактически переданные status, media type, поля, типы и identity.
- **Coercion** — автоматическое приведение внешних значений к другим типам.

## Источники и применимость

Проверено 2026-09-08 на Python 3.14.0, FastAPI 0.137.1, Starlette 1.3.1, HTTPX 0.28.1 и Pydantic 2.12.5; транзитивные httpcore 1.0.9 и AnyIO 4.11.0. Это исполненный baseline. Обнаруженные stable версии: [Python 3.14.7](https://www.python.org/downloads/), [FastAPI 0.141.1](https://pypi.org/project/fastapi/), [Starlette 1.6.0](https://pypi.org/project/starlette/), [Pydantic 2.13.5](https://pypi.org/project/pydantic/); [HTTPX 0.28.1](https://pypi.org/project/httpx/) остаётся stable, 1.0.dev6 — предварительная версия. Новые версии не исполнялись. Python baseline отстаёт на несколько patch releases; перед переносом повторите матрицу, strict validation и закрытие ресурсов. Эти pins не являются рекомендацией для production.

- [HTTPX transports](https://www.python-httpx.org/advanced/transports/) объясняет transport retries и границу request/response; ASGITransport не запускает lifespan автоматически.
- [HTTPX timeouts](https://www.python-httpx.org/advanced/timeouts/) различает connect/read/write/pool ожидания; одинаковые значения не составляют общий deadline.
- [HTTPX exceptions](https://www.python-httpx.org/exceptions/) задаёт классы транспортных отказов и timeout.
- [FastAPI lifespan](https://fastapi.tiangolo.com/advanced/events/) описывает создание общего ресурса до yield и закрытие после.
- [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/) объясняет ограничение автоматического приведения типов; фактическое отклонение строковой суммы проверяется отдельной строкой.
- [RFC 9110, safe methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.1) задаёт read-only смысл GET; реальная операция Pricing дополнительно обязана не создавать бизнес-запись.

Численные пороги относятся к конечному локальному опыту, а не к production SLO. TLS, proxy, DNS, SSRF, disconnect и насыщение пула этим опытом не доказываются.
