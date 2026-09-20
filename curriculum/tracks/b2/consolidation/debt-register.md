---
id: b2.plan.consolidation-debt-register
kind: plan
title: B2 — реестр оставшихся действий и ограничений
owner_track: b2
status: accepted
updated: 2026-09-19
language: ru
---

# Реестр оставшихся действий и ограничений

После прохождения материала инженер может обнаружить разные препятствия: не хватает задания, исполненного опыта, подходящей среды или решения по совокупности результатов. Их нельзя закрывать одинаково. Этот реестр помогает оркестратору выделить один ограниченный пакет, а участнику — понять, какого подтверждения пока нет.

Основание — [G17 acceptance](../../../../governance/reviews/M1.8.18-G17-b2-breadth-pass-acceptance.md), [resolution](../../../../governance/reviews/M1.8.18-G17-b2-breadth-pass-resolution.md), [канонический outcome audit](../module-delivery-plan.md) и задания из [карты маршрутов](routes-and-reuse.md). На snapshot 2026-09-08 есть 11 uncovered и семь probe-only. Ниже сохранены долги и история закрытых content-частей D19/D20 по [G19](../../../../governance/reviews/M1.8.20-G19-http-runtime-acceptance.md); полный реестр 69 exact outcomes остаётся в delivery plan. Новых outcome IDs и semantic relationships здесь нет.

## Правила учёта

У каждой записи один устойчивый локальный ID D01–D27, одна категория и одна текущая disposition. Закрытие части фиксируется отдельно от остаточного условия, а запись не удаляется. Shared concern записан один раз у primary module; ссылки других модулей не создают дополнительные долги. Например, Cache L4 учитывается только в D06, даже если его результат полезен нескольким сервисам.

