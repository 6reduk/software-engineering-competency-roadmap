---
id: b2.plan.module-delivery
kind: plan
title: Аудит покрытия B2 и очередь модулей
owner_track: b2
status: accepted
updated: 2026-09-09
language: ru
---

# Аудит покрытия B2 и очередь модулей

> **Lifecycle update 2026-09-19.** Таблица `partial` ниже сохраняет snapshot
> M1.8.21, в котором module gate зависел от выполнения проекта участником.
> Текущее состояние готовности учебных пакетов находится в
> [каноническом module-state audit](../../../governance/state/MODULE-STATE.md); learner execution и
> proficiency больше не блокируют authoring closure.

## Назначение и способ чтения

Этот документ отвечает на два практических вопроса: что именно покрыто принятыми материалами B2 и какой один bounded package следует проектировать следующим. Это snapshot 2026-09-08 после acceptance M1.8.20. Данные независимо пересчитаны по YAML 61 accepted artifact двенадцати slices. Основания — [G18: принятие consolidation](../../../governance/reviews/M1.8.19-G18-b2-consolidation-acceptance.md) и [G19: принятие HTTP Runtime/S01](../../../governance/reviews/M1.8.20-G19-http-runtime-acceptance.md). G18 завершил consolidation и выбрал S01; G19 принял четыре материала S01. M1.8.21 обновляет план и производное досье; этот refresh и следующая рекомендация остаются в review.

Читать его следует в таком порядке:

1. сводка модулей показывает состояние module gate;
2. реестр 69 LevelOutcomes учитывает каждый outcome ровно один раз у primary capability;
3. карта shared membership показывает, почему одно outcome может быть применимо к нескольким модулям, но не дублирует базовый учёт;
4. очередь объясняет зависимости, а decision brief ограничивает только следующий пакет.

Плановые галочки из [coverage map](coverage-map.md) не считаются существующим покрытием. Источник факта — `coverage` в YAML принятых artifacts. `probe` показывает качество рассуждения, но не доказывает proficiency; project specification задаёт будущую самостоятельную работу, а не является готовой реализацией.

## Executive conclusion

- Из 10 модулей: `complete` — 0, `partial` — 10, `not-started` — 0, `blocked` — 0. Состояния не изменились.
- Принят 61 artifact двенадцати slices; 259 relationships = 22 capability-level `reference` + 237 outcome-level. Покрыты 58 из 69 outcomes; 11 без связей, семь `probe-only`.
- M1.8.20 добавил H0–H3: 10 relationships к Trace capability и Trace L1–L3, новых unique outcomes — 0. Trace L1/L2 получили собственные задания; Trace L3 в этом slice — только interview probe. Исторические C1/R3/R5 relationships сохранены.
- Breadth-pass имеет собственный содержательный вход 10/10; полный пятижанровый content flow теперь также 10/10. HTTP Runtime получил собственные index/interview/kata/project-spec, сохранил собственный R1 learn и supporting C1. Это не выполнение проекта участником и не module completion.
- D19 content/navigation и D20 content/exercise закрыты G19 с audit trail. Исполнение S01, независимое review реализации и возможная регистрация ImplementationReference остаются открытыми условиями D20/D26. Всего 12 project specs, зарегистрированных ImplementationReference — 0.
- Internal hard DAG сохранён: 13 рёбер, восемь capabilities без internal hard prerequisites. Все десять карточек — `not-ready-for-gate`: отсутствуют проверенные самостоятельные результаты, остаются scope gaps и применимое реальное L4 adoption.
- Рекомендуется ровно один следующий **B3 boundary intake**: ограничить будущую работу на границе application transaction и store isolation. Сравнение с B2 completion-tail и подготовкой gate дано ниже; B2 debt сохраняется, переход и следующий пакет ещё не приняты.

## Определения состояний

- `complete` — весь scope модуля покрыт принятыми artifacts, есть полный подходящий artifact flow, и module gate явно пройден.
- `partial` — у модуля есть собственное принятое содержательное покрытие, но остаются outcomes, жанры либо критерии gate.
- `not-started` — собственных принятых содержательных artifacts у модуля нет. Покрытие shared capability в чужом модуле отражается отдельно и не меняет это состояние.
- `blocked` — следующий корректный пакет модуля зависит от отсутствующего решения или непокрытого hard prerequisite.

Hard prerequisite считается выполненным для конкретного bounded package, когда принятое execution evidence (не только `probe`) подтверждает действие prerequisite capability на требуемой пакету глубине. По умолчанию нужен как минимум L2; если rationale ребра или следующий пакет требуют большей автономности, это фиксируется явно. Снятие `blocked` не означает, что prerequisite capability или её модуль завершены целиком.

Три разных уровня учёта не смешиваются: artifact coverage — отдельная YAML-связь; outcome coverage — наличие хотя бы одной принятой artifact-связи к точному LevelOutcome ID; module gate — отдельное решение о завершённости scope модуля.

## Сводка 10 модулей

| Module | Состояние | Develops: primary; supporting | Outcomes в membership / покрыто | Собственные жанры | Сценарии | Hard prerequisites, влияющие на очередь | Главный пробел |
|---|---|---|---:|---|---|---|---|
| HTTP service runtime (`b2.module.http-service-runtime`) | `partial` | `trace-request-execution`, `manage-service-resource-lifecycle`; `control-concurrency-cancellation` | 11 / 11 | index, learn, interview, kata, project-spec | S01, S02 | lifecycle и tracing — без internal hard prerequisites; cancellation требует lifecycle | Собственные H0–H3 и R1 дают полный content flow. Нет выполненного проекта и module gate; S01 не доказывает production Trace L3 или весь S02. Lifecycle L4 и Cancellation L4 имеют только `probe`. |
| Evolvable API contracts (`b2.module.evolvable-api-contracts`) | `partial` | `design-http-api-contracts`, `evolve-api-contracts`, `design-validation-error-contracts`, `design-idempotent-service-operations`; `verify-contract-compatibility` | 19 / 16 | index, learn, interview, kata, project-spec | S03, S04 | evolution, validation, idempotency и compatibility требуют явного HTTP contract | Idempotency L2/L3 добавлены supporting flow S07; остаются Idempotency L4, Evolution L1, Error L4 и module gate. |
| Identity and API security boundaries (`b2.module.identity-aware-boundaries`) | `partial` | `integrate-identity-access-control`, `enforce-api-security-abuse-controls`; `design-http-api-contracts`, `design-service-architecture` | 16 / 13 | index, learn, interview, kata, project-spec | S05, S14 | HTTP contract hard prerequisite выполнен; A3 readiness подтверждён локально и раздельно для S05 и operation-cost половины S14 | S05 покрывает Identity L1–L3, operation-cost flow — Abuse L1–L3. Identity L4, Abuse L4, callback/SSRF и aggregate quota/rate остаются долгом; отдельного module-gate decision нет. |
| Service architecture (`b2.module.service-architecture`) | `partial` | `design-service-architecture`; `integrate-external-services`, `verify-service-behavior` | 12 / 9 | index, learn, interview, kata, project-spec | S06 | primary capability — без internal hard prerequisites; baseline трека A2 используется для test/ADR context | Собственный S06 flow принят, но Architecture, External Services и Verification L4 не покрыты; явного module-gate decision нет. |
| Transactional persistence integration (`b2.module.transactional-persistence-integration`) | `partial` | `manage-application-transaction-boundaries`, `integrate-application-caching`; `design-idempotent-service-operations`, `verify-service-behavior` | 13 / 10 | index, learn, interview, kata, project-spec | S07, S15 | transaction boundary требует service architecture — Architecture L2/L3 приняты; отдельная B3 cache-store readiness S15 подтверждена, B5 неприменим к однопроцессной гарантии | Собственные S07/S15 flows покрывают Transaction L1–L3, Idempotency L2/L3 и Cache L2/L3. Cache L4, Idempotency L4, Verification L4 и отдельный module-gate decision отсутствуют; one-process evidence не завершает capability или модуль. |
| External service integration (`b2.module.external-service-integration`) | `partial` | `integrate-external-services`, `control-concurrency-cancellation`; `control-service-load-resources` | 11 / 10 | index, learn, interview, kata, project-spec | S08; S13 — контекст | external integration, cancellation и load control требуют lifecycle; R4/R5 поддерживают prerequisite, A3/B5 Gate 0 M1.8.17 локально подтверждён | E0–E4 дают собственный External L1/L2 flow. External L3 сохранён в R2/R3/R5; External L4 и отдельный module-gate decision отсутствуют. Полный S08 не завершён; Lifecycle/Cancellation/Load context не получает новых связей. |
| Background and message workflows (`b2.module.background-message-workflows`) | `partial` | `design-asynchronous-workflows`; `design-idempotent-service-operations`, `control-concurrency-cancellation` | 10 / 8 | index, learn, interview, kata, project-spec | S09 | workflow — без internal hard prerequisites; idempotency требует уже покрытого HTTP contract; B5 substrate gate S09 подтверждён отдельно | Собственный S09 flow покрывает Workflow L2/L3. Workflow L4, Idempotency L4 и отдельный module-gate decision отсутствуют; B5 readiness не является B5 proficiency. |
| Service verification (`b2.module.service-verification`) | `partial` | `verify-service-behavior`, `verify-contract-compatibility`; `design-service-architecture` | 12 / 10 | index, learn, interview, kata, project-spec | S10 | compatibility требует HTTP contract; prerequisite-контекст принят | Собственный S10 flow покрывает Verification L1–L3 и Compatibility L1–L3. Architecture L4 и Verification L4 пусты, Compatibility L4 остаётся `probe-only`; отдельного module-gate decision нет. |
| Safe service evolution (`b2.module.safe-service-evolution`) | `partial` | `deliver-service-changes-safely`; `evolve-api-contracts`, `verify-contract-compatibility` | 12 / 10 | index, learn, interview, kata, project-spec | S11 | delivery требует evolution + service verification + compatibility; C/V execution evidence принято, B6/B7 readiness подтверждена только для лаборатории S11 | Собственный S11 flow покрывает Delivery L1–L3; Delivery L4, Evolution L1 и отдельный module-gate decision отсутствуют. Compatibility L4 и Evolution L4 остаются probe-only; локальный rollout не завершает capability. |
| Performance and resource control (`b2.module.performance-resource-control`) | `partial` | `diagnose-service-performance`, `control-service-load-resources`; `manage-service-resource-lifecycle`, `control-concurrency-cancellation` | 14 / 14 | index, learn, interview, kata, project-spec | S12, S13; slice использует S08 | diagnosis требует tracing; load control требует lifecycle | Все applicable outcomes имеют связи, но L4 — только probes; slice центрирован на S08, S12 не раскрыт, module gate не пройден. |

