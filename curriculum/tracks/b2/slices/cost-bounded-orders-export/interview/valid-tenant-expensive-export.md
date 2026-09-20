---
id: b2.interview.valid-tenant-expensive-export
kind: interview
title: Interview — valid tenant, expensive Orders export
owner_track: b2
module: b2.module.identity-aware-boundaries
coverage:
  - target: b2.level-outcome.enforce-api-security-abuse-controls-l1-apply-defined-controls
    role: probe
  - target: b2.level-outcome.enforce-api-security-abuse-controls-l2-protect-typical-endpoint
    role: probe
  - target: b2.level-outcome.enforce-api-security-abuse-controls-l3-design-service-abuse-boundary
    role: probe
status: accepted
updated: 2026-08-30
language: ru
last_verified: 2026-08-28
versions:
  python: 3.14.0
  fastapi: 0.137.1
  starlette: 1.3.1
  pydantic: 2.12.5
---

# Interview: valid tenant, expensive Orders export

## Кейс

Orders API предоставляет `POST /orders/export`. Trusted `IdentityContext` уже создан из проверенного token; tenant из body, query или headers полномочий не даёт. Request содержит `max_rows` и `fields`. Публичный разрешённый список полей (`allowlist`): `id`, `status`, `total_cents`, `currency`, `created_at`; fixture содержит 3000 Orders tenant.

Сервис ограничивает `max_rows <= 500`. Клиент обнаружил, что `500` строк с пятью полями создают больше CPU/memory/response work, чем обычные `400` строк с четырьмя. Нужно защитить стоимость одной операции, не проектируя distributed quota и не добавляя callback URL.

## Основной вопрос

Спроектируйте границу admission: какие предположения проверите, какую server-owned cost unit выберете, где разместите решение и какими наблюдениями докажете, что допустимый export сохранён, а обход не запускает дорогую работу?

<details>
<summary>Ориентиры сильного рассуждения</summary>

Сильный ответ сначала отделяет подтверждённое от неизвестного. Для закреплённого substrate достаточно `estimated_cells = max_rows × unique_allowed_fields`, threshold `2000`, normal `400×4`, at-limit `500×4`, over-limit `501×4` и bypass `500×5`. Binding строгий: неизвестные, чувствительные, duplicate/alias/type variants отклоняются; tenant остаётся server-trusted.

Решение размещается после binding/normalization, но до export executor. Доказательство включает не только `422`, а нулевые delta `export_execution_started` и `cells_serialized`. Normal/at-limit проверяют CSV header, строки и tenant scope. Recovery — normal request после 100 bypass — снова даёт `200` и 1600 cells.

Ответ также должен назвать false-positive границу консервативной оценки, audit disclosure limits и честно отделить per-operation ceiling от rate/quota и SSRF.

</details>

## Уточнения от L1 к L3

### 1. Какой минимальный дефект и regression test соответствуют L1?

<details>
<summary>Ответ и объяснение</summary>

Дефект — row-only check пропускает `500×5=2500`. Минимальная правка считает нормализованные cells и отклоняет `>2000` до executor. Regression test сравнивает normal/at-limit с одним bypass и проверяет нулевые work counters; готовая общесервисная quota policy не нужна.

</details>

### 2. Что делать с duplicate, `customer_email`, `debug` и extra `tenant_id`?

<details>
<summary>Ответ и объяснение</summary>

Не нормализовать их молча. Duplicate делает request contract двусмысленным, неизвестные и чувствительные поля расширяют exposure, а client tenant пересекает границу доверия. Все отклоняются strict binding до cost/execution с безопасным input-invalid problem; значения request в error/audit не копируются.

</details>

### 3. Почему threshold не следует возвращать в error body?

<details>
<summary>Ответ и объяснение</summary>

Клиенту достаточно стабильного типа и исправимого действия — уменьшить export. Точная внутренняя telemetry облегчает probing и связывает публичный error contract с меняемой моделью. Документация может описывать публичные bounds, но response не обязан раскрывать runtime weights или counters.

</details>

### 4. Заполните applicability matrix Abuse L2.

<details>
<summary>Ответ и объяснение</summary>

Request/cost — применимо: составная оценка и bypass checks. Field exposure — применимо: allowlist и forbidden-field negative tests. Quota/rate — не реализуется: ceiling одной операции не ограничивает сумму запросов, это residual risk. Untrusted target — contract не имеет target и отклоняет extra keys; это не SSRF evidence, будущий callback требует отдельного package.

</details>

### 5. Что изменит реальная database или вычисляемое поле?

<details>
<summary>Ответ и объяснение</summary>

Нужно повторить Gate 0. Если основная работа — scan, join, compression или remote I/O, cell count может перестать быть связанным индикатором. Следует найти дешёвую предоперационную оценку и новый observable work indicator; если это невозможно, честно остановить authoring/rollout, а не оставить post-factum limit.

</details>

### 6. Почему 100 rejected requests не являются quota test?

<details>
<summary>Ответ и объяснение</summary>

Они проверяют, что отказы не оставляют учитываемой работы и normal request восстанавливается в локальном процессе. Здесь нет окна времени, shared counter или нескольких workers. Поэтому опыт не доказывает ограничение частоты или aggregate consumption.

</details>

## Rubric для интервьюера

- **L1:** применяет заданные strict bounds, различает invalid и over-cost input, воспроизводит один bypass и проверяет reject-before-work.
- **L2:** завершает четыре строки applicability matrix с controls/evidence или честным `not applicable`; связывает field exposure и disclosure с tests.
- **L3:** превращает неизвестную стоимость в проверяемую модель, защищает placement, legitimate use и tenant isolation, называет false positives, measurement envelope и stop conditions.

Слабые сигналы: «поставим 429», «увеличим timeout», «добавим rate limiter» без модели одной операции; доверие client `cost`; проверка только status; заявление SSRF protection из-за отсутствия callback; точные production claims по локальным milliseconds.

## Словарь и источники

- **Cost unit** — server-defined единица предварительной оценки; здесь CSV-ячейка.
- **Applicability matrix** — разбор каждой требуемой категории как applicable control либо обоснованной границы.
- **Reject-before-work** — отказ без входа в executor и без сериализованных cells.
- **Stop condition** — условие, при котором выбранная модель перестаёт позволять честное продолжение.

Baseline и источники проверены 2026-08-28: [Gate 0](../../../../../../governance/work-packages/M1.8.11-operation-cost-admission-s14-slice.md#gate-0--threatcost-readiness-record), [OWASP API4:2023](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/), [Pydantic configuration](https://docs.pydantic.dev/2.12/api/config/), [RFC 9110 §15.5.21](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.21) и [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html).
