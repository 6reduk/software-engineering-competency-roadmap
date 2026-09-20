---
id: b2.project-spec.cost-bounded-orders-export-api
kind: project-spec
title: Project — cost-bounded Orders export API
owner_track: b2
module: b2.module.identity-aware-boundaries
coverage:
  - target: b2.level-outcome.enforce-api-security-abuse-controls-l2-protect-typical-endpoint
    role: integrate
  - target: b2.level-outcome.enforce-api-security-abuse-controls-l2-protect-typical-endpoint
    role: assess
  - target: b2.level-outcome.enforce-api-security-abuse-controls-l3-design-service-abuse-boundary
    role: integrate
  - target: b2.level-outcome.enforce-api-security-abuse-controls-l3-design-service-abuse-boundary
    role: assess
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

# Project: cost-bounded Orders export API

## Рабочая ситуация

Orders service добавляет синхронный CSV export для двух tenant. Trusted identity и object scope уже решены в prerequisite [«Trusted context и object-authorization boundary»](../../tenant-scoped-orders-authorization/learn/trusted-context-object-authorization-boundary.md), но валидный tenant способен усилить работу одной операции через `max_rows` и ширину `fields`. Row-only limit пропускает `500×5`, а поздний response-size check срабатывает после сериализации.

Выполните самостоятельный milestone: спроектируйте, реализуйте и защитите server-owned admission одной операции до export executor. Стартового repository, готовой реализации и ImplementationReference нет. Выбор структуры кода принадлежит участнику; спецификация закрепляет только contract, evidence и границы.

## Substrate и внешний contract

- CPython 3.14.0, FastAPI 0.137.1, Starlette 1.3.1, Pydantic 2.12.5;
- tenant-indexed deterministic fixture для двух tenant: второй tenant нужен для проверки isolation, а минимум 3000 Orders на исследуемый tenant обеспечивает воспроизводимую выборку для заявленных populations и boundary cases;
- `POST /orders/export`, strict JSON body `max_rows` и `fields`;
- публичный разрешённый список полей (`allowlist`): `id`, `status`, `total_cents`, `currency`, `created_at`;
- чувствительные `customer_email`, `payment_token`, неизвестные, duplicates, aliases, extra keys и client tenant отвергаются;
- admitted request возвращает `200 text/csv`; cost-limit и invalid input — два стабильных `422 application/problem+json` problem types;
- client не задаёт cost, weights или tenant identity.

Единица стоимости — data CSV-cell, формула `estimated_cells = max_rows × count(unique_allowed_fields)`, threshold `2000`. Оценка выполняется после strict normalization и до `export_execution_started`. Это лабораторная модель сериализации, не обещание стоимости SQL или production capacity.

## Invariants

1. **Server-owned cost:** только нормализованная formula сервиса принимает решение.
2. **Reject-before-work:** over-limit и bypass не меняют `export_execution_started` и `cells_serialized`.
3. **Legitimate use:** normal и at-limit дают корректный tenant-scoped CSV.
4. **Tenant/disclosure:** response и audit не раскрывают чужие Orders, credentials, forbidden values или внутреннюю cost telemetry.
5. **Bounded claim:** ceiling одной операции не называется quota, capacity guarantee или SSRF control.

## Milestones и наблюдаемые результаты

### 1. Contract и trust boundary

Зафиксируйте явно настроенную strict model, allowlist, error types и источник `IdentityContext`. Pydantic defaults работают в lax-режиме и могут преобразовать числовую строку, целый `float` или `bool` в `int`; строгий контракт должен отвергать эти type variants до cost calculation. Наблюдаемый результат — schema/ASGI negative cases показывают, что body/header/query не задают tenant, а invalid/unknown/forbidden input не вызывает application export.

Закреплённый безопасный input-invalid response требует собственного mapper/`RequestValidationError` handler: дефолт FastAPI возвращает `application/json`, а `errors()` может содержать исходное значение в `input`. Проверка собранного ASGI/HTTP-приложения должна подтвердить `application/problem+json`, безопасную структуру Problem Details и отсутствие исходного forbidden/sensitive value во всём body; спецификация не задаёт готовую реализацию handler.