Число «покрыто» в таблице относится к уникальным outcomes capabilities из `Develops`, поэтому shared membership намеренно повторяется между модулями. Это число нельзя складывать по строкам. Канонический знаменатель 69 дан ниже.

## Реестр принятых artifacts

Коды используются в outcome-аудите; каждый ведёт к существующему файлу с конкретной YAML-связью. Единица подсчёта relationship — отдельная пара `(target, role)` в YAML: поэтому `practice` и `assess` для одного target считаются двумя relationships, как и `integrate` и `assess`. Один artifact может иметь две relationships к одному target. Итог 259 не означает число уникальных пар `(artifact, target)` или уникально покрытых outcomes.

| Код | Artifact | Kind | Primary module | Relationships |
|---|---|---|---|---:|
| C0 | [Evolvable API contracts index](slices/evolvable-api-contracts/README.md) | index | evolvable API contracts | 4 capability `reference` |
| C1 | [HTTP contract execution boundary](slices/evolvable-api-contracts/learn/http-contract-execution-boundary.md) | learn | evolvable API contracts | 6 `explain` |
| C2 | [Compatible API change](slices/evolvable-api-contracts/learn/compatible-api-change.md) | learn | evolvable API contracts | 6 `explain` |
| C3 | [API contract evolution interview](slices/evolvable-api-contracts/interview/api-contract-evolution.md) | interview | evolvable API contracts | 9 `probe` |
| C4 | [Compatible delivery contract change kata](slices/evolvable-api-contracts/kata/compatible-delivery-contract-change.md) | kata | evolvable API contracts | 4 `practice` + 4 `assess` |
| C5 | [Evolvable Orders API project spec](slices/evolvable-api-contracts/project-spec/evolvable-orders-api.md) | project-spec | evolvable API contracts | 5 `integrate` + 5 `assess` |
| R0 | [Runtime concurrency lifecycle index](slices/runtime-concurrency-lifecycle/README.md) | index | performance/resource control | 5 capability `reference` |
| R1 | [Cancellation, deadlines and resource lifecycle](slices/runtime-concurrency-lifecycle/learn/cancellation-deadlines-resource-lifecycle.md) | learn | HTTP service runtime | 6 `explain` |
| R2 | [Bounded concurrency and pool saturation](slices/runtime-concurrency-lifecycle/learn/bounded-concurrency-pool-saturation.md) | learn | performance/resource control | 7 `explain` |
| R3 | [Runtime resource failure interview](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) | interview | performance/resource control | 17 `probe` |
| R4 | [Stop orphan work and pool exhaustion kata](slices/runtime-concurrency-lifecycle/kata/stop-orphan-work-and-pool-exhaustion.md) | kata | performance/resource control | 6 `practice` + 6 `assess` |
| R5 | [Resilient fan-out service project spec](slices/runtime-concurrency-lifecycle/project-spec/resilient-fanout-service.md) | project-spec | performance/resource control | 7 `integrate` + 7 `assess` |
| A0 | [Service architecture boundaries index](slices/service-architecture-boundaries/README.md) | index | service architecture | 2 capability `reference` |
| A1 | [Change isolation through service boundaries](slices/service-architecture-boundaries/learn/change-isolation-service-boundaries.md) | learn | service architecture | 5 `explain` |
| A2 | [Service boundary change interview](slices/service-architecture-boundaries/interview/service-boundary-change.md) | interview | service architecture | 5 `probe` |
| A3 | [Extract order cancellation policy kata](slices/service-architecture-boundaries/kata/extract-order-cancellation-policy.md) | kata | service architecture | 4 `practice` + 4 `assess` |
| A4 | [Order cancellation policy service project spec](slices/service-architecture-boundaries/project-spec/order-cancellation-policy-service.md) | project-spec | service architecture | 3 `integrate` + 3 `assess` |
| V0 | [Risk-based service verification index](slices/risk-based-service-verification/README.md) | index | service verification | 2 capability `reference` |
| V1 | [Truthful test boundaries](slices/risk-based-service-verification/learn/truthful-test-boundaries.md) | learn | service verification | 5 `explain` |
| V2 | [Green tests, broken contract interview](slices/risk-based-service-verification/interview/green-tests-broken-contract.md) | interview | service verification | 6 `probe` |
| V3 | [Detect Orders error-contract regression kata](slices/risk-based-service-verification/kata/detect-orders-error-contract-regression.md) | kata | service verification | 4 `practice` + 4 `assess` |
| V4 | [Orders verification portfolio project spec](slices/risk-based-service-verification/project-spec/orders-verification-portfolio.md) | project-spec | service verification | 2 `integrate` + 2 `assess` |
| T0 | [Transactional orders operation index](slices/transactional-orders-operation/README.md) | index | transactional persistence integration | 2 capability `reference` |
| T1 | [Transaction boundary failure windows](slices/transactional-orders-operation/learn/transaction-boundary-failure-windows.md) | learn | transactional persistence integration | 5 `explain` |
| T2 | [Commit succeeded, event unknown interview](slices/transactional-orders-operation/interview/commit-succeeded-event-unknown.md) | interview | transactional persistence integration | 5 `probe` |
| T3 | [Recover order confirmation kata](slices/transactional-orders-operation/kata/recover-order-confirmation.md) | kata | transactional persistence integration | 3 `practice` + 3 `assess` |
| T4 | [Resilient order confirmation project spec](slices/transactional-orders-operation/project-spec/resilient-order-confirmation.md) | project-spec | transactional persistence integration | 2 `integrate` + 2 `assess` |
| W0 | [Recoverable OrderConfirmed consumer index](slices/recoverable-order-confirmed-consumer/README.md) | index | background and message workflows | 1 capability `reference` |
| W1 | [Acknowledgement, redelivery and recovery boundary](slices/recoverable-order-confirmed-consumer/learn/acknowledgement-redelivery-recovery-boundary.md) | learn | background and message workflows | 2 `explain` |
| W2 | [Side effect committed, message unacked interview](slices/recoverable-order-confirmed-consumer/interview/side-effect-committed-message-unacked.md) | interview | background and message workflows | 2 `probe` |
| W3 | [Recover OrderConfirmed consumer kata](slices/recoverable-order-confirmed-consumer/kata/recover-order-confirmed-consumer.md) | kata | background and message workflows | 1 `practice` + 1 `assess` |
| W4 | [Resilient fulfillment consumer project spec](slices/recoverable-order-confirmed-consumer/project-spec/resilient-fulfillment-consumer.md) | project-spec | background and message workflows | 2 `integrate` + 2 `assess` |
| I0 | [Tenant-safe Orders authorization index](slices/tenant-scoped-orders-authorization/README.md) | index | identity-aware boundaries | 1 capability `reference` |
| I1 | [Trusted context and object authorization boundary](slices/tenant-scoped-orders-authorization/learn/trusted-context-object-authorization-boundary.md) | learn | identity-aware boundaries | 3 `explain` |
| I2 | [Valid token, cross-tenant Order interview](slices/tenant-scoped-orders-authorization/interview/valid-token-cross-tenant-order.md) | interview | identity-aware boundaries | 3 `probe` |
| I3 | [Block cross-tenant Order read kata](slices/tenant-scoped-orders-authorization/kata/block-cross-tenant-order-read.md) | kata | identity-aware boundaries | 2 `practice` + 2 `assess` |
| I4 | [Tenant-safe Orders read API project spec](slices/tenant-scoped-orders-authorization/project-spec/tenant-safe-orders-read-api.md) | project-spec | identity-aware boundaries | 2 `integrate` + 2 `assess` |
| O0 | [Cost-bounded Orders export index](slices/cost-bounded-orders-export/README.md) | index | identity-aware boundaries | 1 capability `reference` |
| O1 | [Server-owned cost admission boundary](slices/cost-bounded-orders-export/learn/server-owned-cost-admission-boundary.md) | learn | identity-aware boundaries | 3 `explain` |
| O2 | [Valid tenant, expensive Orders export interview](slices/cost-bounded-orders-export/interview/valid-tenant-expensive-export.md) | interview | identity-aware boundaries | 3 `probe` |
| O3 | [Block bulk-export cost bypass kata](slices/cost-bounded-orders-export/kata/block-bulk-export-cost-bypass.md) | kata | identity-aware boundaries | 1 `practice` + 1 `assess` |
| O4 | [Cost-bounded Orders export API project spec](slices/cost-bounded-orders-export/project-spec/cost-bounded-orders-export-api.md) | project-spec | identity-aware boundaries | 2 `integrate` + 2 `assess` |
| K0 | [Tenant-scoped Orders summary cache index](slices/tenant-scoped-orders-cache/README.md) | index | transactional persistence integration | 1 capability `reference` |
| K1 | [Cache-aside, freshness and concurrent-miss coalescing](slices/tenant-scoped-orders-cache/learn/cache-aside-freshness-coalescing.md) | learn | transactional persistence integration | 2 `explain` |
| K2 | [Concurrent miss and stale Orders summary interview](slices/tenant-scoped-orders-cache/interview/concurrent-miss-stale-order-summary.md) | interview | transactional persistence integration | 2 `probe` |
| K3 | [Stop Orders cache stampede kata](slices/tenant-scoped-orders-cache/kata/stop-orders-cache-stampede.md) | kata | transactional persistence integration | 1 `practice` + 1 `assess` |
| K4 | [Resilient tenant Orders summary cache project spec](slices/tenant-scoped-orders-cache/project-spec/resilient-orders-summary-cache.md) | project-spec | transactional persistence integration | 2 `integrate` + 2 `assess` |
| D0 | [Поэтапный выпуск изменения Orders API](slices/safe-orders-service-rollout/README.md) | index | safe service evolution | 1 capability `reference` |
| D1 | [Поэтапный rollout — остановка и восстановление](slices/safe-orders-service-rollout/learn/staged-rollout-stop-recovery.md) | learn | safe service evolution | 3 `explain` |
| D2 | [Интервью — Orders rollout при ограниченной обратимости](slices/safe-orders-service-rollout/interview/limited-reversibility-orders-change.md) | interview | safe service evolution | 3 `probe` |
| D3 | [Kata — остановить небезопасный Orders rollout](slices/safe-orders-service-rollout/kata/stop-unsafe-orders-rollout.md) | kata | safe service evolution | 1 `practice` + 1 `assess` |
| D4 | [Проект — Orders rollout по наблюдаемым условиям](slices/safe-orders-service-rollout/project-spec/evidence-driven-orders-rollout.md) | project-spec | safe service evolution | 2 `integrate` + 2 `assess` |

