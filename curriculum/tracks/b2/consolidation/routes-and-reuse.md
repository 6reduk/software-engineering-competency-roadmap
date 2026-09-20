---
id: b2.plan.consolidation-routes-reuse
kind: plan
title: B2 — маршруты десяти модулей и границы переиспользования
owner_track: b2
status: accepted
updated: 2026-09-09
language: ru
---

# Маршруты десяти модулей

При изменении сервиса часто нужен материал соседнего модуля: проверка контракта помогает выпуску, а lifecycle клиента — интеграции. Но повторное использование материала не завершает соседнюю компетенцию. Эта карта помогает выбрать учебный путь и понять, какой самостоятельный результат он готовит.

Сначала выберите ролевой срез в конце файла, затем карточку модуля. Названия и scope соответствуют [каталогу modules](../modules.md), владельцы действий — [capabilities](../capabilities.md). Порядок обязательных зависимостей задают [prerequisites](../prerequisites.md); рекомендуемый порядок чтения здесь не добавляет рёбер в этот граф. Verification может идти параллельно реализации.

В каждой карточке находится канонический **route status** досье. `Полный пятижанровый flow` означает наличие index → learn → interview → kata → project-spec, а не полноту scope или навык участника. Интервью проверяет рассуждение; kata — ограниченное действие; самостоятельный проект требует исполнения и review. Определения evidence, proficiency, readiness и gate общие с [входом досье](README.md#terms). Snapshot после [G19](../../../../governance/reviews/M1.8.20-G19-http-runtime-acceptance.md) включает S01; прежнее досье принято [G18](../../../../governance/reviews/M1.8.19-G18-b2-consolidation-acceptance.md), текущий refresh остаётся review.

## HTTP Service Runtime — восстановить путь запроса

<a id="http"></a>

**Цель:** найти первую потерю диагностического контекста после refactor и проверить сохранность пути запроса. **Route status: полный пятижанровый flow.** Собственный [index S01](../slices/request-context-loss-diagnosis/README.md) принят G19 вместе с interview/kata/project-spec. Собственный learn — исторический R1 из runtime-slice; C1 остаётся supporting learn другого модуля.

Порядок от объяснения к работе:

1. Learn: supporting [C1 — HTTP execution boundary](../slices/evolvable-api-contracts/learn/http-contract-execution-boundary.md), затем собственный [R1 — request scope и lifecycle](../slices/runtime-concurrency-lifecycle/learn/cancellation-deadlines-resource-lifecycle.md).
2. Собственное [интервью — восстановить путь](../slices/request-context-loss-diagnosis/interview/reconstruct-context-path.md): Trace L1/L2 и только production follow-up probe L3.
3. Собственная [kata — локализовать потерю](../slices/request-context-loss-diagnosis/kata/localize-context-loss.md): заданный путь L1 и первая потеря/регрессия L2.
4. Собственный [project-spec — сохранить контекст через refactor](../slices/request-context-loss-diagnosis/project-spec/preserve-context-through-refactor.md): самостоятельный выбор диагностического значения и границы L2 в отдельном репозитории.

G19 закрыл content/navigation [D19](debt-register.md#d19) и content/exercise [D20](debt-register.md#d20). Сохранены отдельные незакрытые условия исполнения и review; наличие задания не доказывает tracing proficiency. Узкий S01 сохраняет status/body и диагностирует потерю X-Request-ID. Локальная in-process модель не является production Trace L3, сетевым опытом или полным S02.

Supporting [S10 kata](../slices/risk-based-service-verification/kata/detect-orders-error-contract-regression.md) даёт известный handler defect; [runtime interview](../slices/runtime-concurrency-lifecycle/interview/runtime-resource-failure.md), [kata](../slices/runtime-concurrency-lifecycle/kata/stop-orphan-work-and-pool-exhaustion.md) и [fan-out project](../slices/runtime-concurrency-lifecycle/project-spec/resilient-fanout-service.md) посвящены lifecycle/cancellation/pool. Они полезны для resource path и не становятся собственными жанрами S01. Их исторические relationships не изменены.

**Результат участника:** исходные гипотезы, trace первой потери, причинная правка, сохранённый публичный контракт и pipeline, независимая корреляция, concurrent isolation и recovery; resource path оценивается отдельно. Далее — [HTTP gate](module-gates.md#http), [S01 readiness](implementation-readiness.md#http) и supporting [fan-out readiness](implementation-readiness.md#fanout).

## Evolvable API Contracts — изменить API при разных клиентах

<a id="contracts"></a>

**Цель:** провести совместимое изменение и обосновать сохранение либо удаление старого поведения. **Route status: полный пятижанровый flow.** Собственный вход — [Эволюционируемые API-контракты](../slices/evolvable-api-contracts/README.md): index → два learn об исполнении и изменении контракта → interview → kata → project-spec в порядке этого README.

Переиспользуйте [транзакционный S07](../slices/transactional-orders-operation/README.md) для повторяемой command и гонок idempotency, [S10](../slices/risk-based-service-verification/README.md) для клиентских checks и [S11](../slices/safe-orders-service-rollout/README.md) для измеренного выпуска. S07 подтверждает отдельное действие с identity/result и replay при выполнении задания; оно не является новой S03 migration. S11 использует уже заданный контракт, поэтому не заменяет его самостоятельный design. Ни один из этих переходов не устраняет [Evolution L1](debt-register.md#d01) или [L4 migration](debt-register.md#d14).

**Результат участника:** работающие старый и новый клиенты, семантический дефект, не видимый schema diff, и миграционный отчёт с условиями остановки/выхода. Далее — [gate](module-gates.md#contracts) и [проектный старт](implementation-readiness.md#contracts).

## Identity and API Security Boundaries — сохранить границу tenant и стоимости

<a id="identity"></a>

**Цель:** не раскрыть чужой объект и не дать допустимому пользователю обойти предел стоимости операции. **Route status: полный пятижанровый flow.** Есть два собственных входа: [tenant-safe чтение S05](../slices/tenant-scoped-orders-authorization/README.md) и [cost-bounded export S14](../slices/cost-bounded-orders-export/README.md). В каждом порядок index → learn → interview → kata → project-spec; для совместной работы S05 предшествует export как источник trusted context.

Переиспользуйте [HTTP boundary](../slices/evolvable-api-contracts/learn/http-contract-execution-boundary.md), [границы application S06](../slices/service-architecture-boundaries/README.md) и [проверки S10](../slices/risk-based-service-verification/README.md) для размещения enforcement и наблюдения response. Эти материалы помогают проверить, что решение принято до DTO или дорогой работы; они не создают ещё одного Identity/Abuse результата. Два собственных flow не проверяют callback/SSRF или общий quota/rate budget: [D22](debt-register.md#d22), [D23](debt-register.md#d23).

**Результат участника:** одинаковый безопасный отказ для чужого и отсутствующего Order на всех заявленных путях; отдельно — разрешённый tenant-scoped export и нулевая работа после cost rejection. Далее — [gate](module-gates.md#identity), [identity project](implementation-readiness.md#identity) и [export project](implementation-readiness.md#export).

## Service Architecture — удешевить следующее изменение правила

<a id="architecture"></a>

**Цель:** изолировать бизнес-правило от HTTP, persistence и Carrier adapter и проверить следующее изменение. **Route status: полный пятижанровый flow.** [Собственный вход S06](../slices/service-architecture-boundaries/README.md) ведёт через learn → interview → kata → project-spec.

Используйте [HTTP execution boundary](../slices/evolvable-api-contracts/learn/http-contract-execution-boundary.md) для сохранения внешнего ответа и [runtime client boundary](../slices/runtime-concurrency-lifecycle/learn/bounded-concurrency-pool-saturation.md) для уже разобранных outbound concerns. [S10](../slices/risk-based-service-verification/README.md) помогает разделить business и adapter evidence. Реальная подмена adapter подтверждает изоляцию только вместе с отдельной проверкой его mapping; fake сам не доказывает БД/HTTP. Read-only eligibility не проверяет transaction, полную External integration или [межкомандные conventions](debt-register.md#d05).

**Результат участника:** business suite без I/O, реальные adapter checks, сохранённый HTTP-контракт и diff повторного policy change с локализованными обязанностями. Далее — [gate](module-gates.md#architecture) и [readiness](implementation-readiness.md#architecture).

## Transactional Persistence Integration — сохранить результат и производные данные

<a id="persistence"></a>

**Цель:** определить, что стало устойчивым после commit и что нужно восстановить или обновить отдельно. **Route status: полный пятижанровый flow.** Собственные входы — [подтверждение заказа S07](../slices/transactional-orders-operation/README.md) и [Orders cache S15](../slices/tenant-scoped-orders-cache/README.md), каждый index → learn → interview → kata → project-spec. Cache требует собственного store baseline; прохождение S07 не подтверждает его автоматически.

Переиспользуйте [S06](../slices/service-architecture-boundaries/README.md) для application operation, [S10](../slices/risk-based-service-verification/README.md) для правдивых checks, [S05](../slices/tenant-scoped-orders-authorization/README.md) для trusted cache key и [runtime](../slices/runtime-concurrency-lifecycle/README.md) для контекста нагрузки. S07 даёт producer event identity и storage-backed idempotency; S15 проверяет производную сводку, а не новый transaction mechanism. One-process coalescing не даёт shared cache migration: [D06](debt-register.md#d06).

**Результат участника:** отдельно восстановление publication после F0–F3 и same/different-key race evidence; отдельно tenant-safe cache, late-fill timeline, outage и recovery. Их нельзя свести к одному green restart. Далее — [gate](module-gates.md#persistence), [S07 readiness](implementation-readiness.md#transaction) и [S15 readiness](implementation-readiness.md#cache).

## External Service Integration — сохранить смысл ответа зависимости

<a id="external"></a>

**Цель:** отличить подтверждённый предметный результат от сбоя, а при деградации управлять временем и ресурсами. **Route status: полный пятижанровый flow.** Собственный вход — [Pricing L1/L2](../slices/truthful-pricing-client-boundary/README.md): E0 index → E1 learn → E2 interview → E3 kata → E4 project-spec. Это одна read-only операция.

Отдельный supporting путь — [runtime-slice](../slices/runtime-concurrency-lifecycle/README.md): R1 lifecycle как prerequisite → R2 bounded concurrency → R3 interview → R4 kata → R5 fan-out project. Он готовит cancellation/load и External L3, но не становится частью E0–E4 задним числом. [S10](../slices/risk-based-service-verification/README.md) помогает выбрать реальную HTTP boundary проверки.

E3 проверяет применение заданного договора; E4 — самостоятельные внутренние типы и mapping. R5 требует failure injection, budget/degradation и recovery при четырёх вызовах. Reuse не доказывает полный S08, retry semantics либо [External L4](debt-register.md#d08); граница L3 зафиксирована в [D24](debt-register.md#d24). Lifecycle поддерживается собственным R1 из полного [HTTP-маршрута](#http); исполненные tracing/resource результаты всё ещё нужны независимо от Pricing.

**Результат участника:** полная матрица HTTP response/failure → adapter outcome → Quote; для L3 отдельно причинный runtime experiment. Далее — [gate](module-gates.md#external), [Pricing readiness](implementation-readiness.md#pricing) и [fan-out readiness](implementation-readiness.md#fanout).

## Background and Message Workflows — восстановить consumer

<a id="workflow"></a>

**Цель:** повторная доставка должна вернуться к тому же бизнес-результату, а не породить вторую заявку или бесконечный requeue. **Route status: полный пятижанровый flow.** [Собственный S09](../slices/recoverable-order-confirmed-consumer/README.md): index → learn → interview → kata → project-spec.

Переиспользуйте [S07](../slices/transactional-orders-operation/README.md) для event identity и producer boundary, [R1](../slices/runtime-concurrency-lifecycle/learn/cancellation-deadlines-resource-lifecycle.md) для lifecycle и [S10](../slices/risk-based-service-verification/README.md) для наблюдений. S09 самостоятельно проверяет commit/ack и poison transition; он не повторяет outbox, не доказывает exactly-once delivery или общий graceful shutdown. [Workflow migration L4](debt-register.md#d09) требует реального межкомандного этапа.

**Результат участника:** state timeline F0–F3, одна business row после redelivery, terminal source/poison observations и recovery новым процессом. Далее — [gate](module-gates.md#workflow) и [readiness](implementation-readiness.md#workflow).

## Service Verification — проверить механизм, который может сломаться

<a id="verification"></a>

**Цель:** подобрать проверки, которые обнаруживают и локализуют существенные отказы, и уменьшить доказанно лишнюю стоимость. **Route status: полный пятижанровый flow.** [Собственный S10](../slices/risk-based-service-verification/README.md): index → learn → interview → kata → project-spec.

Переиспользуйте [S03](../slices/evolvable-api-contracts/README.md) для существующего контракта и ожиданий клиентов, [S06](../slices/service-architecture-boundaries/README.md) для разных test boundaries и [runtime-проект](../slices/runtime-concurrency-lifecycle/project-spec/resilient-fanout-service.md) как контекст failure-path evidence. S10 задаёт отдельный выбор portfolio; он не перепроектирует API и не заменяет [самостоятельное исполнение tracing D20](debt-register.md#d20), content-часть которого закрыта S01. ASGI check не подтверждает proxy/deployment или реальные неизвестные клиентские версии.

**Результат участника:** risk/mechanism/boundary map, минимум три fault cards, два разных consumer expectations и сравнение стоимости/качества до и после сужения проверки. Далее — [gate](module-gates.md#verification) и [readiness](implementation-readiness.md#verification).

## Safe Service Evolution — остановить выпуск и сохранить обязательства

<a id="delivery"></a>

**Цель:** не продолжить выпуск по недостоверному сигналу и восстановить уже обещанное клиенту поведение. **Route status: полный пятижанровый flow.** [Собственный S11](../slices/safe-orders-service-rollout/README.md): index → learn → interview → kata → project-spec.

Переиспользуйте [S03 project](../slices/evolvable-api-contracts/project-spec/evolvable-orders-api.md) как неизменный контракт и [S10 kata](../slices/risk-based-service-verification/kata/detect-orders-error-contract-regression.md) как проверку ошибки. S11 добавляет измеренные стадии, stop и recovery; он не проводит новую миграцию API и не создаёт новый test portfolio. Aggregate exposure не подтверждает каждое сочетание route/form; возврат трафика на old не доказывает доступность записей new. [Delivery L4](debt-register.md#d11) остаётся отдельным действием.

**Результат участника:** план до запуска, три профиля, cohort × route × valid/invalid observations, отсутствие следующей стадии после stop и readback прежних обязательств. Далее — [gate](module-gates.md#delivery) и [readiness](implementation-readiness.md#delivery).

## Performance and Resource Control — установить причину деградации

<a id="performance"></a>

**Цель:** объяснить рост задержек через состояние работы и подтвердить причинность экспериментом. **Route status: полный пятижанровый flow.** [Собственный runtime index](../slices/runtime-concurrency-lifecycle/README.md) → supporting R1 lifecycle → собственные R2 learn → R3 interview → R4 kata → R5 project-spec.

Из соседнего [HTTP-маршрута](#http) нужны восстановление request path и lifecycle; они предшествуют diagnosis и load control соответственно. [S10](../slices/risk-based-service-verification/README.md) полезен для выбора test boundary. Выполненный runtime experiment может показать S08/S13 saturation и recovery, но наличие всех outcome links не означает отдельного [S12 diagnosis](debt-register.md#d21) или [L4 analysis/capacity](debt-register.md#d17). Жанровый долг HTTP закрыт G19; prerequisite tracing требует результатов участника, не ссылки на S01.

**Результат участника:** одинаковый workload до/после, raw measurements, опровергнутая гипотеза, bounded overload и возврат waiting/in-flight к нулю. Далее — [gate](module-gates.md#performance) и [readiness](implementation-readiness.md#fanout).

## Backend / Distributed Systems

<a id="backend"></a>

Для системного владельца backend [каноническая RoleView](../../../roles/backend-distributed-systems.md) и [точные B2 требования](../role-requirements.md#backend--distributed-systems) задают обязательные действия, не список обязательного чтения.

- **Обязательный baseline:** L3 по всем применимым сервисным действиям десяти карточек, с подтверждением более простых действий там, где они ещё не освоены. Контракты помогают Identity/Idempotency/Compatibility; Architecture — Transaction; Lifecycle — External/Cancellation/Load; Tracing — Diagnosis; Evolution + Verification + Compatibility — Delivery. Это ориентиры существующего DAG. Полный [HTTP flow S01](#http) ведёт к собственному refactor L2; production Trace L3 и S12 нельзя засчитать по одному runtime-project link.
- **Deepening path:** от своего дефицита перейти к самостоятельному project-spec: например, Transaction → Workflow или HTTP lifecycle → External → fan-out. Для полной роли обязательны Evolution L4 и Delivery L4: после L3 нужна реальная межкомандная миграция, см. [D14](debt-register.md#d14) и [D11](debt-register.md#d11). Здесь deepening — рост глубины, а не факультативность этих двух требований.
- **Conditional specialization:** дополнительные L4 по фактической ответственности за runtime, security, data или quality. Они не назначаются всем backend-инженерам автоматически. Вход выбирается по concern из [реестра L4](debt-register.md#outcome-debt); до реального контекста выполняются локальные задания, а adoption не заявляется.

## Architecture / Technical Leadership

<a id="architecture-role"></a>

Для backend-специализации [каноническая RoleView](../../../roles/architecture-technical-leadership.md) и [точные B2 требования](../role-requirements.md#architecture--technical-leadership--backend-specialization) сохраняют системный L3 baseline.

- **Обязательный baseline:** уметь проверить причинность и ограничения всех десяти сервисных границ на L3, включая HTTP Runtime, security scope, External degradation и performance. Вход в [обновлённый HTTP flow S01](#http) ведёт к самостоятельному refactor L2; он не подменяет production Trace L3. Не требуется заново писать каждый endpoint, если применимое самостоятельное evidence уже предъявлено и проверено.
- **Deepening path:** Contracts → Architecture/Verification → Delivery как маршрут обсуждения интегрирующих решений, при сохранении hard prerequisites. Обязательные L4 — HTTP conventions, Evolution migration, Architecture conventions, Compatibility process и Delivery coordination. Их реальные результаты представлены условиями [D13](debt-register.md#d13), [D14](debt-register.md#d14), [D05](debt-register.md#d05), [D16](debt-register.md#d16), [D11](debt-register.md#d11). L4 не разрешает пропустить L3 той же capability.
- **Conditional specialization:** runtime/platform, API security, data/integration и quality enablement выбираются по зоне ответственности согласно [таблице специализаций](../role-requirements.md#conditional-l4-specializations). Требуются соответствующие внешняя readiness и реальное применение; локальные Cache/Workflow/Pricing проекты не заменяют migration несколькими командами.

## Самопроверка навигации

Можно ли использовать один результат проекта в двух модулях?

<details>
<summary>Ответ</summary>

Можно предъявить его для применимых supporting действий, но нужно показать разные наблюдения и пределы каждого вывода. В S07 restart publisher подтверждает восстановление intent, а отдельные race/replay результаты — idempotency. Одна ссылка и одно наблюдение не доказывают оба действия автоматически и не создают новое coverage в этом досье.

</details>