**Evidence** здесь означает наблюдаемый результат деятельности; если указано только задание или probe, это прямо названо. **Proficiency** требует проверки работы участника; **readiness** разрешает начать конкретную работу; **module gate** — отдельное решение; **ImplementationReference** — ссылка после выполнения и review. [Общие определения](README.md#terms) применяются ко всем записям.

Dispositions задают способ обращения с долгом, не автоматическое разрешение authoring:

- `closed-content` — content/navigation действие принято; исполнение участником и gate учитываются отдельно, proficiency не заявляется;
- `candidate-now` — есть конкретное неповторяющееся действие для рассмотрения сейчас, с собственной проверкой readiness до исполнения;
- `after-readiness` — зависимая работа ожидает конкретных входных условий;
- `requires-real-adoption` — обязательный для одной или обеих ролей L4 требует реальных участников и результата;
- `conditional-specialization` — L4 выбирается по ответственности; при выборе всё равно нужны реальные adoption/migration;
- `accepted-limitation` — ограничение уже явно удерживается принятым snapshot; gap остаётся открытым, новый пакет не обоснован одним его наличием.

«Backend» и «Architecture» ниже означают две [B2 RoleViews](../role-requirements.md). Число строк не является severity или приоритетом. Отсутствие роли у L4 не уменьшает важности соответствующего обязательного L3.

## Одиннадцать outcomes без принятой связи

<a id="outcome-debt"></a>

Эти 11 записей соответствуют ровно одному Evolution L1 и десяти L4 из [карты пробелов](../module-delivery-plan.md#карта-оставшихся-пробелов). Для L4 отсутствие связи и отсутствие реального применения отражены одной записью, а не двумя долгами. Условие закрытия включает проверяемый результат, но его принятие и изменение канонического аудита остаются отдельной работой.

### D01 — заданное additive изменение API

<a id="d01"></a>

- **Категория / владелец:** uncovered outcome; Evolvable API Contracts, Evolution L1.
- **Роли:** Backend и Architecture — нижний уровень пути к обязательной Evolution L4; L2 kata не становится заданным L1 действием автоматически.
- **Сейчас / не хватает:** [S03 kata](../slices/evolvable-api-contracts/kata/compatible-delivery-contract-change.md) требует самостоятельного выбора L2; отдельного принятого L1 результата нет в [Evolution audit](../module-delivery-plan.md#api-contracts-and-evolution).
- **Закрытие:** отдельное принятое задание на применение заданного additive change с old/new checks и проверенным исполнением; не переименование существующей kata.
- **Trigger:** найден действительно иной заданный шаг для начинающего участника, который не повторяет самостоятельное S03 изменение.
- **Disposition:** `accepted-limitation`.

### D02 — общее соглашение публичных ошибок

<a id="d02"></a>

- **Категория / владелец:** uncovered outcome; Evolvable API Contracts, Error L4.
- **Роли:** Backend — дополнительная ответственность за conventions; Architecture — conditional quality enablement. Service-level L3 остаётся обязательным.
- **Сейчас / не хватает:** [S03 project](../slices/evolvable-api-contracts/project-spec/evolvable-orders-api.md) задаёт унификацию одного сервиса; нет принятой L4 связи и применения общего error convention несколькими consumers/producers.
- **Закрытие:** исполненная миграция соглашения с taxonomy, security limits, исключениями и feedback нескольких участников по [Error outcome](../level-outcomes.md#b2capabilitydesign-validation-error-contracts).
- **Trigger:** реальная повторяющаяся межсервисная ошибка и владельцы согласовали один migration stage.
- **Disposition:** `conditional-specialization`.

### D03 — миграция технической access-control policy

<a id="d03"></a>

- **Категория / владелец:** uncovered outcome; Identity and API Security Boundaries, Identity L4.
- **Роли:** Backend — при cross-service security ownership; Architecture — conditional API security.
- **Сейчас / не хватает:** [tenant-safe project](../slices/tenant-scoped-orders-authorization/project-spec/tenant-safe-orders-read-api.md) ограничен одним сервисом; нет завершённой межсервисной policy migration.
- **Закрытие:** проверенный этап с trust boundaries, propagation, exceptions и audit feedback вместе с security/platform owners по [Identity L4](../level-outcomes.md#b2capabilityintegrate-identity-access-control).
- **Trigger:** появились реальные сервисы и владельцы общего изменения access control.
- **Disposition:** `conditional-specialization`.

### D04 — применённые abuse defaults нескольких команд

<a id="d04"></a>

- **Категория / владелец:** uncovered outcome; Identity and API Security Boundaries, Abuse L4.
- **Роли:** Backend — при владении общими controls; Architecture — conditional API security.
- **Сейчас / не хватает:** [cost project](../slices/cost-bounded-orders-export/project-spec/cost-bounded-orders-export-api.md) задаёт одну операцию; нет внедрения defaults в нескольких сервисах.
- **Закрытие:** реальное применение controls, зарегистрированные false positives, bypass attempts, exceptions и operational feedback по [Abuse L4](../level-outcomes.md#b2capabilityenforce-api-security-abuse-controls).
- **Trigger:** повторяющийся abuse concern нескольких владельцев и bounded adoption stage; локальные callback/quota задачи остаются D22/D23.
- **Disposition:** `conditional-specialization`.

### D05 — применимые архитектурные conventions

<a id="d05"></a>

- **Категория / владелец:** uncovered outcome; Service Architecture, Architecture L4.
- **Роли:** Backend — дополнительная межсервисная ответственность; Architecture — обязательный L4.
- **Сейчас / не хватает:** [S06 project](../slices/service-architecture-boundaries/project-spec/order-cancellation-policy-service.md) проверяет повторное изменение одного сервиса; нет применения conventions несколькими use cases.
- **Закрытие:** реальные сервисные контексты используют conventions, фиксируют exceptions и обратную связь; показано, что соглашение не стало обязательным framework, согласно [Architecture outcome](../level-outcomes.md#b2capabilitydesign-service-architecture).
- **Trigger:** названы владельцы нескольких сервисов и один проверяемый этап adoption.
- **Disposition:** `requires-real-adoption`.

### D06 — миграция shared cache convention

<a id="d06"></a>

- **Категория / владелец:** uncovered outcome; Transactional Persistence Integration, Cache L4.
- **Роли:** Backend — при shared-cache migration; Architecture — conditional data/integration.
- **Сейчас / не хватает:** [S15 project](../slices/tenant-scoped-orders-cache/project-spec/resilient-orders-summary-cache.md) — один worker; нет mixed-version миграции между сервисами.
- **Закрытие:** завершён реальный stage key/invalidation convention, проверены mixed versions, load shift, rollback/flush risk и production feedback по [Cache L4](../level-outcomes.md#b2capabilityintegrate-application-caching).
- **Trigger:** фактические владельцы shared keys согласовали изменение; пройдена применимая B3/B5 readiness.
- **Disposition:** `conditional-specialization`.

### D07 — согласованная межсервисная idempotency

<a id="d07"></a>

- **Категория / владелец:** uncovered outcome; Evolvable API Contracts, Idempotency L4. Persistence и Workflow используют ту же запись.
- **Роли:** Backend — при общем operation contract; Architecture — conditional data/integration.
- **Сейчас / не хватает:** [S07 project](../slices/transactional-orders-operation/project-spec/resilient-order-confirmation.md) проверяет одну command; нет adoption общего identity/result/conflict/expiry договора несколькими producers/consumers.
- **Закрытие:** совместимые semantics, проверенный migration/adoption plan и фактическое применение в реальном межкомандном этапе с exceptions/feedback по [Idempotency L4 и guardrails](../level-outcomes.md#b2capabilitydesign-idempotent-service-operations).
- **Trigger:** есть конфликтующие договоры реальных участников и согласован один этап перехода.
- **Disposition:** `conditional-specialization`.

### D08 — техническая политика внешних интеграций

<a id="d08"></a>

- **Категория / владелец:** uncovered outcome; External Service Integration, External L4.
- **Роли:** Backend — при integration defaults ownership; Architecture — conditional runtime/platform.
- **Сейчас / не хватает:** [Pricing project](../slices/truthful-pricing-client-boundary/project-spec/integrate-one-pricing-operation.md) L2 и [fan-out project](../slices/runtime-concurrency-lifecycle/project-spec/resilient-fanout-service.md) L3 не проверяют policy нескольких команд.
- **Закрытие:** реальные integration defaults с evidence, exceptions и исполненным migration/adoption stage сохраняют domain-specific failure semantics по [External L4](../level-outcomes.md#b2capabilityintegrate-external-services).
- **Trigger:** реальные владельцы интеграций выделили одно общее изменение с обратной связью.
- **Disposition:** `conditional-specialization`.

### D09 — межкомандная миграция workflow

<a id="d09"></a>

- **Категория / владелец:** uncovered outcome; Background and Message Workflows, Workflow L4.
- **Роли:** Backend — при migration ownership; Architecture — conditional data/integration.
- **Сейчас / не хватает:** [S09 project](../slices/recoverable-order-confirmed-consumer/project-spec/resilient-fulfillment-consumer.md) — один consumer; нет выполненного stage между командами.
- **Закрытие:** проверены реальный producer/consumer sequencing, compatibility и recovery, учтён feedback завершённого этапа по [Workflow L4](../level-outcomes.md#b2capabilitydesign-asynchronous-workflows).
- **Trigger:** названы workflow owners, версии и один исполнимый migration stage с B5 readiness.
- **Disposition:** `conditional-specialization`.

### D10 — межкомандные требования к проверке сервисов

<a id="d10"></a>

- **Категория / владелец:** uncovered outcome; Service Verification, Verification L4.
- **Роли:** Backend — при общих release evidence expectations; Architecture — conditional quality enablement.
- **Сейчас / не хватает:** [S10 portfolio](../slices/risk-based-service-verification/project-spec/orders-verification-portfolio.md) оценивает один сервис; нет использования общего подхода командами в release decisions.
- **Закрытие:** risk-based expectations допускают разные стеки и реально использованы несколькими командами, с exceptions/feedback по [Verification L4](../level-outcomes.md#b2capabilityverify-service-behavior).
- **Trigger:** реальная повторяющаяся потеря evidence между командами и ограниченный adoption stage.
- **Disposition:** `conditional-specialization`.

### D11 — выполненный межкомандный rollout

<a id="d11"></a>

- **Категория / владелец:** uncovered outcome; Safe Service Evolution, Delivery L4.
- **Роли:** обязательный L4 для Backend и Architecture.
- **Сейчас / не хватает:** [S11 project](../slices/safe-orders-service-rollout/project-spec/evidence-driven-orders-rollout.md) задаёт локальный выпуск; нет реального rollout нескольких сервисов/команд.
- **Закрытие:** один технический stage с dependencies, stop conditions, communication и recovery отрепетирован и выполнен, результаты приняты владельцами согласно [Delivery L4](../level-outcomes.md#b2capabilitydeliver-service-changes-safely).
- **Trigger:** реальные команды, service owners, условия B5/B6/B7 и граница C1 участия названы до запуска.
- **Disposition:** `requires-real-adoption`.

## Семь outcomes только с interview probe

<a id="probe-debt"></a>

Точный набор сохранён в [каноническом аудите](../module-delivery-plan.md#карта-оставшихся-пробелов). Эти записи не входят в предыдущие 11. Пробел — отсутствие execution/adoption; ещё один interview не закрывает его.

### D12 — lifecycle policy нескольких сервисов

<a id="d12"></a>

- **Категория / владелец:** probe-only; HTTP Service Runtime, Lifecycle L4.
- **Роли:** Backend — при shared resource policy; Architecture — conditional runtime/platform.
- **Сейчас / не хватает:** [runtime interview](../slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md) только исследует рассуждение; нет применённых defaults минимум в двух контекстах.
- **Закрытие:** реальное применение с exceptions, migration и production feedback, изменяющим policy, по [Lifecycle L4](../level-outcomes.md#b2capabilitymanage-service-resource-lifecycle).
- **Trigger:** владельцы нескольких сервисов/библиотек готовы проверить один общий default.
- **Disposition:** `conditional-specialization`.

### D13 — межкомандные HTTP conventions

<a id="d13"></a>

- **Категория / владелец:** probe-only; Evolvable API Contracts, HTTP L4.
- **Роли:** Backend — дополнительная ответственность; Architecture — обязательный L4.
- **Сейчас / не хватает:** [API interview](../slices/evolvable-api-contracts/interview/api-contract-evolution.md); нет adoption conventions несколькими командами.
- **Закрытие:** conventions решают повторяющуюся проблему, применены реально, имеют versioning, exceptions и adoption evidence по [HTTP L4](../level-outcomes.md#b2capabilitydesign-http-api-contracts).
- **Trigger:** реальные API owners согласовали одну convention и наблюдаемый этап применения.
- **Disposition:** `requires-real-adoption`.

### D14 — миграция API между командами

<a id="d14"></a>

- **Категория / владелец:** probe-only; Evolvable API Contracts, Evolution L4. Safe Evolution использует этот же долг.
- **Роли:** обязательный L4 для Backend и Architecture.
- **Сейчас / не хватает:** [API interview](../slices/evolvable-api-contracts/interview/api-contract-evolution.md); локальные клиенты проекта не подтверждают реальную межкомандную migration.
- **Закрытие:** согласованные sequencing/ownership нескольких producers/consumers привели к цели без незапланированного нарушения клиентов по [Evolution L4](../level-outcomes.md#b2capabilityevolve-api-contracts).
- **Trigger:** реальная migration с названными участниками и bounded stage; отличается от D11 действием над договором клиентов, а не только выпуском binary.
- **Disposition:** `requires-real-adoption`.

### D15 — runtime policy нескольких сервисов

<a id="d15"></a>

- **Категория / владелец:** probe-only; External Service Integration, Cancellation L4.
- **Роли:** Backend — при policy ownership; Architecture — conditional runtime/platform.
- **Сейчас / не хватает:** [runtime interview](../slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md); локальное завершение задач не доказывает end-to-end budgets цепочки.
- **Закрытие:** реальные deadline/cancellation/concurrency defaults применены, ownership непротиворечив, rollout не создаёт каскадных отказов; exceptions/feedback сохранены по [Cancellation L4](../level-outcomes.md#b2capabilitycontrol-concurrency-cancellation).
- **Trigger:** есть реальная цепочка сервисов, владельцы и согласованный stage внедрения.
- **Disposition:** `conditional-specialization`.

### D16 — применённый compatibility process

<a id="d16"></a>

- **Категория / владелец:** probe-only; Service Verification, Compatibility L4.
- **Роли:** Backend — при cross-team process ownership; Architecture — обязательный L4.
- **Сейчас / не хватает:** [API interview](../slices/evolvable-api-contracts/interview/api-contract-evolution.md); нет внедрённого механизма обнаружения breaking changes между командами.
- **Закрытие:** ownership, exceptions, stale consumers и enforcement path действуют в реальном процессе, escape rate отслеживается по [Compatibility L4](../level-outcomes.md#b2capabilityverify-contract-compatibility).
- **Trigger:** реальные consumers/producers готовы применить один механизм до release и собрать обратную связь.
- **Disposition:** `requires-real-adoption`.

### D17 — анализ bottleneck через несколько сервисов

<a id="d17"></a>

- **Категория / владелец:** probe-only; Performance and Resource Control, Performance L4.
- **Роли:** Backend — при межсервисной диагностике; Architecture — conditional runtime/platform.
- **Сейчас / не хватает:** [runtime interview](../slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md); нет реального совместного исследования нескольких сервисов/команд.
- **Закрытие:** общая measurement model локализовала constraint; исполненные решения учли shifting bottleneck и cost, есть feedback владельцев по [Performance L4](../level-outcomes.md#b2capabilitydiagnose-service-performance).
- **Trigger:** реальная cross-service деградация и доступ к измерениям/владельцам; локальный S12 учитывается отдельно в D21.
- **Disposition:** `conditional-specialization`.

### D18 — согласованные capacity boundaries

<a id="d18"></a>

- **Категория / владелец:** probe-only; Performance and Resource Control, Load L4.
- **Роли:** Backend — при ответственности за цепочку; Architecture — conditional runtime/platform.
- **Сейчас / не хватает:** [runtime interview](../slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md); нет совместно применённых limits/budgets цепочки.
- **Закрытие:** реальные limits и timeouts не усиливают overload, определены ownership/capacity evidence и проверен результат внедрения с feedback по [Load L4](../level-outcomes.md#b2capabilitycontrol-service-load-resources).
- **Trigger:** service owners и применимая B7 readiness позволяют выполнить одно изменение границы мощности.
- **Disposition:** `conditional-specialization`.

## Локальные действия и условия допуска

### D19 — собственный жанровый маршрут HTTP Runtime

<a id="d19"></a>

- **Категория / владелец:** navigation/genre gap; HTTP Service Runtime.
- **Роли:** обеим нужен request/runtime baseline; собственный маршрут теперь доступен через все пять жанров.
- **Audit trail:** G18 принял дефицит index/interview/kata/project-spec и выбрал S01; [G19](../../../../governance/reviews/M1.8.20-G19-http-runtime-acceptance.md) принял четыре материала. [HTTP route](routes-and-reuse.md#http) связывает собственные index/interview/kata/project-spec с собственным R1 learn и supporting C1.
- **Content/navigation: closed.** Условие закрытия выполнено принятым M1.8.20; повторный content package для этих жанров не нужен.
- **Остаточное условие:** исполнение проекта участником, независимое review и возможная ImplementationReference остаются в D20/D26; module decision — D27. Это не новый navigation gap.
- **Trigger:** пересмотреть только при конкретном дефекте навигации; наличие десяти partial не переоткрывает D19.
- **Disposition:** `closed-content`.

### D20 — самостоятельная локализация request-state failure

<a id="d20"></a>

- **Категория / владелец:** execution gap; HTTP Service Runtime, tracing L1/L2 и граница перехода к L3.
- **Роли:** обеим нужна самостоятельная диагностика пути; Performance использует tracing как prerequisite.
- **Audit trail:** G18 зафиксировал отсутствие собственного задания и исполнения. G19 принял [kata L1/L2](../slices/request-context-loss-diagnosis/kata/localize-context-loss.md) и [проект L2](../slices/request-context-loss-diagnosis/project-spec/preserve-context-through-refactor.md); **content/exercise: closed** принятым M1.8.20. C1/S10/R5 сохраняют прежние supporting роли; это не повтор их заданий.
- **Не закрыто:** участник ещё не предъявил самостоятельный refactor, raw traces, причинную регрессию, изоляцию и recovery, независимое review реализации и возможную ImplementationReference по D26. Авторский G19 probe не является его результатом. Trace L3 в S01 остаётся только interview probe, production reconstruction не засчитана.
- **Закрытие execution-условия:** проверены исходные гипотезы, первая потеря, исправление без обхода pipeline, сохранность публичного договора и полная матрица проекта; затем обработаны findings независимого review. Регистрация ссылки следует после исполнения и review, module gate рассматривается отдельно.
- **Trigger:** участник начинает уже принятый [S01 проект](implementation-readiness.md#http) со своей B1/A3 readiness; новый content package не требуется.
- **Disposition:** `after-readiness`.

### D21 — отдельная диагностика S12

<a id="d21"></a>

- **Категория / владелец:** scope gap; Performance and Resource Control.
- **Роли:** diagnosis L3 обязателен Backend и Architecture.
- **Сейчас / не хватает:** [R4/R5 route](routes-and-reuse.md#performance) центрирован на S08 pool/cancellation; [S12](../scenarios.md) — стабильная median при нелинейном p99 — не имеет отдельного раскрытого action.
- **Закрытие:** принятое неповторяющееся S12 задание и исполненный experiment с конкурирующими гипотезами, measurement/profile, причинностью и проверкой нового bottleneck; не подбор pool size по памяти.
- **Trigger:** обоснован отдельный механизм S12, проверена самостоятельность tracing и применимая B7 measurement readiness; S01 content уже принят, но его принятие не подтверждает эти readiness-условия. D21 остаётся кандидатом, не назначенным следующим пакетом.
- **Disposition:** `candidate-now`.

### D22 — callback и недоверенный адрес назначения

<a id="d22"></a>

- **Категория / владелец:** scope gap; Identity and API Security Boundaries, Abuse L2/L3.
- **Роли:** обязательное service abuse действие обеих ролей; текущий cost-only flow неполон для всего scope.
- **Сейчас / не хватает:** [export applicability matrix](../slices/cost-bounded-orders-export/project-spec/cost-bounded-orders-export-api.md#applicability-matrix) не имеет target; [Pricing](../slices/truthful-pricing-client-boundary/README.md) использует trusted URL. Нет проверки callback/SSRF.
- **Закрытие:** один согласованный callback scope сохраняет допустимое назначение, блокирует объявленные bypass/failure paths, подтверждён исполнением на принятом DNS/IP/redirect envelope.
- **Trigger:** выполнен применимый readiness из D25 и ограничен один callback action без egress-platform разработки.
- **Disposition:** `after-readiness`.

### D23 — общий tenant quota/rate budget

<a id="d23"></a>

- **Категория / владелец:** scope gap; Identity and API Security Boundaries, Abuse L2/L3.
- **Роли:** обеим нужна граница adversarial workload; один operation ceiling не ограничивает множество допустимых requests.
- **Сейчас / не хватает:** [cost project](../slices/cost-bounded-orders-export/project-spec/cost-bounded-orders-export-api.md) не имеет shared counter; [Cache project](../slices/tenant-scoped-orders-cache/project-spec/resilient-orders-summary-cache.md) не доказывает atomic budget/expiry.
- **Закрытие:** один общий бюджет при concurrent requests имеет явную identity/window/store-failure semantics, проверенные race и recovery, legitimate use сохранён в заявленной topology.
- **Trigger:** D25 подтверждает B3/B5/B7 applicability и ограниченный один budget; quota не объединяется с callback в один пакет.
- **Disposition:** `after-readiness`.

### D24 — External L3 и предел полного S08

<a id="d24"></a>

- **Категория / владелец:** scope gap; External Service Integration.
- **Роли:** External L3 обязателен обеим; дополнительное L4 учитывается только D08.
- **Сейчас / не хватает:** [Pricing E0–E4](../slices/truthful-pricing-client-boundary/README.md) L1/L2 принят; External L3 уже имеет R2/R3/R5 связи в [audit](../module-delivery-plan.md#external-integration-and-runtime-control). Нет принятого завершения полного S08 и зарегистрированного исполнения участника.
- **Закрытие:** самостоятельное failure/degradation evidence R5 проверено в своём scope, весь заявляемый S08 сопоставлен с ним и передан на отдельное рассмотрение module gate; новая спецификация нужна только для установленного distinct gap. Уже принятое gate decision не является входным условием закрытия этого scope gap.
- **Trigger:** предъявлен результат R5 либо найден конкретный недостающий L3 механизм, отличный от существующего fan-out задания.
- **Disposition:** `accepted-limitation`.

### D25 — входная готовность будущих расширений

<a id="d25"></a>

- **Категория / владелец:** external readiness; B2 package intake с A3/B3/B5/B6/B7 owners. Внешние capability IDs не выдумываются.
- **Роли:** обе роли должны отличать допуск к опыту от proficiency соседнего трека.
- **Сейчас / не хватает:** [prerequisites](../prerequisites.md) задают baseline/conditional dependencies; принятые S05, S14-cost, S07/S09, S15, S11 и Pricing подтверждают только собственные среды. Нет переноса readiness на callback, aggregate quota или multi-team L4.
- **Закрытие:** для конкретно выбранного пакета есть scoped readiness record с наблюдениями/ограничениями нужного owner: A3 DNS/IP/redirect для callback; B3 atomicity/expiry/failure, B5 coordination applicability и B7 counters для quota; реальные участники и применимые B5/B6/B7 условия для L4. B1/A3 Gate 0 S01 принят G19 только для его авторской сборки; участник повторяет применимые проверки в своём репозитории. Закрывается допуск выбранного пакета, остальные условия не считаются выполненными.
- **Trigger:** оркестратор выбрал один action и его среду; результат readiness фиксируется до зависимого authoring/execution.
- **Disposition:** `after-readiness`.

### D26 — самостоятельные реализации и ImplementationReference

<a id="d26"></a>

- **Категория / владелец:** implementation reference; участник каждого проекта, B2 registration concern.
- **Роли:** обеим нужны проверяемые результаты деятельности, а не ссылка на project-spec.
- **Сейчас / не хватает:** двенадцать accepted project-spec после G19, ноль зарегистрированных ImplementationReference в текущем accepted-наборе. Нет принятой самостоятельной реализации в рассматриваемом наборе; это ожидаемая стадия, не дефект спецификаций.
- **Закрытие:** для каждого заявляемого проекта выполнены его отдельный репозиторий, воспроизведение, raw evidence, решение и review; затем ссылка регистрируется по установленному процессу. Один реализованный проект не закрывает запись за остальные одиннадцать.
- **Trigger:** участник готов начать выбранный [проектный маршрут](implementation-readiness.md); отсутствие reference не препятствует старту.
- **Disposition:** `after-readiness`.

### D27 — отдельные решения по десяти module gates

<a id="d27"></a>

- **Категория / владелец:** module-gate decision; оркестратор B2.
- **Роли:** обеим нужен ясный предел результата; ролевой L3/L4 и module completion не взаимозаменяемы.
- **Текущее состояние:** [канонический audit](../../../../governance/state/MODULE-STATE.md) зарегистрировал десять отдельных B2 authoring-state решений: восемь модулей закрыты для текущего authoring scope, два остаются partial. Исторические [карточки](module-gates.md) сохранены как rubric пользовательского evidence и superseded как authoring gate.
- **Закрытие authoring-условия:** выполнено 2026-09-19 решением D-080. Готовность учебного пакета отделена от learner execution и proficiency.
- **Trigger повторного открытия:** изменились module scope/capability membership, принят новый deep route либо установлен предметный пробел L1–L3 существующего маршрута.
- **Disposition:** `closed-for-authoring`; запись сохраняет audit trail.

## Проверка полноты и отсутствие двойного счёта

| Категория | Число записей |
|---|---:|
| uncovered outcome | 11 |
| probe-only | 7 |
| execution gap | 1 |
| navigation/genre gap | 1 |
| scope gap | 4 |
| external readiness | 1 |
| implementation reference | 1 |
| module-gate decision | 1 |
| Всего | 27 |

| Disposition | Число записей |
|---|---:|
| candidate-now | 1 |
| closed-content | 1 |
| after-readiness | 6 |
| requires-real-adoption | 5 |
| conditional-specialization | 12 |
| accepted-limitation | 2 |
| Всего | 27 |

D19/D20 сохраняют audit trail одного принятого S01 content-action: D19 navigation и D20 exercise закрыты G19. D20 сохраняет execution-условие, D26 — исполнение/review и регистрацию проектов; это две проекции одного отсутствующего результата, а не два проекта. Таблица категорий считает 27 сохранённых записей, включая закрытую content-часть, а не 27 открытых задач. D22/D23 описывают отсутствующие controls, D25 — допуск к их будущей проверке. D26 описывает реализации, D27 — решения по scope модулей. Эти записи нельзя складывать как «число непокрытых outcomes». Единственная следующая рекомендация дана во [входе досье](README.md); остальные dispositions не являются дополнительными назначениями.

## Самопроверка долга

Закрывает ли новая подробная policy десять пустых и семь probe-only L4?

<details>
<summary>Ответ</summary>

Нет. Она может описать план, но не создать реальное применение и обратную связь. Для выбранного L4 нужны соответствующие владельцы и исполненный этап. Для остальных сохраняется conditional disposition; количество страниц не меняет ни proficiency, ни module-gate решение.

</details>
