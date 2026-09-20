---
id: b2.interview.valid-token-cross-tenant-order
kind: interview
title: Interview — валидный token и чужой Order
owner_track: b2
module: b2.module.identity-aware-boundaries
coverage:
  - target: b2.level-outcome.integrate-identity-access-control-l1-enforce-defined-rule
    role: probe
  - target: b2.level-outcome.integrate-identity-access-control-l2-propagate-context
    role: probe
  - target: b2.level-outcome.integrate-identity-access-control-l3-design-service-enforcement
    role: probe
status: accepted
updated: 2026-08-26
language: ru
last_verified: 2026-08-26
versions:
  python: 3.14.6
  fastapi: 0.141.1
  starlette: 1.3.1
  pyjwt: 2.13.0
  cryptography: 50.0.0
---

# Interview: валидный token и чужой Order

## История для кандидата

Orders service предоставляет `GET /orders/{order_id}`. Tenant A имеет subject `subject-a` и Order `order-a`; tenant B — Order `order-b`. Клиент tenant A предъявляет корректный RS256 JWT и запрашивает `order-b`.

FastAPI dependency проверяет fixture public key, только `RS256`, `iss=https://issuer.test.local`, `aud=orders-api`, `exp`, `nbf`, не предоставляет допуск рассинхронизации часов (`leeway=0`) и требует непустые `sub`/`tenant_id`. После проверки создаётся `IdentityContext(subject_id, tenant_id)`. Любой tenant в header/query/body недоверен. Доступ разрешён только если `order.tenant_id == context.tenant_id`.

Без валидного credential сервис возвращает закреплённый `401 application/problem+json` с Bearer challenge. Чужой и отсутствующий Order дают полностью одинаковый `404 application/problem+json`, `Cache-Control: no-store` и body без object/tenant fields. Audit фиксирует решение, но не token, claims dump или Order fields.

Задача кандидата — не выбрать другой IAM stack, а показать, как заданный контракт проходит путь от применения правила до самостоятельного design enforcement.

## Вопросы

### 1. Что доказал валидный token и чего он не доказал?

<details>
<summary>Ориентир сильного ответа</summary>

Он доказал, что token прошёл выбранную проверку происхождения, назначения и времени, поэтому сервис может построить trusted context. Он не доказал право на `order-b`: object authorization требует отдельного отношения между trusted tenant и owner tenant ресурса. Формула «authenticated значит authorized» выдаёт broken object-level authorization.

</details>

### 2. Примените заданное правило к `subject-a/tenant-a → order-b/tenant-b`.

<details>
<summary>Ориентир сильного ответа</summary>

Сравнение не совпадает, поэтому decision — deny. Наружу возвращается закреплённый `404` без полей Order; внутри audit допустим coarse reason `tenant_mismatch`. Кандидат не меняет контракт на `403` и не начинает обсуждать роли, которых в истории нет.

</details>

### 3. Где внешние claims становятся доверенным контекстом?

<details>
<summary>Ориентир сильного ответа</summary>

После единственного validator, который получил credential из FastAPI security dependency и успешно проверил signature, жёстко заданный algorithm, issuer, audience, required claims, `exp` и `nbf`. Только затем создаётся минимальный immutable `IdentityContext`. Декодированный без проверки payload, `X-Tenant-ID` или произвольный claims dictionary не пересекают trust boundary.

</details>

### 4. Как передать context через application flow и не связать правило только с router?

<details>
<summary>Ориентир сильного ответа</summary>

Router явно передаёт `IdentityContext` и недоверенный `order_id` в application operation. Operation получает Order через port, проверяет owner tenant до формирования DTO и возвращает typed allowed/not-found result. Так прямой вызов operation и второй delivery adapter используют то же правило. Framework dependency отвечает за authentication; operation — за object relation.

</details>

### 5. Follow-up: persistence уже делает `WHERE id=? AND tenant_id=?`. Нужна ли ещё проверка?

<details>
<summary>Ориентир сильного ответа</summary>

Tenant-scoped lookup полезен и уменьшает шанс загрузить чужие данные, но application invariant должен остаться явным и проверяемым. Новый adapter или ошибочный query не должен неявно снять authorization. Допустим port `find_visible_order(order_id, tenant_id)`, если его контракт прямо выражает authorization relation и все adapters проходят contract tests; это design choice, а не повод считать любой найденный объект разрешённым.

