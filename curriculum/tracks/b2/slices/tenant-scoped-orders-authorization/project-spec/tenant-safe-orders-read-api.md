---
id: b2.project-spec.tenant-safe-orders-read-api
kind: project-spec
title: Project — tenant-safe Orders read API
owner_track: b2
module: b2.module.identity-aware-boundaries
coverage:
  - target: b2.level-outcome.integrate-identity-access-control-l2-propagate-context
    role: integrate
  - target: b2.level-outcome.integrate-identity-access-control-l2-propagate-context
    role: assess
  - target: b2.level-outcome.integrate-identity-access-control-l3-design-service-enforcement
    role: integrate
  - target: b2.level-outcome.integrate-identity-access-control-l3-design-service-enforcement
    role: assess
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

# Project: tenant-safe Orders read API

## Рабочая ситуация

Orders service открывает один endpoint `GET /orders/{order_id}` двум tenant. Успешная authentication сейчас позволяет загрузить Order по ID без проверки owner tenant. В результате валидный пользователь tenant A может прочитать `order-b` tenant B, а добавление фильтра только в один router оставит обход через прямой application call или будущий delivery adapter.

Соберите самостоятельный сервисный milestone, в котором server-trusted identity context проходит от bearer validation до object-level decision, все заявленные пути дают deny by default, а HTTP и audit contracts не раскрывают чужой Order. Стартового repository и ImplementationReference нет; выбор структуры кода и ports принадлежит участнику и защищается короткой записью решения.

## Закреплённый substrate и fixtures

- Python 3.14.6, FastAPI 0.141.1, Starlette 1.3.1, PyJWT 2.13.0, `cryptography` 50.0.0;
- локальная RSA fixture pair; private key существует только у test issuer, Orders service получает public key;
- `algorithms=["RS256"]`, `issuer=https://issuer.test.local`, `audience=orders-api`, `leeway=0`;
- обязательные `iss`, `aud`, `sub`, `tenant_id`, `exp`, `nbf`; `sub`/`tenant_id` — непустые строки;
- tenant A: `subject-a`, `order-a`; tenant B: `order-b`; отдельный `order-missing` отсутствует;
- token issuance UI, JWKS/discovery, rotation/revocation, IdP и production database вне milestone.

JWT является bearer credential: владение строкой достаточно для предъявления, поэтому token нельзя помещать в logs или project artifacts. Claims становятся trusted только после полной validation; route/header/query/body tenant identifiers не заменяют их.

## Внешний contract

Allowed `A→order-a` возвращает `200 application/json` и только публичные поля `order-a`.

Missing credential возвращает `401` с `WWW-Authenticate: Bearer`. Предъявленный malformed/invalid token получает `401` и Bearer challenge с `error="invalid_token"`. Оба имеют `Content-Type: application/problem+json` и body:

```json
{"type":"https://orders.example/problems/authentication-required","title":"Authentication required","status":401}
```

Cross-tenant и missing Order получают полностью одинаковые status, headers и body:

```http
HTTP/1.1 404 Not Found
Cache-Control: no-store
Content-Type: application/problem+json

{"type":"https://orders.example/problems/order-not-found","title":"Order not found","status":404}
```

Это локальная existence-leakage policy: внешний клиент не различает «нет объекта» и «объект есть, но принадлежит другому tenant». Internal audit может различать причины при ограниченном доступе к журналу.

## Обязательные invariants

1. **Trusted context:** только validator создаёт `IdentityContext(subject_id, tenant_id)` после всех проверок; token и claims dictionary не проходят в application layer.
2. **Object rule:** `orders.read` разрешён только при `order.tenant_id == context.tenant_id`.
3. **Deny by default:** пустой/неполный context, неизвестное отношение и любой неявный path дают deny.
4. **Disclosure:** чужие Order fields, credential и security internals отсутствуют в response, log и audit.
5. **Path consistency:** HTTP route, прямой application call и заявленный альтернативный adapter не расходятся в object decision.

## Milestones и наблюдаемые результаты

### 1. Trust boundary

Опишите, где извлекается credential, где проверяются key/algorithm/issuer/audience/time/required claims и где появляется immutable context. Наблюдаемый результат — component evidence, которое показывает trusted `subject-a/tenant-a` для valid fixture и отсутствие application call для missing/malformed/expired/wrong-audience token.

Review не принимает простой `jwt.decode(token, key)` без жёсткого algorithm и required claims или построение context до проверки.

### 2. Resource enforcement

Разместите заданное правило так, чтобы оно выполнялось до Order DTO и не зависело только от FastAPI router. Наблюдаемый результат — одинаковый decision для HTTP route, прямого operation call и минимум одного дополнительного заявленного bypass path: второго adapter либо storage adapter, который вернул Order другого tenant вопреки ожиданию.

Review принимает разные структуры ports/adapters, если application-visible invariant остаётся fail-closed и проверяемым. Tenant-scoped storage lookup допустим как defence in depth, но не как недоказанное предположение «найденный объект уже разрешён».

### 3. Disclosure и audit

