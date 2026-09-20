---
id: b2.project-spec.resilient-orders-summary-cache
kind: project-spec
title: Project — resilient tenant Orders summary cache
owner_track: b2
module: b2.module.transactional-persistence-integration
coverage:
  - target: b2.level-outcome.integrate-application-caching-l2-apply-known-cache-pattern
    role: integrate
  - target: b2.level-outcome.integrate-application-caching-l2-apply-known-cache-pattern
    role: assess
  - target: b2.level-outcome.integrate-application-caching-l3-design-consistency-failure-behavior
    role: integrate
  - target: b2.level-outcome.integrate-application-caching-l3-design-consistency-failure-behavior
    role: assess
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

# Project: resilient tenant Orders summary cache

## Рабочая ситуация

Orders service вычисляет `GET /orders/summary` из PostgreSQL. Cache снижает повторные reads, но три риска остались неявными: burst misses усиливают PostgreSQL, invalidation может проиграть late fill старой версии, а cache outage превращается либо в недоступность, либо в неконтролируемый fallback. Ошибка key дополнительно способна смешать tenants.

Выполните самостоятельный интеграционный milestone одного сервиса: реализуйте закреплённый cache-aside contract и защитите его исходными проверяемыми результатами (`raw evidence`) для hit, cold miss, concurrent burst, commit/invalidation race, tenant isolation, Redis failure и recovery. Стартового repository, готовой архитектуры, эталонного кода и ImplementationReference нет.

## Закреплённый substrate и contract

- CPython 3.14.0, FastAPI 0.137.1, Starlette 1.3.1, Uvicorn 0.49.0;
- один Uvicorn worker/process и один asyncio event loop;
- PostgreSQL 18.6 + Psycopg 3.3.4 как source of truth;
- Redis 8.4.5 без persistence + redis-py 8.0.1, один async client/pool на lifespan;
- `GET /orders/summary`, trusted `IdentityContext.tenant_id`, `Cache-Control: no-store`;
- `200` value: `tenant_id`, `data_version`, `open_orders`, `total_cents`, `source_updated_at`, `generated_at`;
- cache error: `503 application/problem+json`, `code=cache_unavailable`, `Retry-After: 1`;
- source timeout/error на miss: `503 application/problem+json`, `code=summary_source_unavailable`, `Retry-After: 1`, без cache fill;
- key `orders-summary:v1:{trusted_tenant_id}`, JSON `schema_version=1`, TTL 2 с;
- redis-py 8.0.1 с явно отключёнными автоматическими retry — `Retry(NoBackoff(), 0)` или наблюдаемо эквивалентная конфигурация; pool 64;
- внешний budget 250 мс на каждую Redis-команду, например task-level timeout;
- freshness anchor — начало SQL statement; перед `SET` вычисляется `remaining_ttl = max(0, 2 секунды − elapsed_since_statement_start)`, при нулевом остатке fill пропускается, а `SET` должен завершиться внутри собственного 250-мс command budget;
- write order: PostgreSQL commit, затем `DEL` tenant key.

Заранее подготовленные тестовые данные (`fixtures`): tenant-a v1 `(3, 12500)`, tenant-b v1 `(7, 91000)`; write переводит tenant-a в v2 `(4, 15000)`. Любое client-supplied tenant значение не меняет trusted scope.

## Invariants

1. **Tenant key/value:** разные tenants не разделяют key/value; value tenant совпадает с trusted context.
2. **Freshness:** после commit v1 допустима не дольше 2.25 с: `statement_start + 2 с + 250 мс ≤ commit + 2,25 с`; затем следующий успешный response имеет v2.
3. **Amplification:** один 32-request cold burst в одном process при успешном fill создаёт не более одного PostgreSQL read на key; при продолжающемся `SET` failure число последовательных reads ограничено `N` запросами.
4. **Failure:** Redis outage даёт ограниченный по времени `503`, не source fallback; recovery возвращает controlled range.
5. **Bounded claim:** граница применимости подтверждения не распространяется на несколько workers, distributed coordination, production capacity или Cache L4.

## Milestones и наблюдаемые результаты

### 1. Source/cache boundary и lifecycle

Зафиксируйте schema, fixtures, trusted key construction и владельцев ресурсов. Redis client создаётся один раз на application lifespan и закрывается на shutdown. Покажите, что очистка Redis не теряет авторитетные данные, а `Cache-Control: no-store` отделяет HTTP cache.