### Дельта M1.8.17

| Код | Artifact | Kind | Primary module | Relationships |
|---|---|---|---|---:|
| E0 | [Правдивая граница клиента Pricing](slices/truthful-pricing-client-boundary/README.md) | index | external service integration | 1 capability `reference` |
| E1 | [От HTTP-ответа к предметному исходу](slices/truthful-pricing-client-boundary/learn/response-to-domain-outcome.md) | learn | external service integration | 2 `explain` |
| E2 | [Решения на границе Pricing](slices/truthful-pricing-client-boundary/interview/pricing-client-decisions.md) | interview | external service integration | 2 `probe` |
| E3 | [Прекратить подмену сбоя пустым результатом](slices/truthful-pricing-client-boundary/kata/stop-failure-to-empty-collapse.md) | kata | external service integration | 1 `practice` + 1 `assess` |
| E4 | [Самостоятельно интегрировать Pricing](slices/truthful-pricing-client-boundary/project-spec/integrate-one-pricing-operation.md) | project-spec | external service integration | 1 `integrate` + 1 `assess` |

### Дельта M1.8.20

H0–H3 — локальные коды аудита, не новые semantic IDs. Все четыре принадлежат HTTP Service Runtime; отдельный learn не добавлен.

| Код | Artifact | Kind | Primary module | Relationships |
|---|---|---|---|---:|
| H0 | [Где запрос потерял контекст](slices/request-context-loss-diagnosis/README.md) | index | HTTP service runtime | 1 capability `reference` |
| H1 | [Восстановить путь контекста](slices/request-context-loss-diagnosis/interview/reconstruct-context-path.md) | interview | HTTP service runtime | 3 `probe` |
| H2 | [Локализовать потерю](slices/request-context-loss-diagnosis/kata/localize-context-loss.md) | kata | HTTP service runtime | 2 `practice` + 2 `assess` |
| H3 | [Сохранить контекст через refactor](slices/request-context-loss-diagnosis/project-spec/preserve-context-through-refactor.md) | project-spec | HTTP service runtime | 1 `integrate` + 1 `assess` |

## Базовый outcome-level audit: 69 outcomes

В каждой строке ровно один канонический LevelOutcome из [каталога outcomes](level-outcomes.md). Короткое имя не заменяет semantic ID. `—` означает отсутствие принятой coverage relationship. Наличие `probe` отдельно отмечено и не трактуется как execution evidence.

### Request runtime

