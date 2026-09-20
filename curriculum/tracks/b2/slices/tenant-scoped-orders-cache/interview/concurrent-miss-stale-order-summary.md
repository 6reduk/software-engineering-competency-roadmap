---
id: b2.interview.concurrent-miss-stale-order-summary
kind: interview
title: Interview — concurrent miss и stale Orders summary
owner_track: b2
module: b2.module.transactional-persistence-integration
coverage:
  - target: b2.level-outcome.integrate-application-caching-l2-apply-known-cache-pattern
    role: probe
  - target: b2.level-outcome.integrate-application-caching-l3-design-consistency-failure-behavior
    role: probe
status: accepted
updated: 2026-09-03
language: ru
last_verified: 2026-09-01
versions:
  python: 3.14.0
  fastapi: 0.137.1
  starlette: 1.3.1
  uvicorn: 0.49.0
  redis: 8.4.5
  redis_py: 8.0.1
  postgresql: 18.6
  psycopg: 3.3.4
---

# Interview: concurrent miss и stale Orders summary

## Кейс

Orders service предоставляет `GET /orders/summary`. PostgreSQL — source of truth; Redis хранит JSON сводки с TTL 2 с. Trusted `IdentityContext.tenant_id` уже построен из проверенного credential. Key задан как `orders-summary:v1:{trusted_tenant_id}`. Один Uvicorn worker обслуживает asyncio tasks; несколько workers не заявлены.

После истечения TTL 32 одновременных запроса tenant-a выполняют почти 32 одинаковых SELECT. Команда предлагает process-local coalescing. Одновременно write operation может committed v2 и выполнить `DEL`, пока ранее начавшийся reader ещё держит v1. При Redis outage продукт готов вернуть `503`, но не готов бесконтрольно направить трафик в PostgreSQL.

## Основной вопрос

Спроектируйте read path и проверяемые подтверждения (`evidence`): как ограничить source-read amplification, какую старую версию допустимо вернуть после commit, что измерять при race/outage/recovery и где заканчивается доказанная гарантия?

<details>
<summary>Ориентиры сильного рассуждения</summary>

Сильный ответ сначала формулирует инварианты: tenant-safe key/value, TTL и максимум 2.25 с stale после commit, не более одного source read на 32-request cold burst в одном process при успешном fill, fail-closed `503` и ноль source reads при отказе `GET` до обращения к PostgreSQL.

На miss нужен один владелец per key и повторный `GET` после ожидания. `asyncio.Lock` не синхронизирует workers, поэтому граница применимости утверждения остаётся one-process. Writer инвалидирует после commit. Кандидат явно воспроизводит late fill: SQL statement reader-а начался до commit и увидел v1, writer committed v2 и сделал `DEL`, reader записал v1 с TTL, уменьшенным на время с начала statement. `SET` завершается внутри отдельного бюджета 250 мс, поэтому v1 исчезает не позже `statement_start + 2 с + 250 мс ≤ commit + 2,25 с`.

Evidence сочетает status/body tenant/version и counters: hit/miss/error, source reads на key, fallback `503`, invalidation errors. При контролируемом отказе cache adapter до `GET` 32/32 requests завершаются `503` без PostgreSQL; recovery снова даёт 32 корректных `200` и не более одного source read. Низкая amplification при чужом tenant или вечной v1 не принимается.

</details>

## Уточнения от L2 к L3

### 1. Почему key недостаточно построить из query `tenant_id`?

<details>
<summary>Ответ и объяснение</summary>

Query принадлежит клиенту и не повышает полномочия. Он позволит tenant-a выбрать key tenant-b. Key строится из server-created trusted context; tenant повторяется внутри value для проверки corruption. Нужен тест с forged query/header и двумя наборами заранее подготовленных тестовых данных (`fixtures`).

</details>

### 2. Что сломано в «обернём SELECT в lock»?

<details>
<summary>Ответ и объяснение</summary>

Если после входа в lock не повторить `GET`, все waiters последовательно выполнят SELECT. Параллелизм исчезнет, но число source reads останется близким к числу запросов. Проверка должна считать reads, а не только одновременные connections.

</details>

### 3. Как меняется граница утверждения при четырёх Uvicorn workers?

<details>
<summary>Ответ и объяснение</summary>

