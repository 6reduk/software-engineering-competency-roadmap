---
id: b2.project-spec.order-cancellation-policy-service
kind: project-spec
title: Проектная спецификация — границы eligibility в Orders service
owner_track: b2
module: b2.module.service-architecture
coverage:
  - target: b2.level-outcome.design-service-architecture-l2-structure-typical-feature
    role: integrate
  - target: b2.level-outcome.design-service-architecture-l2-structure-typical-feature
    role: assess
  - target: b2.level-outcome.design-service-architecture-l3-reshape-changing-service
    role: integrate
  - target: b2.level-outcome.design-service-architecture-l3-reshape-changing-service
    role: assess
  - target: b2.level-outcome.verify-service-behavior-l2-select-test-boundaries
    role: integrate
  - target: b2.level-outcome.verify-service-behavior-l2-select-test-boundaries
    role: assess
status: accepted
updated: 2026-08-19
language: ru
---

# Проектная спецификация: границы eligibility в Orders service

Вы поддерживаете небольшой FastAPI Orders service. Read-only endpoint `GET /orders/{order_id}/cancellation-eligibility` исторически смешал HTTP mapping, ORM, Carrier HTTP call и правило отмены. Требование `PREMIUM + PACKED + handoff not started` привело к согласованным правкам этих частей и хрупким мокам.

Выполните в отдельном репозитории один интеграционный milestone: выделите application operation и чистую policy, подключите их к реальным persistence и Carrier HTTP adapters выбранным способом и докажите, что следующее изменение правила локализуется. Спецификация задаёт наблюдаемый результат, но не структуру репозитория, DI framework или эталонную реализацию.

## Предметный контракт

- `CREATED` разрешён для любого tier;
- `PACKED` разрешён только для `PREMIUM`, если Carrier сообщает `handoff_started=false`;
- остальные комбинации запрещены;
- operation ничего не записывает и не создаёт side effects;
- прежний HTTP status/body для существующих случаев сохраняется и документируется участником до миграции.

## Единственный milestone

### Цель

Получить работающий endpoint с реальными границами и разными классами проверок, а затем провести повторное небольшое policy change без согласованных правок delivery, persistence и Carrier client.

### Наблюдаемые deliverables

1. Небольшой FastAPI service и документированная команда запуска.
2. Реальный persistence adapter к выбранной локальной БД/ORM и реальный HTTP adapter к управляемой Carrier stub/service.
3. Application operation и domain policy, которые не импортируют FastAPI, ORM и конкретный HTTP client.
4. Один и тот же набор business-policy tests, проходящий с fake/in-memory adapters без FastAPI, DB и сети.
5. Отдельные adapter/integration checks для ORM mapping, Carrier response/error mapping и endpoint response.
6. Targeted regression прежнего внешнего поведения.
7. Повторное изменение: клиент `STANDARD` может отменить `PACKED` до handoff при локально выбранном дополнительном бизнес-условии. Условие фиксируется до реализации и меняет policy/application tests, но не требует согласованных правок router, ORM mapping и Carrier client.
8. Короткий decision record.

Повторное изменение — диагностический probe поверхности изменения, а не новое каноническое правило курса. Оно не должно расширять проект до pricing, transactions или identity.

## Decision record

Зафиксируйте:

- исходную боль через конкретный change path;
- минимум две альтернативы, например оставить orchestration в router, выделить только policy или выделить policy + operation + один/два ports;
- выбранную boundary и направление зависимостей;
- incremental migration от текущего endpoint без big-bang rewrite;
- стоимость indirection, contract maintenance и дополнительных tests;
- оставшиеся риски и неизвестные;
- критерий удаления abstraction, если у неё исчезнет независимая причина изменения.

## Verification contract

| Риск | Минимальное подтверждение |
|---|---|
| Ошибка business policy | Табличные tests без I/O для всех комбинаций status/tier/handoff |
| Ошибка application coordination | Tests с fake/in-memory adapters, включая отсутствие лишнего Carrier lookup там, где это часть выбранного решения |
| Неверный persistence mapping | Integration check с реальной выбранной БД/ORM |
| Неверный Carrier mapping | HTTP adapter check на success и минимум один внешний error outcome |
| Регрессия публичного поведения | Endpoint check фактического status/body |
| Скрытая связанность | Diff/отчёт повторного policy change с перечислением затронутых обязанностей и tests |

Business tests и adapter checks не заменяют друг друга. Используйте существующий разбор [фактической HTTP boundary](../../evolvable-api-contracts/learn/http-contract-execution-boundary.md) и [downstream client boundary](../../runtime-concurrency-lifecycle/learn/bounded-concurrency-pool-saturation.md); повторно проектировать timeout, retry, pool lifecycle и cancellation в этом milestone не нужно.

## Review criteria

- [ ] Один S06 substrate согласован в README, коде, tests и decision record.
- [ ] Внешнее прежнее поведение зафиксировано до миграции и сохранено.
- [ ] Policy исполняется без I/O и framework runtime.
- [ ] Production adapters заменяются fake/in-memory без изменения application/domain code.
- [ ] Реальные mappings имеют отдельные checks.
- [ ] Dependency direction объяснено и подтверждается imports/сборкой.
- [ ] Повторное policy change локализовано и сравнение до/после воспроизводимо.
- [ ] Рассмотрены минимум две альтернативы и стоимость выбранной границы.
- [ ] Transaction mechanics, B5/C1 и L4 claims не включены.
- [ ] Нет готового решения или фиктивной ImplementationReference.

## Non-goals

- предписанная Clean/Hexagonal/Onion architecture;
- обязательные repository, class-based use case или DI container;
- production database topology, migrations и performance tuning;
- commit/rollback, unit of work, outbox, refund, event publishing;
- полная service-wide verification strategy;
- timeout/retry/cancellation/pool design Carrier client;
- microservice decomposition и cross-team conventions.

## Вопросы защиты

### Что доказывает заменяемость adapter?

<details>
<summary>Ориентиры ответа</summary>

Один и тот же application/domain code и business suite работают с production и fake/in-memory реализациями; wiring меняется снаружи. Отдельные integration checks доказывают production mapping. Наличие interface без реально выполненной подмены недостаточно.

</details>

### Почему milestone отличается от kata?

<details>
<summary>Ориентиры ответа</summary>

Kata фокусируется на выделении минимальных границ из намеренно связанного scaffold. Проект интегрирует выбранное решение с реальной БД и HTTP adapter, разделяет evidence, требует decision record и повторное изменение как L3-проверку change surface.

</details>

### Какой риск остался после зелёных tests?

<details>
<summary>Ориентиры ответа</summary>

Нужно назвать пределы конкретных границ: fake не доказывает production mapping; локальная stub-интеграция не доказывает весь production Carrier behavior; endpoint checks не дают полной verification strategy. Риск связывается с отдельной проверкой или осознанным non-goal.

</details>

## ImplementationReference

Отсутствует до самостоятельного выполнения проекта и независимого review. Эта спецификация не является эталонной реализацией.