### 2. Cost model и placement

Запишите cost/threat matrix, нормализуйте request и выполните admission до executor. Наблюдаемый результат — raw counters связывают estimate с cells normal/at-limit и показывают нулевую работу over/bypass. Status-only test недостаточен.

### 3. Applicability matrix Abuse L2

Заполните все четыре категории таблицы ниже ссылками на свои test names или outputs. `not applicable` допустимо только вместе с boundary и residual risk. Если появляется callback, shared counter или необходимость distributed coordination, остановите milestone и запросите новый readiness decision.

### 4. Adversarial envelope и recovery

Запустите одинаковые populations и сохраните вход, normalized form, estimate, HTTP result, executor/cell deltas, CSV assertions и audit assertions. После серии bypass requests подтвердите normal outcome; не выдавайте latency локального измерительного стенда (`harness`) за production SLO. Recovery в этом задании означает отсутствие накопленного эффекта отклонённых запросов и сохранность следующей допустимой операции; это не восстановление уже израсходованных ресурсов и не evidence quota/rate control.

### 5. Decision record

Не более двух страниц: контекст, invariants, модель и placement; rejected alternatives; false-positive trade-off; что сломает формулу; stop conditions и триггеры перекалибровки. Код решения в record не вставляется.

## Failure/measurement envelope

Один процесс, fixture 3000 Orders, по 20 последовательных ASGI requests для первых четырёх populations; recovery — normal сразу после 100 bypass requests. Measurement point: client-side request duration и server-side counters. Зависимостей и concurrency в baseline нет.

| Population | Request и estimate | Acceptance |
|---|---|---|
| legitimate/normal | `400 × 4 = 1600` | `200`; 400 data rows, exact header/tenant scope, 1600 cells, executor +1 |
| at-limit | `500 × 4 = 2000` | `200`; 500 rows, 2000 cells, executor +1 |
| over-limit | `501 × 4 = 2004` | cost-limit `422`; executor/cells delta `0` |
| shape-bypass | `500 × 5 = 2500` | тот же cost-limit `422`; executor/cells delta `0` |
| recovery | normal после 100 bypass | `200`, 1600 cells; rejected requests суммарно дали zero work delta |

Локальный Gate 0 ориентир: median 2.969/3.225/2.639/2.592 ms и recovery 4.268 ms. Эти числа диагностические. Acceptance не требует повторить milliseconds, но требует exact outcomes/counters в том же workload.

## Threat/cost matrix

| Path | Cost/exposure consequence | Control | Required evidence |
|---|---|---|---|
| `max_rows` растёт | больше rows/cells | strict range + composite estimate | over-limit case |
| добавлено пятое allowed field | row-only bypass, шире CSV | field count в cost | shape-bypass case |
| duplicate/alias/type variant, включая `true`, `"500"` или `500.0` для `max_rows` | неоднозначная normalization или lax-преобразование до cost | явно настроенные strict types, exact names, duplicates forbidden | schema/ASGI input-invalid cases до cost calculation |
| unknown/sensitive field | disclosure и новая работа | fixed allowlist | negative response/audit assertions |
| client `tenant_id` | cross-tenant selector | identity только из trusted `IdentityContext` prerequisite, extra forbidden | forged-context case |
| serialize-then-reject | потраченная работа скрыта status | admission до executor | zero counters |

## Applicability matrix

| Категория | Диспозиция | Evidence | Residual risk |
|---|---|---|---|
| Request/cost bounds | Applicable: composite cost и threshold 2000 | пять populations, estimate/counter correlation | SQL/bytes/compression и aggregate requests не смоделированы |
| Field exposure | Applicable: allowlist и strict binding | sensitive/unknown/extra negative cases без echo | CSV formula interpretation и DLP вне scope |
| Quota/rate | `not applicable` как реализованный control | record явно отличает operation ceiling от time window/shared counter | множество допустимых requests может перегрузить сервис |
| Untrusted target | `not applicable`: target отсутствует, extra keys forbidden | contract/OpenAPI и negative extra-target case | будущий callback требует отдельной SSRF boundary |

## Audit/error assertions