Сформируйте единый error mapper и структурированный audit sink. Запись authorization decision содержит `request_id`, trusted `subject_id`/`tenant_id`, `action=orders.read`, `resource_type=order`, requested `resource_id`, `decision`, coarse `reason` и `http_status`. Authentication failure содержит только request ID, coarse `missing|invalid` и `401`.

Наблюдаемый результат — exact-response assertions и negative assertions: ни token, ни Authorization header, ни claims dump, ни keys, ни response body, ни Order fields не появляются в audit/log capture.

### 4. Security evidence и защита решения

Соберите component и ASGI/HTTP evidence, заполните threat/bypass matrix и короткий decision record. Наблюдаемый результат — reviewer может связать каждый invariant с конкретным test/output и объяснить, какая граница была реально выполнена.

## Обязательный evidence envelope

Для каждой строки сохраните test name, вход, context после validation, точный HTTP result, audit observation и negative disclosure assertions.

| Population | Token/claims fixture и request | Trusted context | HTTP observation | Audit observation |
|---|---|---|---|---|
| allowed | valid A; `/orders/order-a` | `subject-a/tenant-a` | `200`; только public fields `order-a` | allow/allowed |
| unauthenticated | no token; отдельно invalid signature или expired | отсутствует | закреплённый `401`; корректный Bearer challenge | authentication failure без claims/token |
| cross-tenant | valid A; `/orders/order-b` | `subject-a/tenant-a` | закреплённый `404`; нет Order fields | deny/tenant_mismatch |
| forged-context | valid A; `/orders/order-b?tenant_id=tenant-b`, `X-Tenant-ID: tenant-b` | всё ещё `subject-a/tenant-a` | тот же `404` | deny с trusted tenant A |
| missing-object | valid A; `/orders/order-missing` | `subject-a/tenant-a` | byte-equivalent cross-tenant `404` | deny/not_found |

ASGI/HTTP comparison для последних двух denial populations включает status, media type, `Cache-Control` и точный body. Component evidence отдельно доказывает, что внутренние причины и decisions сформированы корректно.

## Threat/bypass matrix

Участник обязан дополнить таблицу ссылкой на свои tests или outputs.

| Threat или bypass | Почему возможен | Требуемое control | Evidence |
|---|---|---|---|
| Подмена object ID | клиент управляет path | owner-tenant rule для каждого объекта | cross-tenant case |
| Подмена tenant header/query | клиент управляет request metadata | context только из validated claims | forged-context case |
| Проверка только router | operation вызывается другим adapter/test | application-visible enforcement | direct-call case |
| Ошибочный storage adapter | фильтр tenant потерян при изменении query | fail-closed check до DTO | malicious/faulty adapter case |
| DTO/log до decision | чужие поля становятся side effect | decision перед mapping/logging | disclosure assertions |
| Пустой context | wiring/claim regression | explicit deny, не default tenant | missing-context component case |
| Разные not-found responses | статус совпадает, body/header различается | единый error mapper | exact equality case |

## Короткий decision record

Запишите не больше двух страниц:

- контекст и четыре invariants;
- выбранные trust и enforcement boundaries;
- почему client tenant не является authority;
- почему cross-tenant и missing используют одинаковый `404`;
- какие alternative placements рассмотрены;
- какие проверки опровергнут решение при будущем изменении;
- что намеренно осталось вне scope.

Не вставляйте готовую реализацию в record. Его цель — сделать основания и границы решения проверяемыми.

## Review criteria

- [ ] Один substrate и exact baseline совпадают с этой specification.
- [ ] Validator фиксирует key/RS256/issuer/audience/time/required claims и fail-closed behavior.
- [ ] Context не зависит от route/header/query/body tenant.
- [ ] Object rule выполняется до DTO по всем заявленным paths.
- [ ] Пять populations имеют отдельное deterministic evidence.
- [ ] Cross-tenant и missing wire responses полностью равны.
- [ ] Audit содержит достаточный decision context и не содержит secrets/чужих fields.
- [ ] Threat matrix связывает каждый bypass с test/output.
- [ ] Decision record защищает placement и раскрывает отвергнутые варианты.
- [ ] Нет готового IdP, policy engine, RLS lesson, S14 controls или Identity L4 claim.

## Non-goals

Не реализуйте login/token issuance/refresh/revocation, key discovery/rotation, IAM governance, service-to-service identity, delegation, cross-service policy migration, универсальный RBAC/ABAC engine, row-level security, quota/rate/cost/SSRF controls, production rollout или эталонный repository. Это один сервис, одна read operation и несколько путей к одному object decision.

## Источники и актуальность

Проверено 2026-08-26: [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519.html), [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725.html), [RFC 6750](https://www.rfc-editor.org/rfc/rfc6750.html), [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html), [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html), [PyJWT API](https://pyjwt.readthedocs.io/en/stable/api.html), [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), [Starlette TestClient](https://www.starlette.io/testclient/), [OWASP BOLA](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/), [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) и [OWASP Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html).

Starlette 1.6.0 новее закреплённой 1.3.1. При обновлении baseline повторите component и assembled ASGI/HTTP evidence; совместимость нельзя вывести только из release number.
