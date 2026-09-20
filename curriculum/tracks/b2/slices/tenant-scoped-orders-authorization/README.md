---
id: b2.index.tenant-scoped-orders-authorization
kind: index
title: Tenant-safe чтение Orders с проверенной identity
owner_track: b2
module: b2.module.identity-aware-boundaries
coverage:
  - target: b2.capability.integrate-identity-access-control
    role: reference
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

# Tenant-safe чтение Orders с проверенной identity

Клиент tenant A предъявляет корректно подписанный token и запрашивает `GET /orders/order-b`, где `order-b` принадлежит tenant B. Успешная проверка token отвечает только на вопрос «кто обращается к сервису и можно ли доверять этим утверждениям». Она не отвечает на другой вопрос: «разрешено ли этому субъекту читать именно этот Order».

Этот slice проводит проверенные `subject_id` и `tenant_id` через один Orders flow и размещает проверку доступа к объекту так, чтобы ни path, ни query, ни `X-Tenant-ID` не могли заменить доверенный tenant context. Результат — один проверяемый контракт: свой Order возвращается, чужой не раскрывается, отсутствие контекста не открывает доступ.

## Закреплённая техническая история

- endpoint: `GET /orders/{order_id}`;
- tenant A: subject `subject-a`, Order `order-a`;
- tenant B: Order `order-b`;
- bearer credential: локальный JWT, подписанный fixture issuer алгоритмом `RS256`;
- доверенные claims: `iss=https://issuer.test.local`, `aud=orders-api`, `sub`, `tenant_id`, `exp`, `nbf`;
- проверенный baseline: Python 3.14.6, FastAPI 0.141.1, Starlette 1.3.1, PyJWT 2.13.0, `cryptography` 50.0.0;
- доступ разрешён только при `order.tenant_id == identity_context.tenant_id`;
- без credentials или с невалидным token сервис возвращает `401 application/problem+json` и Bearer challenge;
- чужой и отсутствующий Order дают полностью одинаковый `404 application/problem+json` с `Cache-Control: no-store`;
- audit record фиксирует решение, но не token, Authorization header, claims dump или Order fields.

Полная запись решений и первичных источников находится в [Gate 0](../../../../../governance/work-packages/M1.8.9-identity-aware-boundaries-s05-slice.md#gate-0--a3-identitytrustsecurity-readiness-record). Материалы не требуют верить index: каждое version-sensitive утверждение сопровождается источником и проверяемым наблюдением.

## Маршрут

1. [Граница доверенного контекста и object authorization](learn/trusted-context-object-authorization-boundary.md) — различите authentication, передачу контекста и решение по конкретному Order.
2. [Interview: валидный token и чужой Order](interview/valid-token-cross-tenant-order.md) — пройдите от заданного правила к поиску обходных путей.
3. [Kata: заблокировать cross-tenant read](kata/block-cross-tenant-order-read.md) — самостоятельно соберите минимальный scaffold и закройте один bypass.
4. [Project: tenant-safe Orders read API](project-spec/tenant-safe-orders-read-api.md) — защитите placement решения несколькими путями и собранным HTTP evidence.

До kata полезно понимать фактическую [HTTP execution boundary](../evolvable-api-contracts/learn/http-contract-execution-boundary.md), [application boundary](../service-architecture-boundaries/learn/change-isolation-service-boundaries.md) и [выбор правдивой test boundary](../risk-based-service-verification/learn/truthful-test-boundaries.md). Эти темы здесь используются, но не преподаются повторно.

## Ожидаемый результат

После маршрута инженер умеет применить заданное правило уровня объекта, передать server-trusted identity context без зависимости от client-supplied tenant и самостоятельно разместить deny-by-default enforcement. Отдельными результатами служат positive/negative HTTP cases, наблюдение контекста после validation и threat/bypass matrix; один зелёный router test не подменяет их все.

Slice не обучает login, выдаче и rotation token, IAM/IdP infrastructure, криптографии, универсальному RBAC/ABAC, row-level security, rate/quota/SSRF controls или межсервисной policy migration. Он не подтверждает A3 proficiency, Identity L4 либо новое HTTP, Architecture и Verification coverage.

## Актуальность источников

Baseline проверен 2026-08-26. На эту дату FastAPI 0.141.1 и PyJWT 2.13.0 были актуальными релизами, а Starlette 1.6.0 уже новее закреплённой 1.3.1. Slice не зависит от внутренностей Starlette: при обновлении связки нужно повторить собранные ASGI/HTTP cases, особенно Bearer challenge, media type и равенство двух `404` responses.

Нормативная основа: [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519.html), [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725.html), [Bearer usage RFC 6750](https://www.rfc-editor.org/rfc/rfc6750.html), [HTTP semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html), [Problem Details RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html), [PyJWT API](https://pyjwt.readthedocs.io/en/stable/api.html), [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) и [OWASP API1:2023 BOLA](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/).
