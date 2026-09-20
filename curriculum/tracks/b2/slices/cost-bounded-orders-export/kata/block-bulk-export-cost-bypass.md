---
id: b2.kata.block-bulk-export-cost-bypass
kind: kata
title: Kata — block bulk-export cost bypass
owner_track: b2
module: b2.module.identity-aware-boundaries
coverage:
  - target: b2.level-outcome.enforce-api-security-abuse-controls-l1-apply-defined-controls
    role: practice
  - target: b2.level-outcome.enforce-api-security-abuse-controls-l1-apply-defined-controls
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

# Kata: block bulk-export cost bypass

## История

Ваш Orders service разрешает tenant экспортировать до 500 строк через `POST /orders/export`. После добавления выбора публичных полей проверка осталась прежней: handler смотрит только на `max_rows`. Запрос `500×5` теперь запускает 2500 CSV-cell writes, хотя принятый envelope допускает 2000.

Стартового scaffold нет. Создайте минимальную систему самостоятельно на закреплённом baseline: FastAPI/Pydantic, tenant-indexed fixture из 3000 Orders и синхронный CSV response. Identity validation можно представить готовым immutable `IdentityContext`; нельзя брать tenant из request.

## Ограниченная задача

1. Воспроизведите дефект: normal `400×4` и at-limit `500×4` проходят, `500×5` из полей разрешённого списка (`allowlist`) тоже ошибочно пересекает executor.
2. Введите минимальную server-owned оценку `max_rows × count(unique_allowed_fields)` и threshold `2000` после strict normalization, до executor.
3. Докажите, что bypass получает закреплённый cost-limit `422 application/problem+json`, а `export_execution_started` и `cells_serialized` не меняются.
4. Сохраните normal/at-limit CSV behavior и добавьте negative checks для duplicate, unknown, `customer_email` и extra `tenant_id`.
5. Явно настройте strict binding и добавьте один negative case, который до расчёта стоимости отклоняет опасное lax-преобразование `max_rows` (например, `true`, `"500"` или `500.0`), не превращая kata в обзор всех вариантов типов.

## Контракты

Allowlist: `id`, `status`, `total_cents`, `currency`, `created_at`. Body содержит только явно настроенные strict `max_rows: 1..3000` и non-empty `fields: 1..5`; duplicate и extra input запрещены. Полагаясь на Pydantic defaults, strict contract получить нельзя: lax binding может преобразовать числовую строку, целый `float` или `bool` в `int`. Over-cost problem имеет стабильные `type`, `title`, `status=422`, но не раскрывает token, body, values, threshold или counters.

Input-invalid response проверяйте через собранное ASGI/HTTP-приложение: `Content-Type` — `application/problem+json`, структура содержит только закреплённые безопасные поля, а исходное запрещённое или чувствительное значение отсутствует во всём response body. Дефолтный FastAPI `RequestValidationError` handler возвращает `application/json` и может перенести исходный `input` из `errors()`, поэтому для этого контракта требуется собственный безопасный mapper/handler; его готовая реализация в kata не предоставляется.

`cells_serialized` увеличивается на каждое записанное значение data row; CSV header в unit не входит. `export_execution_started` увеличивается ровно при входе в executor. Эти определения не меняйте ради зелёного теста.

## Acceptance criteria

- [ ] До исправления отдельный bypass test красный и показывает пересечение executor.
- [ ] После исправления normal `1600` и at-limit `2000` дают `200`, правильный header/row count и exact cells.
- [ ] Bypass `2500` даёт cost-limit `422`, work deltas равны нулю.
- [ ] Over-limit `501×4=2004` ведёт себя так же, как bypass.
- [ ] Duplicate/unknown/forbidden/extra input даёт input-invalid `422` до execution и без echo значений.
- [ ] Выбранный lax type variant отклоняется до cost calculation; ASGI response имеет `application/problem+json`, безопасную структуру и не содержит исходное значение.
- [ ] Normal request после 100 bypass requests снова даёт `200` и 1600 cells.
- [ ] Имена проверок или output различают подтверждение status и подтверждение reject-before-work.

## Non-goals

Не создавайте готовый production repository, distributed rate limiter, shared counter, callback URL, SSRF validation, background export, database optimization или универсальную cost formula. Не расширяйте kata до Abuse L2/L3: один исправленный bypass подтверждает только L1 practice/assessment.

## Подсказки

<details>
<summary>Подсказка 1 — где искать неполную модель</summary>

Составьте таблицу dimensions, которые меняют фактическую работу, и сравните её с тем, что проверяет старый limit. Для этого defect достаточно строк и публичных fields.

</details>

<details>
<summary>Подсказка 2 — порядок действий</summary>

Разделите binding, normalization, estimation и execution. Cost formula должна получать уже нормализованный request, но executor ещё не должен быть вызван.

</details>

<details>
<summary>Подсказка 3 — доказательство placement</summary>

Оборачивайте executor наблюдаемой точкой перехвата или подмены (`seam`) либо счётчиком. Проверка одного `response.status_code == 422` остаётся зелёной даже при serialize-then-reject defect.

</details>

## Самопроверка

Почему молчаливое удаление пятого поля — не эквивалентное исправление?

<details>
<summary>Ответ и объяснение</summary>

Оно меняет обещанный результат без явного отказа: клиент получает не тот export и не знает, что запрос был преобразован. Admission должен либо принять нормализованный request contract целиком, либо вернуть стабильную исправимую ошибку.

</details>

## Словарь и источники

- **Scaffold** — заранее предоставленная стартовая кодовая база; в этой kata его нет.
- **Regression check** — проверка, которая сначала воспроизводит defect, затем защищает исправленное поведение.
- **Work indicator** — наблюдаемый счётчик фактической работы за границей запуска export executor.
- **Allowlist** — закрытый список точных имён полей, разрешённых публичным export contract.
- **Seam** — наблюдаемая точка перехвата или подмены, через которую тест обнаруживает вызов executor.

Проверено 2026-08-28: [Gate 0](../../../../../../governance/work-packages/M1.8.11-operation-cost-admission-s14-slice.md#gate-0--threatcost-readiness-record), [OWASP API4:2023](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/), [FastAPI Request Body](https://fastapi.tiangolo.com/tutorial/body/), [Pydantic validators](https://docs.pydantic.dev/2.12/concepts/validators/) и [Python `csv`](https://docs.python.org/3.14/library/csv.html).