Audit разрешает `request_id`, trusted `tenant_id`, `action`, `decision`, coarse `reason`, normalized field count и status. Запретите token, Authorization header, полный body, values, exported rows, forbidden field value и internal weights. Problem Details содержит стабильные `type`, `title`, `status`; wire status совпадает с `status` member. Для input-invalid ASGI case дополнительно проверьте `Content-Type: application/problem+json`, разрешённую безопасную структуру и отсутствие исходного forbidden/sensitive value во всём response body.

## Альтернативы, которые нужно рассмотреть

- row-only и response-size limits;
- post-factum timeout;
- молчаливое усечение fields/rows;
- фактический row count перед decision;
- отдельная дешёвая metadata estimate;
- rate limiter как ошибочная замена per-operation cost.

Оцените их по placement, false positives, наблюдаемости, disclosure и применимости к закреплённому substrate. Универсально правильного production выбора спецификация не задаёт.

## Review criteria

- [ ] Exact baseline и contract воспроизводимы одной документированной командой.
- [ ] Все пять populations имеют raw evidence и одинаковые определения counters.
- [ ] Allowed CSV корректен и tenant-scoped; rejected paths имеют zero work delta.
- [ ] Unknown, duplicate, sensitive, forged tenant и lax type-variant inputs отклоняются до cost/export.
- [ ] Input-invalid ASGI response имеет `application/problem+json`, безопасную структуру и не содержит исходное forbidden/sensitive value.
- [ ] Applicability matrix завершена, а L2 evidence отделено от L3 design defense.
- [ ] Decision record объясняет formula, placement, false positives, alternatives и stop conditions.
- [ ] Audit/error negative assertions проверяют отсутствие disclosure.
- [ ] Recovery наблюдается после снятия adversarial workload.
- [ ] Нет callback, SSRF implementation, distributed quota, background export или готового решения.

## Вопросы защиты

Какое наблюдение опровергнет выбранную cost unit?

<details>
<summary>Ориентиры ответа</summary>

Профиль, где одинаковое число cells даёт существенно разную учитываемую работу из-за scan, больших строк, вычисляемых полей, compression или remote I/O. Тогда нужен новый work indicator и повторный Gate 0, а не только другой threshold.

</details>

Почему проект может заявлять L2/L3, а kata — только L1?

<details>
<summary>Ориентиры ответа</summary>

Проект завершает applicability matrix, сравнивает пять populations, защищает multi-tenant/adversarial boundary, legitimate use, disclosure, recovery и design alternatives. Kata исправляет один заданный bypass по заданной модели; это применение control, не самостоятельный endpoint design.

</details>

## Non-goals, словарь и источники

Не реализуйте database tuning, streaming/file storage, distributed quota/rate, global fairness, callback/SSRF, background workflow, JWT lesson, platform rollout, L4 policy или ImplementationReference.

- **Milestone** — законченный инженерный этап с наблюдаемым результатом.
- **Cost/threat matrix** — связь управляемой формы request с работой, control и проверкой.
- **Decision record** — краткая запись выбора, альтернатив, последствий и triggers пересмотра.
- **Allowlist** — закрытый список точных имён полей, разрешённых публичным export contract.
- **Harness** — измерительный стенд с закреплёнными fixture, workload, точками измерения и evidence.
- **Recovery** — отсутствие накопленного эффекта отклонённых запросов и сохранность следующей допустимой операции; не восстановление израсходованных ресурсов и не quota/rate evidence.

Проверено 2026-08-28: [Gate 0](../../../../../../governance/work-packages/M1.8.11-operation-cost-admission-s14-slice.md#gate-0--threatcost-readiness-record), [OWASP API4:2023](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/), [FastAPI request body](https://fastapi.tiangolo.com/tutorial/body/), [FastAPI error handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/), [Pydantic configuration](https://docs.pydantic.dev/2.12/api/config/), [Python `csv`](https://docs.python.org/3.14/library/csv.html), [RFC 9110 §15.5.21](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.21) и [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html). Закреплённый локальный baseline отстаёт от stable CPython 3.14.7, FastAPI 0.141.1, Starlette 1.6.0 и Pydantic 2.13.4; upgrade требует повторить весь evidence envelope.