</details>

### 6. Назовите обходные пути и проверку для каждого.

<details>
<summary>Ориентир сильного ответа</summary>

Минимум: доверие `X-Tenant-ID`/query tenant — forged-context HTTP case; проверка только router — прямой component call operation; DTO или debug log до authorization — assertion об отсутствии чужих fields в response/audit; fail-open при пустом context — negative component case; второй route/adapter — threat matrix и contract test общей operation. Сильный ответ связывает угрозу с наблюдением, а не перечисляет security-термины.

</details>

### 7. Как доказать отсутствие existence leakage?

<details>
<summary>Ориентир сильного ответа</summary>

Запустить собранное приложение с тем же валидным token для `order-b` и `order-missing`; сравнить status, media type, cache header и body на полное равенство. Одновременно component/audit evidence различает внутренние причины. Проверка только одинакового status с разными body недостаточна.

</details>

### 8. Что должно быть в audit и чего там быть не должно?

<details>
<summary>Ориентир сильного ответа</summary>

Нужны request/correlation ID, trusted subject/tenant, action, resource type/ID, allow/deny, coarse reason и итоговый status. Нельзя писать bearer token, Authorization header, claims dump, keys, credentials, response body или Order fields. Для authentication failure нет trusted subject/tenant; запись содержит request ID, coarse missing/invalid и `401`.

</details>

### 9. Какие разные evidence подтверждают L1, L2 и L3?

<details>
<summary>Ориентир сильного ответа</summary>

L1 — positive/negative cases заданного `tenant matches owner` rule. L2 — наблюдение, что после validation context содержит только trusted `subject-a/tenant-a`, forged request tenant его не меняет и audit сохраняет trusted значения. L3 — обоснованное placement во всех путях, threat/bypass matrix, fail-closed behavior и полное HTTP evidence без leakage. Один end-to-end test может участвовать в нескольких доказательствах, но не делает их неразличимыми.

</details>

### 10. Когда нужно остановиться и не обещать больше?

<details>
<summary>Ориентир сильного ответа</summary>

Когда задача требует key rotation/JWKS, IdP operations, cross-service delegation, универсальный policy engine, row-level security или rate/quota/SSRF controls. Это отдельные trust boundaries и capabilities. Один Orders read path не доказывает Identity L4 и не подтверждает A3 proficiency.

</details>

## Rubric для интервьюера

| Уровень наблюдения | Признаки рассуждения |
|---|---|
| Не подтверждает L1 | Считает валидный token достаточным; доверяет tenant из request; не формулирует отношение subject/resource; допускает выдачу чужих полей в error/log. |
| L1 — применяет правило | Правильно различает `200`, `401`, одинаковый `404`; называет positive/negative cases и не меняет заданный contract. |
| L2 — проводит context | Показывает единственную trust boundary, минимальный immutable context, явную передачу в operation и forged-context evidence; audit использует trusted tenant. |
| L3 — проектирует enforcement | Находит router/application/adapter bypasses, выбирает placement до DTO, сохраняет deny-by-default, разводит internal reason и wire disclosure, связывает угрозы с component и ASGI checks. |

Сильный кандидат объясняет причинность и границы обещаний. Количество упоминаний JWT, OAuth, RBAC или ABAC не повышает оценку. `probe` выявляет рассуждение, но само интервью не является evidence самостоятельной реализации.

## Правдоподобные, но слабые ответы

- «JWT валиден, значит endpoint можно выполнить» — путает authentication с resource permission.
- «Сравним Order с `X-Tenant-ID`» — доверяет клиенту источник полномочия.
- «Dependency на router всё закроет» — не рассматривает прямой application path или второй adapter.
- «Вернём `403` для чужого и `404` для missing» — нарушает закреплённую leakage semantics.
- «Залогируем token для расследования» — создаёт второй канал компрометации credential.
- «Есть один зелёный unit test» — не доказывает wiring и wire contract.

## Источники и актуальность

Проверено 2026-08-26 по [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725.html), [RFC 6750](https://www.rfc-editor.org/rfc/rfc6750.html), [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html), [PyJWT API](https://pyjwt.readthedocs.io/en/stable/api.html), [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), [OWASP BOLA](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/), [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) и [OWASP Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html). Starlette 1.6.0 новее закреплённой 1.3.1; при upgrade повторяется ASGI evidence, а не переносится уверенность по номеру версии.
