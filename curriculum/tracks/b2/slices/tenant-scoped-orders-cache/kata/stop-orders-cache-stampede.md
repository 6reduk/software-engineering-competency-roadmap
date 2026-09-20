---
id: b2.kata.stop-orders-cache-stampede
kind: kata
title: Kata — stop Orders cache stampede
owner_track: b2
module: b2.module.transactional-persistence-integration
coverage:
  - target: b2.level-outcome.integrate-application-caching-l2-apply-known-cache-pattern
    role: practice
  - target: b2.level-outcome.integrate-application-caching-l2-apply-known-cache-pattern
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

# Kata: stop Orders cache stampede

## История

Orders service отвечает на `GET /orders/summary`. Tenant A имеет сводку v1: три открытых заказа на 12500 cents. Redis key `orders-summary:v1:tenant-a` живёт 2 с. На hit всё работает, но сразу после удаления key burst из 32 requests выполняет почти 32 одинаковых PostgreSQL reads.

Стартового scaffold нет. Создайте минимальную систему самостоятельно: один Python process/event loop, read operation, управляемый Redis adapter, детерминированные исходные тестовые данные (`source fixture`) или PostgreSQL 18.6 и счётчик source reads на key. `IdentityContext` считается готовым; tenant из query/header использовать нельзя.

## Один дефект

Исправьте только concurrent cold miss: для одного tenant-safe key один burst должен создавать не более одного source read в закреплённом process. Не добавляйте invalidation-race protocol, несколько workers, distributed lock или production rollout — они относятся к project, а не к этой kata.

## Контракты, которые нужно сохранить

- key: `orders-summary:v1:{trusted_tenant_id}`;
- value: `schema_version`, `tenant_id`, `data_version`, `open_orders`, `total_cents`, `source_updated_at`, `generated_at`;
- TTL: 2 с;
- freshness anchor — начало SQL statement; перед `SET` TTL уменьшается на прошедшее с этого момента время, а при нулевом остатке fill пропускается с `503 summary_source_unavailable`;
- hit не читает source;
- redis-py 8.0.1 имеет явно отключённые автоматические retry (`Retry(NoBackoff(), 0)` или наблюдаемо эквивалентная конфигурация), а каждая Redis-команда ограничена внешним budget 250 мс;
- контролируемый error/timeout cache adapter до `GET` даёт `503 cache_unavailable` без source fallback и с `source_read=0`;
- response другого tenant никогда не возвращается;
- один worker/process — явная граница claims.

## Ограниченная задача

1. Воспроизведите дефект отдельным тестом: очистите tenant-a key, одновременно отпустите 32 requests и покажите source reads, близкие к числу requests.
2. Внесите минимальную coordination-правку на key, сохранив cache-aside.
3. Докажите, что после исправления пять независимых bursts по 32 requests дают правильную v1 и `source_read≤1` каждый.
4. Добавьте regression checks warm hit, tenant-a/tenant-b isolation, cache failure и следующий burst после отказа.
5. Зафиксируйте process boundary и объясните, почему тест не доказывает поведение двух workers.

## Acceptance criteria

- [ ] До исправления defect test красный по amplification, а не только по latency.
- [ ] Один cold miss даёт `200` и ровно один source read.
- [ ] Двадцать warm hits не добавляют source reads.
- [ ] Пять bursts × 32 requests дают 100% корректных `200`; каждый burst — `source_read≤1` на key.
- [ ] Параллельные tenant-a/tenant-b requests используют разные keys/values; leakage `0`.
- [ ] Fault injection в cache adapter до `GET` приводит 32 requests к контролируемым `503` не позже 350 мс; source reads `0`.
- [ ] После восстановления следующий 32-request cold burst даёт корректные `200`, `source_read≤1` и завершается не позже 150 мс на закреплённом лабораторном host.
- [ ] Coordination state не оставляет зависших waiters после ошибки/cancellation.
- [ ] README опыта называет versions, workload, duration, counters и one-process boundary.

Числа — критерии локального Gate 0, не production performance target. Порог `≤150 мс` здесь относится только к recovery: kata проверяет correctness concurrent-miss burst и не наследует одноимённый project acceptance threshold. Если host не воспроизводит временные thresholds, сначала запишите отличие и согласуйте эквивалентные условия и границы измерения (`measurement envelope`); нельзя молча убрать correctness или source-read bound. Реальное выключение Redis/Docker можно проверить дополнительно, но его host-dependent время не является acceptance threshold.

## Non-goals

- готовый scaffold, пошаговая реализация или эталонный код;
- commit/invalidation race и read-your-writes;
- Redis lease, distributed lock, несколько workers/instances;
- load test PostgreSQL capacity, query tuning или Cache L4 migration;
- замена fail-closed на необоснованный database fallback.

## Постепенные подсказки

<details>
<summary>Подсказка 1 — что считать</summary>

Latency может случайно выглядеть хорошо. Добавьте счётчик фактических source reads на tenant key и проверяйте response tenant/version одновременно.

</details>

<details>
<summary>Подсказка 2 — где находится координация</summary>

Нужен один coordination object на cache key, а не один global lock на все tenants. Глобальная блокировка исправит amplification ценой ненужной связи независимых tenant.

</details>

<details>
<summary>Подсказка 3 — что проверить после ожидания</summary>

Task, получивший право продолжить после другого task, не знает, остался ли miss. Повторная проверка cache отличает будущего владельца загрузки (`leader`) от ожидающего запроса (`follower`).

</details>

<details>
<summary>Подсказка 4 — ошибка владельца</summary>

Используйте `async with lock` либо эквивалентный `acquire` с `release` в `finally`, чтобы обычный выход, exception или cancellation владельца освобождали lock. Проверьте, что следующий waiter может завершиться. Не сохраняйте навсегда незавершённый Future.

</details>

## Самопроверка

Почему один global lock не является хорошей минимальной правкой?

<details>
<summary>Ответ и объяснение</summary>

Он связывает независимые keys: miss tenant-a задерживает tenant-b. Требование ограничивает повторную работу одного key, поэтому coordination должна иметь тот же scope. Global lock может пройти один узкий тест, но создаёт ложную очередь.

</details>

Какой результат покажет, что lock лишь сериализовал stampede?

<details>
<summary>Ответ и объяснение</summary>

Все ответы будут корректны, параллельных SELECT не будет, но `source_read` останется 32. Это значит, что после ожидания отсутствует повторный cache lookup или follower всё ещё загружает source.

</details>

## Словарь и источники

- **Cold miss burst** — одновременно начавшаяся группа однотипных запросов (`population`) к отсутствующему key.
- **Per-key coordination** — синхронизация только запросов одного cache key.
- **Follower** — request, использующий результат владельца загрузки вместо нового source read.
- **Regression check** — проверка, которая падает при возвращении исходного amplification defect.

Источники: [Python `asyncio.Lock`](https://docs.python.org/3.14/library/asyncio-sync.html#lock), [Redis async client](https://redis.io/docs/latest/develop/clients/redis-py/async/), [Redis `SET`](https://redis.io/docs/latest/commands/set/) и [Gate 0](../../../../../../governance/work-packages/M1.8.13-application-caching-s15-slice.md#gate-0--b3-cache-store-и-применимая-b5-coordination-readiness).