**Результат:** executable startup/shutdown check, key/value contract и два tenant fixtures.

### 2. L2 normal path

Реализуйте hit, cold miss, TTL и fail-closed error mapping. Выбор структуры adapters и application operation принадлежит участнику; framework handler не должен быть единственным местом бизнес-инвариантов.

**Результат:** contract/component checks, один cold read, двадцать hits, негативная серия cross-tenant проверок и сохранённые counters.

### 3. Concurrent miss boundary

Сначала сохраните дефектный baseline, затем ограничьте amplification на key. Coordination должна иметь явный lifecycle и не блокировать независимый tenant. Проверьте cancellation/error владельца и отсутствие stuck waiters.

**Результат:** пять повторяемых 32-request bursts до/после, source-read counts и explanation one-process boundary.

### 4. Commit/invalidation race

Создайте управляемую паузу после чтения v1, но до cache fill. Пока reader остановлен, committed v2 и выполните `DEL`; затем разрешите late fill. Не заменяйте race случайным sleep без сигнала достигнутой точки.

**Результат:** timeline с commit/delete/fill, немедленно допустимая v1 и наблюдаемая v2 не позже 2250 мс. Отдельно покажите rollback: он не создаёт invalidation новой версии.

### 5. Cache failure и recovery

Воспроизведите correctness-отказ контролируемой fault injection в точке подмены cache adapter до `GET`. Не меняйте source fixture. Проверьте весь 32-request failure burst и затем восстановите adapter. Фактическое выключение Redis/Docker можно выполнить дополнительно как host-dependent диагностику без переносимого wall-clock threshold.

**Результат:** 32 `503`, source reads `0`, завершение в пределах порога; recovery burst — 32 корректных `200`, source reads `≤1`, без cross-tenant value. Отдельный outcome для post-read `SET` failure: `503 cache_unavailable`, fill отсутствует, `source_read≥1`; если `SET` продолжает падать, последовательные владельцы burst могут выполнить до `N` source reads без зависших waiters.

### 6. Decision record и защита

Оформите решение с контекстом, выбранным fail-closed contract, альтернативами и trigger пересмотра. Обязательные альтернативы: необъединённый cache-aside, process-local coalescing, bounded fail-open и внешняя lease/lock coordination. Последняя не реализуется только ради сравнения.

**Результат:** ADR, raw observations, обработанные findings независимого review и список claims, которые проект намеренно не делает.

## Условия отказа и измерения (`failure/measurement envelope`)

Каждая строка задаёт группу однотипных прогонов (`population`), условия воспроизведения и относящийся только к ней порог принятия.

| Population | Условия | Acceptance |
|---|---|---|
| Cold miss | пустой tenant-a key, 1 request | `200` v1, `source_read=1` |
| Warm hit | тот же key, 20 requests | все `200` v1, дополнительных reads `0` |
| Concurrent miss | пять прогонов; перед каждым `DEL`; 32 tasks одновременно | каждый: 100% правильных `200`, `source_read≤1`, ≤150 мс |
| Tenant isolation | tenant-a и tenant-b misses параллельно; forged tenant inputs | разные values, leakage `0`, по одному read на key |
| Invalidation race | controlled v1 read; v2 commit; `DEL`; поздний v1 fill | v1 только внутри окна; v2 ≤2250 мс |
| Cache failure before source read | 32 tasks, fault injection в adapter до `GET`, command budget 250 мс | 32 `503`, source reads `0`, ≤350 мс |
| Cache fill failure after source read | контролируемый отказ `SET` после PostgreSQL read | `503 cache_unavailable`, fill отсутствует, `source_read≥1`; для burst допускается до `N` reads |
| Recovery | Redis снова доступен, key пуст, 32 tasks | 32 `200` v2, `source_read≤1`, ≤150 мс |

Точка измерения (`measurement point`) — внутри одного process от входа read operation до application outcome. Сохраняйте распределение задержек для каждой population, status, tenant/version и counters `cache_hit`, `cache_miss`, `cache_error`, `source_read` на key, `fallback_503`, `cache_invalidation_error`. Five-burst duration и host/container configuration входят в report. Порог concurrent miss `≤150 мс` — project acceptance threshold, выбранный с запасом относительно наблюдённого Gate 0 диапазона 90.93–103.90 мс; learn и kata могут проверять тот же correctness без этого performance threshold.

