---
id: b2.kata.block-cross-tenant-order-read
kind: kata
title: Kata — заблокировать cross-tenant чтение Order
owner_track: b2
module: b2.module.identity-aware-boundaries
coverage:
  - target: b2.level-outcome.integrate-identity-access-control-l1-enforce-defined-rule
    role: practice
  - target: b2.level-outcome.integrate-identity-access-control-l1-enforce-defined-rule
    role: assess
  - target: b2.level-outcome.integrate-identity-access-control-l2-propagate-context
    role: practice
  - target: b2.level-outcome.integrate-identity-access-control-l2-propagate-context
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

# Kata: заблокировать cross-tenant чтение Order

## Рабочая история

Orders service уже принимает `GET /orders/{order_id}`. Tenant A имеет `subject-a` и `order-a`, tenant B — `order-b`. Текущий handler проверяет подпись token и затем загружает Order только по `order_id`. Поэтому пользователь tenant A получает `200` и поля `order-b`: authentication работает, object authorization отсутствует.

Новое требование: валидный token tenant A не должен давать доступ к Order tenant B, даже если клиент добавит `X-Tenant-ID: tenant-b` или `?tenant_id=tenant-b`. Сначала запишите invariants и ожидаемые наблюдения, затем воспроизведите уязвимость, разместите trusted context/enforcement и докажите исправление.

Стартового scaffold и готового repository нет. Создайте минимальную систему самостоятельно. Достаточно Python 3.14.6, FastAPI 0.141.1, Starlette 1.3.1, PyJWT 2.13.0, `cryptography` 50.0.0, fixture RSA key pair и in-memory store. Не реализуйте login, token endpoint, JWKS или production database.

## Закреплённый контракт

- fixture issuer: `https://issuer.test.local`; audience: `orders-api`; algorithm: только `RS256`;
- обязательные claims: `iss`, `aud`, `sub`, `tenant_id`, `exp`, `nbf`; `leeway=0`;
- validator строит `IdentityContext(subject_id, tenant_id)` только после полной проверки;
- allow iff `order.tenant_id == context.tenant_id`; иначе deny by default;
- allowed `A→order-a`: `200 application/json`;
- missing/invalid token: `401 application/problem+json` с Bearer challenge;
- `A→order-b` и `A→order-missing`: одинаковый `404 application/problem+json`, `Cache-Control: no-store`, body `{"type":"https://orders.example/problems/order-not-found","title":"Order not found","status":404}`;
- audit не содержит token, Authorization header, claims dump или Order fields.

## Ограниченная задача

1. Запишите trusted-context, object-authorization, deny-by-default и disclosure invariants своими словами.
2. Создайте два tenant и по одному deterministic Order fixture.
3. Покажите failing test: валидный token A читает `order-b` через исходный path.
4. Введите единственную validation boundary и минимальный immutable context.
5. Разместите object check до формирования response DTO.
6. Добавьте forged request tenant и докажите, что context остался `tenant-a`.
7. Зафиксируйте безопасный audit decision и assertions об отсутствии secrets/чужих fields.

Не добавляйте готовый policy framework: цель kata — один cross-tenant bypass и observable propagation, а не универсальная authorization system.

## Ожидаемые результаты

| Проверка | Вход | Обязательное наблюдение |
|---|---|---|
| Baseline vulnerability | valid A token, `order-b` | test до исправления показывает недопустимый `200` |
| Allowed | valid A token, `order-a` | context `subject-a/tenant-a`, `200`, audit allow |
| Cross-tenant | valid A token, `order-b` | тот же context, `404`, ни одного поля `order-b`, audit deny |
| Forged tenant | valid A token, `order-b`, header/query tenant B | context не меняется, результат совпадает с cross-tenant |
| Unauthenticated sanity | без token | operation не вызвана, `401` + Bearer challenge |

Kata не требует полной project matrix: отдельный missing-object equality case и несколько обходных adapters входят в project. Здесь достаточно одного bypass, но проверка должна существовать и на component boundary, и на собранном HTTP path.

## Критерии самопроверки

- [ ] До кода записаны четыре invariants и populations.
- [ ] Разрешённый algorithm и key заданы verifier, а не token.
- [ ] `sub`/`tenant_id` не попадают в context до signature/issuer/audience/time validation.
- [ ] Header/query tenant не влияет на context или allow decision.
- [ ] Enforcement выполняется до DTO/serialization.
- [ ] Cross-tenant path возвращает закреплённый `404`, а response/audit не содержит Order fields или secrets.
- [ ] Есть failing-before/passing-after evidence одного bypass.
- [ ] Component test и ASGI/HTTP test называют разные проверяемые границы.

## Progressive hints

<details>
<summary>Подсказка 1 — найдите источник полномочия</summary>

Разделите все входы на server-validated и client-controlled. `order_id`, headers и query выбирает клиент. Только результат единственного validator может породить trusted tenant.

</details>

<details>
<summary>Подсказка 2 — сузьте передаваемый объект</summary>

Не передавайте вниз token или произвольный claims dictionary. Application operation достаточно двух проверенных строк; это упрощает отрицательные tests и audit assertions.

</details>

<details>
<summary>Подсказка 3 — проверьте место решения</summary>

Вызовите application operation напрямую с Order другого tenant. Если allow/deny существует только в router, вы нашли обход. Проверка должна предшествовать DTO, но оставаться наблюдаемой независимо от storage adapter.

</details>

<details>
<summary>Подсказка 4 — докажите отсутствие disclosure</summary>

Проверяйте не только status. Assert media type, cache header, точный body, отсутствие fixture fields и отсутствие credential substrings в audit sink.

</details>

## После выполнения

Объясните партнёру, какое доказательство относится к применению заданного rule (L1), а какое — к безопасной передаче context (L2). Если ответ опирается только на один `200/404` test, добавьте observation context и forged-input case.

Готового решения в material нет. Review оценивает ваши invariants, placement и evidence, а не сходство структуры каталогов с чужим примером.

## Источники и актуальность

Контракт проверен 2026-08-26 по [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725.html), [RFC 6750](https://www.rfc-editor.org/rfc/rfc6750.html), [PyJWT API](https://pyjwt.readthedocs.io/en/stable/api.html), [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), [OWASP BOLA](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/) и [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html). Starlette 1.6.0 новее baseline 1.3.1; обновление требует повторить ASGI observations.