У каждого process своя память и lock registry. Один key может получить до четырёх владельцев загрузки — по одному на worker. Для общей гарантии понадобится внешний coordination mechanism и B5 readiness либо честный новый threshold `≤4`; текущий evidence нельзя расширять словами.

</details>

### 4. Почему commit → `DEL` не гарантирует немедленную v2?

<details>
<summary>Ответ и объяснение</summary>

SQL statement reader-а мог начаться до commit и увидеть v1, но выполнить `SET` после `DEL`. Это late fill. Перед `SET` полный TTL уменьшается на время с начала statement; при исчерпанном остатке fill пропускается, а сам `SET` ограничен отдельным бюджетом 250 мс. Чтобы обещать read-your-writes, нужен другой механизм и новое решение.

</details>

### 5. Что происходит, если `DEL` не удался после commit?

<details>
<summary>Ответ и объяснение</summary>

Database result уже подтверждён и не откатывается из-за cache. Сервис фиксирует invalidation error. Пока Redis недоступен, reads fail-closed; после восстановления старый key ограничен оставшимся TTL. Если продукт требует немедленной видимости, этот исход неприемлем и Gate 0 нужно менять.

</details>

### 6. Почему прямой database fallback на Redis error опасен?

<details>
<summary>Ответ и объяснение</summary>

При полном outage каждый request станет miss и может создать request-for-request source load, умноженную на workers. Fail-open допустим только с отдельным подтверждением ограниченного admission/coalescing. В текущем контракте initial или repeated `GET` failure происходит до PostgreSQL и даёт `503 cache_unavailable`, `source_read=0`. Отказ `SET` происходит уже после source read: внешний ответ тот же, fill отсутствует, но `source_read≥1`, а последовательные владельцы burst могут довести число чтений до `N`.

</details>

### 7. Какие наблюдения различают хороший и ложноположительный результат?

<details>
<summary>Ответ и объяснение</summary>

Нужны одновременно response status, tenant, `data_version`, время до v2 и source reads на key. `source_read=1` при stale v1 после 2.25 с — провал freshness; 32 правильных `200` при 32 reads — провал amplification; 32 `503` после recovery — провал восстановления.

</details>

### 8. Чем application freshness отличается от HTTP caching и database consistency?

<details>
<summary>Ответ и объяснение</summary>

Redis TTL — локальная политика производного value. HTTP freshness управляет повторным использованием response intermediaries/clients; здесь оно запрещено `Cache-Control: no-store`. PostgreSQL consistency определяет видимость committed rows. Ни один слой автоматически не переносит гарантию на другой.

</details>

## Rubric для интервьюера

- **Слабый ответ:** называет Redis, TTL и lock, но не задаёт trusted key, race, failure outcome или группу однотипных измерительных прогонов (`measurement population`).
- **Уверенный L2:** применяет cache-aside, tenant-safe key, TTL, double-check coalescing и tests hit/miss/isolation/failure в заданной topology.
- **Сильный L3:** самостоятельно формулирует freshness invariant, воспроизводит late fill, разделяет commit и invalidation, защищает fail-closed trade-off, связывает counters с правильностью response и ограничивает claim одним process.
- **Ложная глубина:** предлагает distributed lock без lease/failure semantics либо обещает zero stale благодаря `DEL`; термины не заменяют доказательство.

Interview имеет роль `probe`: даже сильное рассуждение не заменяет execution evidence project specification.

## Локальный словарь и источники

- **Amplification** — число source reads, созданных одной входной population для одного key.
- **Late fill** — заполнение cache старым snapshot после commit/invalidation новой версии.
- **Bounded fallback** — заранее ограниченный исход при cache failure; здесь fail-closed `503` без source read.
- **Claim boundary** — граница применимости утверждения: one-process topology, за пределы которой экспериментальный вывод не переносится.

Источники: [Redis `SET`](https://redis.io/docs/latest/commands/set/), [Redis `DEL`](https://redis.io/docs/latest/commands/del/), [redis-py async/timeouts](https://redis.io/docs/latest/develop/clients/redis-py/async/), [Python `asyncio.Lock`](https://docs.python.org/3.14/library/asyncio-sync.html#lock), [FastAPI process memory](https://fastapi.tiangolo.com/deployment/concepts/#replication-processes-and-memory), [PostgreSQL Read Committed](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED) и [Gate 0](../../../../../../governance/work-packages/M1.8.13-application-caching-s15-slice.md#gate-0--b3-cache-store-и-применимая-b5-coordination-readiness).