| LevelOutcome | Принятые связи |
|---|---|
| L1 — пройти известный request path (`b2.level-outcome.trace-request-execution-l1-follow-known-path`) | [C1](slices/evolvable-api-contracts/learn/http-contract-execution-boundary.md) `explain`; [H1](slices/request-context-loss-diagnosis/interview/reconstruct-context-path.md) `probe`; [H2](slices/request-context-loss-diagnosis/kata/localize-context-loss.md) `practice`, `assess` |
| L2 — диагностировать типовой сбой (`b2.level-outcome.trace-request-execution-l2-diagnose-common-failure`) | [C1](slices/evolvable-api-contracts/learn/http-contract-execution-boundary.md) `explain`; [H1](slices/request-context-loss-diagnosis/interview/reconstruct-context-path.md) `probe`; [H2](slices/request-context-loss-diagnosis/kata/localize-context-loss.md) `practice`, `assess`; [H3](slices/request-context-loss-diagnosis/project-spec/preserve-context-through-refactor.md) `integrate`, `assess` |
| L3 — восстановить production path (`b2.level-outcome.trace-request-execution-l3-explain-production-path`) | [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe`; [R5](slices/runtime-concurrency-lifecycle/project-spec/resilient-fanout-service.md) `integrate`, `assess`; [H1](slices/request-context-loss-diagnosis/interview/reconstruct-context-path.md) `probe` |
| L1 — использовать заданный resource scope (`b2.level-outcome.manage-service-resource-lifecycle-l1-use-defined-scope`) | [R1](slices/runtime-concurrency-lifecycle/learn/cancellation-deadlines-resource-lifecycle.md) `explain` |
| L2 — спроектировать локальный lifecycle (`b2.level-outcome.manage-service-resource-lifecycle-l2-design-local-lifecycle`) | [R1](slices/runtime-concurrency-lifecycle/learn/cancellation-deadlines-resource-lifecycle.md) `explain`; [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe`; [R4](slices/runtime-concurrency-lifecycle/kata/stop-orphan-work-and-pool-exhaustion.md) `practice`, `assess` |
| L3 — устранить leak/race (`b2.level-outcome.manage-service-resource-lifecycle-l3-remediate-leak`) | [R1](slices/runtime-concurrency-lifecycle/learn/cancellation-deadlines-resource-lifecycle.md) `explain`; [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe`; [R5](slices/runtime-concurrency-lifecycle/project-spec/resilient-fanout-service.md) `integrate`, `assess` |
| L4 — установить service policy (`b2.level-outcome.manage-service-resource-lifecycle-l4-establish-service-policy`) | [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe` only |

### API contracts and evolution

| LevelOutcome | Принятые связи |
|---|---|
| L1 — реализовать заданный HTTP contract (`b2.level-outcome.design-http-api-contracts-l1-implement-specified-contract`) | [C1](slices/evolvable-api-contracts/learn/http-contract-execution-boundary.md) `explain` |
| L2 — спроектировать типовой resource (`b2.level-outcome.design-http-api-contracts-l2-design-typical-resource`) | [C1](slices/evolvable-api-contracts/learn/http-contract-execution-boundary.md) `explain`; [C3](slices/evolvable-api-contracts/interview/api-contract-evolution.md) `probe`; [C4](slices/evolvable-api-contracts/kata/compatible-delivery-contract-change.md) `practice`, `assess` |
| L3 — разрешить неоднозначные требования (`b2.level-outcome.design-http-api-contracts-l3-resolve-ambiguous-requirements`) | [C3](slices/evolvable-api-contracts/interview/api-contract-evolution.md) `probe`; [C5](slices/evolvable-api-contracts/project-spec/evolvable-orders-api.md) `integrate`, `assess` |
| L4 — установить межкомандные conventions (`b2.level-outcome.design-http-api-contracts-l4-establish-cross-team-conventions`) | [C3](slices/evolvable-api-contracts/interview/api-contract-evolution.md) `probe` only |
| L1 — применить additive change (`b2.level-outcome.evolve-api-contracts-l1-apply-additive-change`) | — |
| L2 — спланировать compatible change (`b2.level-outcome.evolve-api-contracts-l2-plan-compatible-change`) | [C2](slices/evolvable-api-contracts/learn/compatible-api-change.md) `explain`; [C3](slices/evolvable-api-contracts/interview/api-contract-evolution.md) `probe`; [C4](slices/evolvable-api-contracts/kata/compatible-delivery-contract-change.md) `practice`, `assess` |
| L3 — провести миграцию сервиса (`b2.level-outcome.evolve-api-contracts-l3-own-service-migration`) | [C2](slices/evolvable-api-contracts/learn/compatible-api-change.md) `explain`; [C3](slices/evolvable-api-contracts/interview/api-contract-evolution.md) `probe`; [C5](slices/evolvable-api-contracts/project-spec/evolvable-orders-api.md) `integrate`, `assess` |
| L4 — провести cross-team migration (`b2.level-outcome.evolve-api-contracts-l4-lead-cross-team-migration`) | [C3](slices/evolvable-api-contracts/interview/api-contract-evolution.md) `probe` only |
| L1 — следовать error convention (`b2.level-outcome.design-validation-error-contracts-l1-follow-error-convention`) | [C1](slices/evolvable-api-contracts/learn/http-contract-execution-boundary.md) `explain` |
| L2 — спроектировать client errors (`b2.level-outcome.design-validation-error-contracts-l2-design-client-errors`) | [C1](slices/evolvable-api-contracts/learn/http-contract-execution-boundary.md) `explain`; [C4](slices/evolvable-api-contracts/kata/compatible-delivery-contract-change.md) `practice`, `assess` |
| L3 — унифицировать service boundaries (`b2.level-outcome.design-validation-error-contracts-l3-unify-service-boundaries`) | [C5](slices/evolvable-api-contracts/project-spec/evolvable-orders-api.md) `integrate`, `assess` |
| L4 — установить shared error convention (`b2.level-outcome.design-validation-error-contracts-l4-establish-shared-convention`) | — |
| L2 — реализовать известный idempotency pattern (`b2.level-outcome.design-idempotent-service-operations-l2-implement-known-pattern`) | [T1](slices/transactional-orders-operation/learn/transaction-boundary-failure-windows.md) `explain`; [T2](slices/transactional-orders-operation/interview/commit-succeeded-event-unknown.md) `probe`; [T3](slices/transactional-orders-operation/kata/recover-order-confirmation.md) `practice`, `assess` |
| L3 — спроектировать failure-safe operation (`b2.level-outcome.design-idempotent-service-operations-l3-design-failure-safe-operation`) | [T1](slices/transactional-orders-operation/learn/transaction-boundary-failure-windows.md) `explain`; [T2](slices/transactional-orders-operation/interview/commit-succeeded-event-unknown.md) `probe`; [T4](slices/transactional-orders-operation/project-spec/resilient-order-confirmation.md) `integrate`, `assess` |
| L4 — согласовать operation contracts (`b2.level-outcome.design-idempotent-service-operations-l4-align-operation-contracts`) | — |

### Identity and API security

| LevelOutcome | Принятые связи |
|---|---|
| L1 — применить заданное auth rule (`b2.level-outcome.integrate-identity-access-control-l1-enforce-defined-rule`) | [I1](slices/tenant-scoped-orders-authorization/learn/trusted-context-object-authorization-boundary.md) `explain`; [I2](slices/tenant-scoped-orders-authorization/interview/valid-token-cross-tenant-order.md) `probe`; [I3](slices/tenant-scoped-orders-authorization/kata/block-cross-tenant-order-read.md) `practice`, `assess` |
| L2 — провести subject/tenant context (`b2.level-outcome.integrate-identity-access-control-l2-propagate-context`) | [I1](slices/tenant-scoped-orders-authorization/learn/trusted-context-object-authorization-boundary.md) `explain`; [I2](slices/tenant-scoped-orders-authorization/interview/valid-token-cross-tenant-order.md) `probe`; [I3](slices/tenant-scoped-orders-authorization/kata/block-cross-tenant-order-read.md) `practice`, `assess`; [I4](slices/tenant-scoped-orders-authorization/project-spec/tenant-safe-orders-read-api.md) `integrate`, `assess` |
| L3 — спроектировать service enforcement (`b2.level-outcome.integrate-identity-access-control-l3-design-service-enforcement`) | [I1](slices/tenant-scoped-orders-authorization/learn/trusted-context-object-authorization-boundary.md) `explain`; [I2](slices/tenant-scoped-orders-authorization/interview/valid-token-cross-tenant-order.md) `probe`; [I4](slices/tenant-scoped-orders-authorization/project-spec/tenant-safe-orders-read-api.md) `integrate`, `assess` |
| L4 — согласовать cross-service policy (`b2.level-outcome.integrate-identity-access-control-l4-align-cross-service-policy`) | — |
| L1 — применить заданные abuse controls (`b2.level-outcome.enforce-api-security-abuse-controls-l1-apply-defined-controls`) | [O1](slices/cost-bounded-orders-export/learn/server-owned-cost-admission-boundary.md) `explain`; [O2](slices/cost-bounded-orders-export/interview/valid-tenant-expensive-export.md) `probe`; [O3](slices/cost-bounded-orders-export/kata/block-bulk-export-cost-bypass.md) `practice`, `assess` |
| L2 — защитить типовой endpoint (`b2.level-outcome.enforce-api-security-abuse-controls-l2-protect-typical-endpoint`) | [O1](slices/cost-bounded-orders-export/learn/server-owned-cost-admission-boundary.md) `explain`; [O2](slices/cost-bounded-orders-export/interview/valid-tenant-expensive-export.md) `probe`; [O4](slices/cost-bounded-orders-export/project-spec/cost-bounded-orders-export-api.md) `integrate`, `assess` |
| L3 — спроектировать service abuse boundary (`b2.level-outcome.enforce-api-security-abuse-controls-l3-design-service-abuse-boundary`) | [O1](slices/cost-bounded-orders-export/learn/server-owned-cost-admission-boundary.md) `explain`; [O2](slices/cost-bounded-orders-export/interview/valid-tenant-expensive-export.md) `probe`; [O4](slices/cost-bounded-orders-export/project-spec/cost-bounded-orders-export-api.md) `integrate`, `assess` |
| L4 — установить cross-service controls (`b2.level-outcome.enforce-api-security-abuse-controls-l4-establish-cross-service-controls`) | — |

### Service architecture, persistence and workflows

| LevelOutcome | Принятые связи |
|---|---|
| L1 — следовать существующим boundaries (`b2.level-outcome.design-service-architecture-l1-follow-existing-boundaries`) | [A1](slices/service-architecture-boundaries/learn/change-isolation-service-boundaries.md) `explain`; [A2](slices/service-architecture-boundaries/interview/service-boundary-change.md) `probe`; [A3](slices/service-architecture-boundaries/kata/extract-order-cancellation-policy.md) `practice`, `assess` |
| L2 — структурировать типовую feature (`b2.level-outcome.design-service-architecture-l2-structure-typical-feature`) | [A1](slices/service-architecture-boundaries/learn/change-isolation-service-boundaries.md) `explain`; [A2](slices/service-architecture-boundaries/interview/service-boundary-change.md) `probe`; [A3](slices/service-architecture-boundaries/kata/extract-order-cancellation-policy.md) `practice`, `assess`; [A4](slices/service-architecture-boundaries/project-spec/order-cancellation-policy-service.md) `integrate`, `assess` |
| L3 — перестроить изменяющийся сервис (`b2.level-outcome.design-service-architecture-l3-reshape-changing-service`) | [A1](slices/service-architecture-boundaries/learn/change-isolation-service-boundaries.md) `explain`; [A2](slices/service-architecture-boundaries/interview/service-boundary-change.md) `probe`; [A4](slices/service-architecture-boundaries/project-spec/order-cancellation-policy-service.md) `integrate`, `assess` |
| L4 — установить reusable boundaries (`b2.level-outcome.design-service-architecture-l4-establish-reusable-boundaries`) | — |
| L1 — использовать заданную transaction unit (`b2.level-outcome.manage-application-transaction-boundaries-l1-use-defined-unit`) | [T1](slices/transactional-orders-operation/learn/transaction-boundary-failure-windows.md) `explain`; [T2](slices/transactional-orders-operation/interview/commit-succeeded-event-unknown.md) `probe`; [T3](slices/transactional-orders-operation/kata/recover-order-confirmation.md) `practice`, `assess` |
| L2 — спроектировать operation boundary (`b2.level-outcome.manage-application-transaction-boundaries-l2-design-operation-boundary`) | [T1](slices/transactional-orders-operation/learn/transaction-boundary-failure-windows.md) `explain`; [T2](slices/transactional-orders-operation/interview/commit-succeeded-event-unknown.md) `probe`; [T3](slices/transactional-orders-operation/kata/recover-order-confirmation.md) `practice`, `assess` |
| L3 — разрешить consistency side effects (`b2.level-outcome.manage-application-transaction-boundaries-l3-resolve-side-effect-consistency`) | [T1](slices/transactional-orders-operation/learn/transaction-boundary-failure-windows.md) `explain`; [T2](slices/transactional-orders-operation/interview/commit-succeeded-event-unknown.md) `probe`; [T4](slices/transactional-orders-operation/project-spec/resilient-order-confirmation.md) `integrate`, `assess` |
| L2 — применить известный cache pattern (`b2.level-outcome.integrate-application-caching-l2-apply-known-cache-pattern`) | [K1](slices/tenant-scoped-orders-cache/learn/cache-aside-freshness-coalescing.md) `explain`; [K2](slices/tenant-scoped-orders-cache/interview/concurrent-miss-stale-order-summary.md) `probe`; [K3](slices/tenant-scoped-orders-cache/kata/stop-orders-cache-stampede.md) `practice`, `assess`; [K4](slices/tenant-scoped-orders-cache/project-spec/resilient-orders-summary-cache.md) `integrate`, `assess` |
| L3 — спроектировать cache consistency/failure (`b2.level-outcome.integrate-application-caching-l3-design-consistency-failure-behavior`) | [K1](slices/tenant-scoped-orders-cache/learn/cache-aside-freshness-coalescing.md) `explain`; [K2](slices/tenant-scoped-orders-cache/interview/concurrent-miss-stale-order-summary.md) `probe`; [K4](slices/tenant-scoped-orders-cache/project-spec/resilient-orders-summary-cache.md) `integrate`, `assess` |
| L4 — координировать cache migration (`b2.level-outcome.integrate-application-caching-l4-coordinate-cache-migration`) | — |
| L2 — реализовать background flow (`b2.level-outcome.design-asynchronous-workflows-l2-implement-background-flow`) | [W1](slices/recoverable-order-confirmed-consumer/learn/acknowledgement-redelivery-recovery-boundary.md) `explain`; [W2](slices/recoverable-order-confirmed-consumer/interview/side-effect-committed-message-unacked.md) `probe`; [W3](slices/recoverable-order-confirmed-consumer/kata/recover-order-confirmed-consumer.md) `practice`, `assess`; [W4](slices/recoverable-order-confirmed-consumer/project-spec/resilient-fulfillment-consumer.md) `integrate`, `assess` |
| L3 — спроектировать recoverable workflow (`b2.level-outcome.design-asynchronous-workflows-l3-design-recoverable-workflow`) | [W1](slices/recoverable-order-confirmed-consumer/learn/acknowledgement-redelivery-recovery-boundary.md) `explain`; [W2](slices/recoverable-order-confirmed-consumer/interview/side-effect-committed-message-unacked.md) `probe`; [W4](slices/recoverable-order-confirmed-consumer/project-spec/resilient-fulfillment-consumer.md) `integrate`, `assess` |
| L4 — координировать workflow migration (`b2.level-outcome.design-asynchronous-workflows-l4-coordinate-workflow-migration`) | — |

### External integration and runtime control

| LevelOutcome | Принятые связи |
|---|---|
| L1 — использовать заданный client (`b2.level-outcome.integrate-external-services-l1-use-defined-client`) | [R2](slices/runtime-concurrency-lifecycle/learn/bounded-concurrency-pool-saturation.md) `explain`; [E1](slices/truthful-pricing-client-boundary/learn/response-to-domain-outcome.md) `explain`; [E2](slices/truthful-pricing-client-boundary/interview/pricing-client-decisions.md) `probe`; [E3](slices/truthful-pricing-client-boundary/kata/stop-failure-to-empty-collapse.md) `practice`, `assess` |
| L2 — спроектировать client boundary (`b2.level-outcome.integrate-external-services-l2-design-typical-client-boundary`) | [R2](slices/runtime-concurrency-lifecycle/learn/bounded-concurrency-pool-saturation.md) `explain`; [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe`; [R4](slices/runtime-concurrency-lifecycle/kata/stop-orphan-work-and-pool-exhaustion.md) `practice`, `assess`; [E1](slices/truthful-pricing-client-boundary/learn/response-to-domain-outcome.md) `explain`; [E2](slices/truthful-pricing-client-boundary/interview/pricing-client-decisions.md) `probe`; [E4](slices/truthful-pricing-client-boundary/project-spec/integrate-one-pricing-operation.md) `integrate`, `assess` |
| L3 — владеть degraded dependency (`b2.level-outcome.integrate-external-services-l3-own-degraded-dependency`) | [R2](slices/runtime-concurrency-lifecycle/learn/bounded-concurrency-pool-saturation.md) `explain`; [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe`; [R5](slices/runtime-concurrency-lifecycle/project-spec/resilient-fanout-service.md) `integrate`, `assess` |
| L4 — согласовать integration policy (`b2.level-outcome.integrate-external-services-l4-align-integration-policy`) | — |
| L1 — сохранить cleanup при cancellation (`b2.level-outcome.control-concurrency-cancellation-l1-preserve-cleanup`) | [R1](slices/runtime-concurrency-lifecycle/learn/cancellation-deadlines-resource-lifecycle.md) `explain` |
| L2 — ограничить local work (`b2.level-outcome.control-concurrency-cancellation-l2-bound-local-work`) | [R1](slices/runtime-concurrency-lifecycle/learn/cancellation-deadlines-resource-lifecycle.md) `explain`; [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe`; [R4](slices/runtime-concurrency-lifecycle/kata/stop-orphan-work-and-pool-exhaustion.md) `practice`, `assess` |
| L3 — устранить runtime failure (`b2.level-outcome.control-concurrency-cancellation-l3-remediate-runtime-failure`) | [R1](slices/runtime-concurrency-lifecycle/learn/cancellation-deadlines-resource-lifecycle.md) `explain`; [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe`; [R5](slices/runtime-concurrency-lifecycle/project-spec/resilient-fanout-service.md) `integrate`, `assess` |
| L4 — установить runtime policy (`b2.level-outcome.control-concurrency-cancellation-l4-establish-runtime-policy`) | [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe` only |

### Verification and delivery

| LevelOutcome | Принятые связи |
|---|---|
| L1 — проверить local behavior (`b2.level-outcome.verify-service-behavior-l1-test-local-behavior`) | [A1](slices/service-architecture-boundaries/learn/change-isolation-service-boundaries.md) `explain`; [A2](slices/service-architecture-boundaries/interview/service-boundary-change.md) `probe`; [A3](slices/service-architecture-boundaries/kata/extract-order-cancellation-policy.md) `practice`, `assess`; [V1](slices/risk-based-service-verification/learn/truthful-test-boundaries.md) `explain`; [V2](slices/risk-based-service-verification/interview/green-tests-broken-contract.md) `probe`; [V3](slices/risk-based-service-verification/kata/detect-orders-error-contract-regression.md) `practice`, `assess` |
| L2 — выбрать test boundaries (`b2.level-outcome.verify-service-behavior-l2-select-test-boundaries`) | [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe`; [R4](slices/runtime-concurrency-lifecycle/kata/stop-orphan-work-and-pool-exhaustion.md) `practice`, `assess`; [A1](slices/service-architecture-boundaries/learn/change-isolation-service-boundaries.md) `explain`; [A2](slices/service-architecture-boundaries/interview/service-boundary-change.md) `probe`; [A3](slices/service-architecture-boundaries/kata/extract-order-cancellation-policy.md) `practice`, `assess`; [A4](slices/service-architecture-boundaries/project-spec/order-cancellation-policy-service.md) `integrate`, `assess`; [V1](slices/risk-based-service-verification/learn/truthful-test-boundaries.md) `explain`; [V2](slices/risk-based-service-verification/interview/green-tests-broken-contract.md) `probe`; [V3](slices/risk-based-service-verification/kata/detect-orders-error-contract-regression.md) `practice`, `assess` |
| L3 — спроектировать service verification strategy (`b2.level-outcome.verify-service-behavior-l3-design-service-strategy`) | [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe`; [R5](slices/runtime-concurrency-lifecycle/project-spec/resilient-fanout-service.md) `integrate`, `assess`; [V1](slices/risk-based-service-verification/learn/truthful-test-boundaries.md) `explain`; [V2](slices/risk-based-service-verification/interview/green-tests-broken-contract.md) `probe`; [V4](slices/risk-based-service-verification/project-spec/orders-verification-portfolio.md) `integrate`, `assess` |
| L4 — согласовать cross-team evidence (`b2.level-outcome.verify-service-behavior-l4-align-cross-team-evidence`) | — |
| L1 — поддерживать contract check (`b2.level-outcome.verify-contract-compatibility-l1-maintain-contract-check`) | [V1](slices/risk-based-service-verification/learn/truthful-test-boundaries.md) `explain`; [V2](slices/risk-based-service-verification/interview/green-tests-broken-contract.md) `probe`; [V3](slices/risk-based-service-verification/kata/detect-orders-error-contract-regression.md) `practice`, `assess` |
| L2 — обнаружить breaking change (`b2.level-outcome.verify-contract-compatibility-l2-detect-breaking-change`) | [C2](slices/evolvable-api-contracts/learn/compatible-api-change.md) `explain`; [C3](slices/evolvable-api-contracts/interview/api-contract-evolution.md) `probe`; [C4](slices/evolvable-api-contracts/kata/compatible-delivery-contract-change.md) `practice`, `assess`; [V1](slices/risk-based-service-verification/learn/truthful-test-boundaries.md) `explain`; [V2](slices/risk-based-service-verification/interview/green-tests-broken-contract.md) `probe`; [V3](slices/risk-based-service-verification/kata/detect-orders-error-contract-regression.md) `practice`, `assess` |
| L3 — построить consumer evidence (`b2.level-outcome.verify-contract-compatibility-l3-build-consumer-evidence`) | [C2](slices/evolvable-api-contracts/learn/compatible-api-change.md) `explain`; [C3](slices/evolvable-api-contracts/interview/api-contract-evolution.md) `probe`; [C5](slices/evolvable-api-contracts/project-spec/evolvable-orders-api.md) `integrate`, `assess`; [V2](slices/risk-based-service-verification/interview/green-tests-broken-contract.md) `probe`; [V4](slices/risk-based-service-verification/project-spec/orders-verification-portfolio.md) `integrate`, `assess` |
| L4 — установить compatibility process (`b2.level-outcome.verify-contract-compatibility-l4-establish-compatibility-process`) | [C3](slices/evolvable-api-contracts/interview/api-contract-evolution.md) `probe` only |
| L1 — следовать rollout checklist (`b2.level-outcome.deliver-service-changes-safely-l1-follow-rollout-checklist`) | [D1](slices/safe-orders-service-rollout/learn/staged-rollout-stop-recovery.md) `explain`; [D2](slices/safe-orders-service-rollout/interview/limited-reversibility-orders-change.md) `probe`; [D3](slices/safe-orders-service-rollout/kata/stop-unsafe-orders-rollout.md) `practice`, `assess` |
| L2 — спланировать типовой rollout (`b2.level-outcome.deliver-service-changes-safely-l2-plan-typical-rollout`) | [C2](slices/evolvable-api-contracts/learn/compatible-api-change.md) `explain`; [D1](slices/safe-orders-service-rollout/learn/staged-rollout-stop-recovery.md) `explain`; [D2](slices/safe-orders-service-rollout/interview/limited-reversibility-orders-change.md) `probe`; [D4](slices/safe-orders-service-rollout/project-spec/evidence-driven-orders-rollout.md) `integrate`, `assess` |
| L3 — провести risky migration (`b2.level-outcome.deliver-service-changes-safely-l3-own-risky-migration`) | [C2](slices/evolvable-api-contracts/learn/compatible-api-change.md) `explain`; [C5](slices/evolvable-api-contracts/project-spec/evolvable-orders-api.md) `integrate`, `assess`; [D1](slices/safe-orders-service-rollout/learn/staged-rollout-stop-recovery.md) `explain`; [D2](slices/safe-orders-service-rollout/interview/limited-reversibility-orders-change.md) `probe`; [D4](slices/safe-orders-service-rollout/project-spec/evidence-driven-orders-rollout.md) `integrate`, `assess` |
| L4 — координировать cross-team change (`b2.level-outcome.deliver-service-changes-safely-l4-coordinate-cross-team-change`) | — |

### Performance and load

| LevelOutcome | Принятые связи |
|---|---|
| L2 — локализовать типовой bottleneck (`b2.level-outcome.diagnose-service-performance-l2-localize-common-bottleneck`) | [R2](slices/runtime-concurrency-lifecycle/learn/bounded-concurrency-pool-saturation.md) `explain`; [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe`; [R4](slices/runtime-concurrency-lifecycle/kata/stop-orphan-work-and-pool-exhaustion.md) `practice`, `assess` |
| L3 — исследовать production degradation (`b2.level-outcome.diagnose-service-performance-l3-investigate-production-degradation`) | [R2](slices/runtime-concurrency-lifecycle/learn/bounded-concurrency-pool-saturation.md) `explain`; [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe`; [R5](slices/runtime-concurrency-lifecycle/project-spec/resilient-fanout-service.md) `integrate`, `assess` |
| L4 — вести cross-service analysis (`b2.level-outcome.diagnose-service-performance-l4-lead-cross-service-analysis`) | [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe` only |
| L2 — настроить local bounds (`b2.level-outcome.control-service-load-resources-l2-configure-local-bounds`) | [R2](slices/runtime-concurrency-lifecycle/learn/bounded-concurrency-pool-saturation.md) `explain`; [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe`; [R4](slices/runtime-concurrency-lifecycle/kata/stop-orphan-work-and-pool-exhaustion.md) `practice`, `assess` |
| L3 — спроектировать graceful overload (`b2.level-outcome.control-service-load-resources-l3-design-graceful-overload`) | [R2](slices/runtime-concurrency-lifecycle/learn/bounded-concurrency-pool-saturation.md) `explain`; [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe`; [R5](slices/runtime-concurrency-lifecycle/project-spec/resilient-fanout-service.md) `integrate`, `assess` |
| L4 — согласовать capacity boundaries (`b2.level-outcome.control-service-load-resources-l4-align-capacity-boundaries`) | [R3](slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) `probe` only |

## Shared module membership

Базовый реестр выше считает outcome только у его capability. Ниже показано повторное использование capabilities модулями без создания новых outcomes.

| Shared capability | Primary module | Дополнительные modules из `Develops` |
|---|---|---|
| Трассировка запроса (`b2.capability.trace-request-execution`) | HTTP service runtime | — |
| Lifecycle ресурсов (`b2.capability.manage-service-resource-lifecycle`) | HTTP service runtime | Performance and resource control |
| HTTP API contracts (`b2.capability.design-http-api-contracts`) | Evolvable API contracts | Identity and API security boundaries |
| API evolution (`b2.capability.evolve-api-contracts`) | Evolvable API contracts | Safe service evolution |
| Validation/error contracts (`b2.capability.design-validation-error-contracts`) | Evolvable API contracts | — |
| Identity/access control (`b2.capability.integrate-identity-access-control`) | Identity and API security boundaries | — |
| API abuse controls (`b2.capability.enforce-api-security-abuse-controls`) | Identity and API security boundaries | — |
| Service architecture (`b2.capability.design-service-architecture`) | Service architecture | Identity and API security boundaries; Service verification |
| Transaction boundaries (`b2.capability.manage-application-transaction-boundaries`) | Transactional persistence integration | — |
| Application caching (`b2.capability.integrate-application-caching`) | Transactional persistence integration | — |
| Idempotent operations (`b2.capability.design-idempotent-service-operations`) | Evolvable API contracts | Transactional persistence integration; Background and message workflows |
| External integrations (`b2.capability.integrate-external-services`) | External service integration | Service architecture |
| Async workflows (`b2.capability.design-asynchronous-workflows`) | Background and message workflows | — |
| Concurrency/cancellation (`b2.capability.control-concurrency-cancellation`) | External service integration | HTTP service runtime; Background and message workflows; Performance and resource control |
| Service verification (`b2.capability.verify-service-behavior`) | Service verification | Service architecture; Transactional persistence integration |
| Contract compatibility (`b2.capability.verify-contract-compatibility`) | Service verification | Evolvable API contracts; Safe service evolution |
| Safe delivery (`b2.capability.deliver-service-changes-safely`) | Safe service evolution | — |
| Performance diagnosis (`b2.capability.diagnose-service-performance`) | Performance and resource control | — |
| Load/resource control (`b2.capability.control-service-load-resources`) | Performance and resource control | External service integration |

## Карта оставшихся пробелов

| Пробел | Масштаб | Последствие |
|---|---:|---|
| Outcomes без любой принятой связи | 11 / 69 | Evolution L1 и десять L4: Error, Identity, Abuse, Architecture, Cache, Idempotency, External Integration, Workflow, Verification, Delivery. Delivery L1 впервые покрыт S11; все exact IDs представлены пустыми строками канонического реестра. |
| Outcomes только с `probe` | 7 | L4 reasoning можно обсудить, но нет execution/adoption evidence; module completion из этого не следует. |
| Модули без собственных содержательных artifacts | 0 / 10 | Breadth-pass и пятижанровый content flow — 10/10 после G19; proficiency не следует из наличия материалов. |
| ImplementationReference | 0 | Двенадцать project specs не имеют принятой самостоятельной реализации; это ожидаемый долг, а не дефект спецификаций. |
| Module gate decisions | 0 явных | Полный набор жанров и несколько flow не заменяют отдельного решения о завершённости module scope. |
| External prerequisites | только baseline/conditional specifications | B3 readiness S15 подтверждена локально, а B5 признан неприменимым к однопроцессной гарантии. B6/B7 readiness S11 подтверждена только для его локального rollout. A3/B5 readiness Pricing подтверждена только для M1.8.17. B1/A3 readiness S01 подтверждена только для его in-process сборки. Для callback/SSRF, aggregate quota/rate и L4-пакетов нужны собственные применимые readiness records owner tracks; выдумывать placeholder capability IDs нельзя. |

Architecture L4, Verification L4, External Services L4 и Cache L4 не имеют ни одной принятой relationship. M1.8.13 не заявляет Transaction, Load Control, Identity, Verification, B3 или B5 outcomes: принятые contracts и Gate 0 не переносят coverage за границу cache action. S15 также не закрывает distributed cache migration, callback/SSRF или aggregate quota/rate.

Семь `probe-only` остаются теми же exact IDs:

- `b2.level-outcome.manage-service-resource-lifecycle-l4-establish-service-policy`;
- `b2.level-outcome.design-http-api-contracts-l4-establish-cross-team-conventions`;
- `b2.level-outcome.evolve-api-contracts-l4-lead-cross-team-migration`;
- `b2.level-outcome.control-concurrency-cancellation-l4-establish-runtime-policy`;
- `b2.level-outcome.verify-contract-compatibility-l4-establish-compatibility-process`;
- `b2.level-outcome.diagnose-service-performance-l4-lead-cross-service-analysis`;
- `b2.level-outcome.control-service-load-resources-l4-align-capacity-boundaries`.

Историческая разность M1.8.15: Delivery L1 имеет `explain`, `probe`, `practice` и `assess` D1–D3, поэтому covered вырос с 57 до 58, а `probe-only` не изменился. Delivery L2 раньше имел только C2 `explain`, теперь D4 задаёт собственное `integrate/assess`; Delivery L3 уже имел C5 `integrate/assess`, а D4 проверяет другое действие — подготовленные stop/incident/recovery и измеренные стадии. Это coverage учебных artifacts, не факт выполнения проекта участником.

S11 не добавил Evolution/Compatibility/Verification/B6/B7 relationships. Согласно acceptance G14, aggregate exposure не доказывает полный S1 route/form cross-product, R-old не доказывает доступность заказов, ранее принятых new, а readback общего in-memory state не доказывает durability или process-crash recovery. Эти границы не пересматриваются refresh-пакетом.

## Фазовый переход после M1.8.20

G17 принял первый breadth-pass с собственным входом 10/10 и полным flow 9/10. G18 принял consolidation dossier и выбрал одно действие S01. G19 добавил четыре собственных жанра HTTP Runtime; вместе с R1 learn и supporting C1 это полный десятый маршрут. [Карта HTTP reuse](consolidation/routes-and-reuse.md#http) отличает самостоятельный refactor H3 от заданного дефекта H2, известного handler defect S10 и fan-out R5.

D19 закрыт в content/navigation части, D20 — в content/exercise части; [реестр долга](consolidation/debt-register.md#d19) сохраняет их историю. Исходный и исправленный traces, самостоятельный выбор границы, регрессия, review реализации и возможная ImplementationReference ещё должны появиться у участника. Новый S01 project-spec не подтверждает эти результаты. Trace L3 получает только H1 probe; прежние R3 probe и R5 integrate/assess не удалены и не расширены до production evidence нового slice.

Обычный локальный долг сохраняет Evolution L1, самостоятельное выполнение tracing L1/L2, S12 diagnosis и scope Abuse L2/L3: callback/SSRF и aggregate quota. Их нельзя закрыть суммой outcomes или статусом accepted у задания. Десять пустых L4 и семь probe-only L4 требуют реального применения: владельцев, выполненного этапа adoption/migration, exceptions и обратной связи. Локальная лаборатория не создаёт межкомандный результат.

### Hard DAG и локальная readiness

[Prerequisites](prerequisites.md) дают 19 capabilities, 13 уникальных рёбер Requires и восемь capabilities без internal hard prerequisites; граф ацикличен. HTTP L2 поддержан C4, Architecture L2 — A3/A4, Lifecycle L2 — R4, Tracing L2 — H2/H3, исторический Tracing L3 — R5, Evolution L2/L3 — C4/C5, Verification L2/L3 — V3/V4, Compatibility L2/L3 — C4/C5/V3/V4. Здесь коды A3/A4 обозначают artifacts реестра, а внешний A3 track — отдельного владельца readiness.

External требует Lifecycle; ни одна другая B2 capability не требует External в колонке Requires. Поэтому E3/E4 не открывают новых downstream hard prerequisites. Delivery по-прежнему требует Evolution, Verification и Compatibility, но сама не является hard prerequisite другой B2 capability. Related и external specifications исключены из топологической сортировки. Все прежние internal readiness основания сохранены; итог blocked 0 не обещает готовую среду для любого будущего пакета.

[Gate 0 M1.8.17](../../../governance/work-packages/M1.8.17-external-integration-s08-slice.md) и [профиль A G16](../../../governance/reviews/M1.8.17-G16-external-integration-glm.md) подтверждают только выбранную loopback Pricing/Quote модель. Acceptance фиксирует 82 входящих проверки, 79 attempts/receipts, false absence 27/27 → 0/27 и recovery 6/6. Это принятое evidence, runtime-прогоны M1.8.21 не выполнялись. Trusted configured target не доказывает DNS/redirect/SSRF protection; read-only и one-attempt не доказывают B5 proficiency или distributed retry semantics. Timeout не означает remote cancellation; response release подтверждён косвенно, connect-refused не входит в основную матрицу. Эти ограничения приняты G16, а не являются новыми findings.

Профиль B G16 не выполнялся по явному однопрофильному исключению; learning/editorial risk assessment оркестратора не является вторым независимым review. Исключение не переносится на следующий gate. S05/S14-cost, S07/S09, S15 и S11 сохраняют только свои readiness boundaries; в частности, cache-store S15 не подтверждает aggregate quota coordination, а B6/B7 S11 не подтверждает multi-team rollout.

[G19](../../../governance/reviews/M1.8.20-G19-http-runtime-acceptance.md) сохраняет узкую S01-модель: status/body корректны, дефект проявляется потерей обязательного диагностического X-Request-ID. Принятый независимый probe — 369 операций; он не доказывает network behavior, worker reuse, crash recovery или production Trace L3. Dependency-exit на error path связывается с finally вокруг yield; отсутствие checkpoint сначала требует проверки instrumentation. Recovery — три повтора по 20 последовательных операций, всего 60. Эти ограничения и однопрофильное исключение G19 не пересматриваются; профиль B для review M1.8.21 не отменён.

## Сравнение следующей фазы

Сравнение использует [актуальный долг](consolidation/debt-register.md), [десять gate cards](consolidation/module-gates.md) и обе [RoleViews](role-requirements.md). Результат выбора — рекомендация оркестратору, без нового задания или начисления coverage.

| Вариант | Конкретный результат и ценность | Readiness и недостающие основания | Решение |
|---|---|---|---|
| B2 completion-tail D21: один S12 experiment | Различить причины нелинейного p99 при стабильной median; diagnosis L3 обязателен обеим ролям | Нужны distinct mechanism относительно R4/R5, самостоятельность tracing и B7 measurement readiness. S01 даёт L2 задание, но не исполненную production reconstruction; эти входные условия ещё не подтверждены | Не выбран сейчас. D21 сохраняет trigger, новый pool-tuning slice не обоснован |
| Подготовка HTTP Runtime module gate | Свести tracing/lifecycle/cancellation результаты к одному решению по scope; жанры уже полны | H3 и R5 остаются заданиями, нет независимо проверенных реализаций. S01 не закрывает production Trace L3, весь S02 и conditional Lifecycle/Cancellation L4. Карточка не близка к решению только от появления H0–H3 | Не выбран: сначала реальные работы по D20/D26; новый gate dossier не создаст их |
| B3 boundary intake: application transaction / store isolation | Уточнить один будущий пакет store-level действия, важного обеим depth-ролям; не переносить локальную B2 readiness на B3 proficiency | Есть принятый B3 track/cluster scope, B2 ownership и явная disposition долга. Для документального intake runtime Gate 0 не нужен; конкретная среда и readiness будут требованием будущего execution package | **Выбран единственный следующий вариант** |

Callback D22 и quota D23 остаются after-readiness: их DNS/redirect либо atomic budget/coordination среды не подтверждены S01/Pricing/cache. Evolution L1 D01 не выбран ради увеличения 58/69: отдельный заданный шаг относительно C4 не установлен. L4 D02–D18 требует реальных участников и выполненного этапа; новый текст их не заменит. Эти долги не исчезают при переходе к B3.

## Decision brief: один B3 boundary intake

### Центральный результат и закрываемый риск

Рекомендуется один документальный intake на границе **application transaction B2 и store isolation B3**. Участнику уже доступны B2 S07/S15, но их локальные проверки PostgreSQL/cache не означают самостоятельного владения устройством store. Следующий управленческий результат — reviewable граница одного будущего store-level действия из существующего [B3 transactions/concurrency cluster](../catalog/b3-transactional-data.md), его наблюдаемое evidence и условия допуска. Это закрывает риск неявного переноса B2 application ownership и локальной B3 readiness на новый трек.

### Prerequisites, scope и non-goals

Основания: принятые scope B3 и B2, [prerequisites](prerequisites.md), breadth и пятижанровый content flow B2 10/10, сохранённые D01–D27. До запуска оркестратор назначает владельца и точный Ownership отдельного bounded intake. Это предложение не выполняет такое назначение.

В scope одного intake: разграничить application operation/side effects и store isolation/concurrency; выбрать одно проверяемое store-level действие без создания semantic IDs; указать необходимый baseline, механизм будущего failure/control evidence и вопросы владельцам. B2 S07 может дать пример потребности, но не заимствованное B3 proficiency. Для самого intake подтверждения runtime не требуются; проектирование зависимого учебного исполнения начинается только после собственного readiness gate.

Non-goals: полный B3 blueprint или курс, новые capabilities/outcomes/coverage, учебные материалы и реализации, SQL/store tuning как второе действие, распределённая consistency B5, platform B6, reliability discipline B7, фиктивное завершение B2 или L4. В M1.8.21 никакие файлы B3 и program status не меняются.

### Проверяемый exit trigger

Intake завершён для передачи, когда есть один документ в review с одной границей действия, владельцем concern, сопоставлением B2/B3 non-goals, readiness-условиями и наблюдаемым результатом будущей проверки; нет неразрешённого ownership-конфликта. Оркестратор после независимого review принимает либо возвращает этот конкретный intake. Его принятие не означает acceptance будущего content package. Автоматического нового B2 consolidation-цикла нет: возврат к B2 запускает конкретный trigger долга, например предъявленная самостоятельная реализация D26 или подтверждённый отдельный механизм/readiness D21.

## Open questions и известный долг

1. Блокирующих вопросов внутри Ownership M1.8.21 нет. Выбор B3 intake, его назначение и acceptance остаются решениями оркестратора.
2. Все 10 модулей остаются partial и not-ready-for-gate. Общий дефицит — самостоятельные проекты с исходными наблюдениями и независимым review; 12 заданий не являются 12 выполненными работами.
3. D19 content/navigation и D20 content/exercise закрыты G19; незакрытые execution-условия D20/D26 и scope/L4 ограничения карточек сохранены. D21–D25 не получают readiness от S01.
4. Один Evolution L1, десять uncovered L4 и семь probe-only L4 остаются в аудите. Реальный adoption/migration нельзя заменить дополнительным текстом.
5. Однопрофильные исключения G18/G19 сохранены как исторические решения; они не разрешают пропускать профиль B следующего независимого review.

## Воспроизводимость подсчёта и self-check

Пересчёт 2026-09-09 выполнен отдельно от старого плана по front matter всех `curriculum/tracks/b2/slices/**/*.md` с `status: accepted`. Каталог `level-outcomes.md` даёт ровно 69 ID, `capabilities.md` — 19 ID, `modules.md` — 10 `Develops` memberships. Каждая YAML-связь проверена как `(artifact, target, role)`; внутри artifact повторов `(target, role)` нет. Capability references отделены до вычисления covered/probe-only.

| Slice / локальные коды | Artifacts | Capability reference | Outcome relationships |
|---|---:|---:|---:|
| S03 / C0–C5 | 6 | 4 | 39 |
| Runtime S08 / R0–R5 | 6 | 5 | 56 |
| S06 / A0–A4 | 5 | 2 | 24 |
| S10 / V0–V4 | 5 | 2 | 23 |
| S07 / T0–T4 | 5 | 2 | 20 |
| S09 / W0–W4 | 5 | 1 | 10 |
| S05 / I0–I4 | 5 | 1 | 14 |
| Operation-cost S14 / O0–O4 | 5 | 1 | 12 |
| S15 / K0–K4 | 5 | 1 | 10 |
| S11 / D0–D4 | 5 | 1 | 12 |
| External S08 / E0–E4 | 5 | 1 | 8 |
| HTTP Runtime S01 / H0–H3 | 4 | 1 | 9 |
| Итого | 61 | 22 | 237 |

Контроль по ролям: `reference 22 / explain 55 / probe 60 / practice 30 / integrate 31 / assess 61`, сумма 259. Первые 57 artifacts дают прежние 249 = 21 + 228; их historical relationships сохранены. Дельта M1.8.20 — `reference 1 / explain 0 / probe 3 / practice 2 / integrate 1 / assess 3`, сумма 10. Девять outcome-level links направлены только в Trace L1–L3; разность covered множеств пуста. Все 10 memberships независимо пересчитаны по Develops, все модули имеют собственные пять жанров. Состояния 0/10/0/0 сохранены по определению состояния и отсутствию module-gate decisions.

Для повторения нужен Python с PyYAML; код ниже выполняется из корня blueprint и ничего не записывает. Он считает набор по YAML, а не по таблице плана.

```python
from pathlib import Path
from collections import defaultdict
import re
import yaml

base = Path("curriculum/tracks/b2")
catalog = (base / "level-outcomes.md").read_text(encoding="utf-8-sig")
ids = re.findall(r"^\| `(b2\.level-outcome\.[^`]+)`", catalog, re.M)
assert len(ids) == len(set(ids)) == 69
roles = defaultdict(set)
artifacts = references = outcome_links = 0
previous = set()
for path in (base / "slices").rglob("*.md"):
    meta = yaml.safe_load(path.read_text(encoding="utf-8-sig").split("---", 2)[1])
    if meta["status"] != "accepted":
        continue
    artifacts += 1
    pairs = [(x["target"], x["role"]) for x in meta["coverage"]]
    assert len(pairs) == len(set(pairs)), path
    for target, role in pairs:
        if target.startswith("b2.capability."):
            assert role == "reference"
            references += 1
        else:
            assert target in ids, (path, target)
            outcome_links += 1
            roles[target].add(role)
            if "request-context-loss-diagnosis" not in path.parts:
                previous.add(target)
print(artifacts, references + outcome_links, references, outcome_links)
print(len(roles), len(set(ids) - roles.keys()))
print("new unique", sorted(set(roles) - previous))
print(sorted(target for target in ids if roles.get(target) == {"probe"}))
```

Механическая самопроверка M1.8.21: YAML шести изменённых документов и 61 accepted artifact разобран; registry и все 69 строк outcome audit сверены с exact target/role; memberships проверены по Develops. Hard DAG строится только по Requires, без related, external context и rationale: 19 узлов, 13 рёбер, восемь корней, циклов нет. Локальные ссылки/anchors, Markdown tables, fences, реальные details tags, trailing whitespace и conflict markers проверены перед Handoff. Runtime G19 не повторяется; его accepted evidence используется с исходными ограничениями.

Ownership контролируется pre/post SHA-256 всего набора файлов Study, включая набор путей; разрешены только этот план и пять файлов consolidation из M1.8.21. Авторский pre-snapshot и исходные версии шести файлов сохранены в системном temp для проверки diff. Это доказательство текущего авторского прохода, не независимое восстановление более раннего состояния; Git root отсутствует. Точные итоги сравнения передаются в Handoff.

## Рекомендуемый scope независимого review

- Профиль A: независимо пересчитать 61/259 = 22 + 237, роли 22/55/60/30/31/61, 58 covered, 11 uncovered, семь exact probe-only; сверить 61 registry row и 69 outcome rows с YAML, H0–H3 и сохранность прежних 57/249.
- Профиль A: проверить все 10 memberships и states 0/10/0/0, Requires DAG 13/8, no-new-coverage/semantic IDs и Ownership шести файлов; отдельно отсутствие ImplementationReference и module-gate decisions.
- Профиль B: пройти оба ролевых входа к HTTP learn → interview → kata → project-spec, различить own/supporting и content/proficiency; проверить новую readiness-карточку H3 и историю D19/D20.
- Оба профиля: повторно оценить десять gate cards, конкретный общий execution blocker, external readiness и conditional L4; сравнить D21, HTTP gate preparation и B3 intake, boundedness выбора и exit trigger.
- Сохранить узкую G19 in-process границу, только H1 probe для Trace L3, отсутствие автоматического переноса однопрофильного исключения. Проверить YAML, links/anchors и Markdown hygiene; результат M1.8.21 остаётся review, не acceptance.