Если локальный host не выдерживает временной threshold, можно предложить новый после отдельного baseline, но нельзя ослабить 100% correctness, tenant isolation, `source_read≤1`, fail-closed zero-read или freshness semantics.

## Обязательные failure scenarios

1. Cached JSON имеет чужой `tenant_id` или неизвестную schema version.
2. Владелец concurrent load получает cancellation/exception до fill.
3. Redis `GET` превышает внешний command budget 250 мс.
4. Остаточный TTL исчерпан до fill либо Redis `SET` не завершился в своём 250-мс command budget.
5. PostgreSQL write откатывается до commit.
6. PostgreSQL commit успешен, `DEL` не выполнен.
7. Reader делает late fill v1 после successful `DEL` v2.
8. Redis восстанавливается после серии из 32 outage requests.
9. Конфигурация запускается с двумя workers — как отрицательная демонстрация границы, не как acceptance distributed guarantee.

Для каждого укажите invariant, наблюдение, внешний outcome и предел доказательства. Девятый сценарий не требует исправления, но запрещает скрыть расширение topology.

## Review criteria

### Correctness и consistency

- [ ] Tenant берётся только из trusted context; key/value checks не допускают leakage.
- [ ] Source of truth и cache ownership различены.
- [ ] TTL/freshness сформулированы через version и post-commit time.
- [ ] Commit → invalidation ordering и late-fill outcome воспроизведены.

### Concurrency и failure

- [ ] Source-read amplification измеряется на key для всей группы прогонов.
- [ ] Coordination ограничена одним process и очищается после success/error/cancellation.
- [ ] Cache outage не вызывает source fallback.
- [ ] Recovery проверяет response correctness и source reads, а не только `PING`.

### Проверяемые подтверждения и решение

- [ ] Raw results позволяют пересчитать thresholds.
- [ ] Первый отклонённый baseline сохранён или честно описан.
- [ ] ADR сравнивает alternatives и называет trigger нового Gate 0.
- [ ] Cache L2 и L3 имеют раздельные подтверждения: normal pattern/isolation против race/failure/recovery design.
- [ ] Нет готового решения, фиктивного ImplementationReference или Cache L4 claim.

## Вопросы защиты

Почему этот проект доказывает L2 и L3 разными наблюдениями?

<details>
<summary>Что должен раскрыть ответ</summary>

L2 — корректное самостоятельное применение pattern: key, TTL, hit/miss, invalidation, failure и isolation. L3 — выбранная consistency/failure boundary: late-fill race, commit order, measurable amplification, outage trade-off и recovery. Один green hit test не доказывает L3.

</details>

Какое решение изменится первым при переходе к четырём workers?

<details>
<summary>Что должен раскрыть ответ</summary>

Coalescing claim: process-local state больше не ограничивает весь instance. Нужно либо принять threshold до четырёх reads, либо выбрать внешнюю coordination semantics и пройти B5 Gate. Остальные thresholds также перепроверяются в новой topology.

</details>

Почему v1 после `DEL` не всегда является дефектом реализации?

<details>
<summary>Что должен раскрыть ответ</summary>

Reader мог получить v1 до commit и записать её после delete. В текущем контракте это допустимый late fill, если v2 появляется в freshness bound. Дефект — обещать немедленную свежесть или превышать 2.25 с, а не само существование race outcome.

</details>

## Non-goals и известный долг

- distributed lock/lease, Redis Cluster/Sentinel, multi-region и cross-service migration;
- write-through, write-behind, event-driven invalidation и universal TTL;
- PostgreSQL query tuning или production capacity program;
- zero-stale, linearizability, exactly-once invalidation или read-your-writes;
- готовая реализация и регистрация ImplementationReference.

Cache L4 остаётся отдельным долгом с mixed-version migration, несколькими сервисами и production feedback.

## Словарь и источники

- **Evidence population** — точно заданная группа однотипных requests, для которой сохраняется проверяемое подтверждение и проверяется threshold.
- **Invalidation error** — неуспешное удаление cache key после уже подтверждённого database commit.
- **Recovery** — возврат корректных responses и bounded source reads после прекращения cache failure.
- **Decision trigger** — изменение требований/topology, которое требует пересмотра ADR и Gate 0.

Первичные источники и точные версии перечислены в [Gate 0](../../../../../../governance/work-packages/M1.8.13-application-caching-s15-slice.md#gate-0--b3-cache-store-и-применимая-b5-coordination-readiness); предметная модель раскрыта в [brief](../learn/cache-aside-freshness-coalescing.md).
