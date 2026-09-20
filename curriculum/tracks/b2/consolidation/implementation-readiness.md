---
id: b2.plan.consolidation-implementation-readiness
kind: plan
title: B2 — готовность к самостоятельным проектам
owner_track: b2
status: accepted
updated: 2026-09-09
language: ru
---

# Готовность к самостоятельным проектам

Вы выбрали project-spec, но готового репозитория нет. Это ожидаемый переход: участник сам создаёт минимальную систему, принимает оставленные ему решения и предъявляет проверяемый результат. Этот файл помогает подготовиться к двенадцати принятым проектам B2, не выдавая архитектуру или готовый код.

Выберите карточку проекта ниже. Сначала проверьте learning route и доступность его среды, затем откройте саму спецификацию целиком: она остаётся источником точных fixtures, командных обязанностей, populations и thresholds. Краткие контуры ниже не заменяют её acceptance criteria. Точные закреплённые версии берутся из metadata соответствующего project-spec; общего «последнего стека B2» здесь нет. При изменении baseline участник повторяет применимые readiness-проверки, не переносит старые измерения автоматически.

**Readiness** — готовность начать именно этот опыт; **evidence** — наблюдаемый результат его выполнения; **proficiency** — подтверждённая способность участника после проверки. **ImplementationReference** появляется только после самостоятельного выполнения и review. Учебные coverage links и project-spec не являются реализацией; **module gate** остаётся отдельным решением. Эти определения согласованы с [досье](README.md#terms). Ноль ImplementationReference — snapshot после [G19](../../../../governance/reviews/M1.8.20-G19-http-runtime-acceptance.md), учтённый один раз в [D26](debt-register.md#d26).

## Checklist старта собственного репозитория

До реализации нужно сделать воспроизводимыми исходные условия, иначе reviewer не отличит исправление от изменения стенда.

- [ ] Выбран один project-spec и его целевое действие; проверены требования выбранной роли — [Backend / Distributed Systems](routes-and-reuse.md#backend) или [Architecture / Technical Leadership](routes-and-reuse.md#architecture-role), [scope и prerequisites](../prerequisites.md).
- [ ] Прочитаны index, learn, interview и kata выбранного маршрута либо предъявлены применимые ранее проверенные результаты; отсутствие нового чтения не подменяет prerequisite evidence.
- [ ] В отдельном репозитории участника записаны ссылка на spec, его revision/date, точные версии, topology, fixtures и команды запуска/сброса/очистки.
- [ ] Проверены реальные механизмы среды, требуемые spec: БД, broker, cache или HTTP transport; mock не заменяет механизм, который нужно наблюдать.
- [ ] До изменения записаны invariants, конкурирующие гипотезы или план, measurement populations, точки наблюдения, thresholds и ожидаемые control/failure/recovery результаты.
- [ ] Решения участника отделены от заданного контракта; отклонение от spec получает явное согласование, а не скрытую замену проверки.
- [ ] Подготовлено безопасное сохранение raw observations без credentials; опубликованный отчёт не содержит секреты.

Авторские стенды S11/Pricing/S01 не предоставляются как scaffold. Исторический Gate 0 подтверждает доступность механики в ограниченной среде автора, но не запуск в вашем репозитории. [D25](debt-register.md#d25) сохраняет условия будущих расширений. Репозиторий, scaffold, grader и CI template данным dossier не создаются.

## Сохранить контекст через собственный refactor

<a id="http"></a>

**Задание:** [Preserve context through refactor](../slices/request-context-loss-diagnosis/project-spec/preserve-context-through-refactor.md), H3. Вход — [полный HTTP route](routes-and-reuse.md#http): собственный index, supporting C1 и собственный R1 learn, затем interview и kata. G19 закрыл content/navigation D19 и content/exercise D20; исполнение участником остаётся открытым.

**Самостоятельная работа и среда:** отдельный репозиторий с одним GET /quote, три заданных исхода и server-owned UUID в X-Request-ID. Участник выбирает диагностическое значение, владельца, область жизни и одну границу refactor, сохраняя публичный договор; готового scaffold и решения нет. Минимальная среда — закреплённые версии project-spec, один процесс/event-loop thread, async dependency/endpoint/error handlers и HTTPX ASGITransport без сети. До опыта нужны собственные B1/A3 readiness-наблюдения трёх исходов и topology; иной baseline требует повтора, G19 не подтверждает новую среду автоматически.

**Минимальное evidence:** минимум две гипотезы до instrumentation, независимая корреляция, исходный симптом и первая наблюдаемая потеря, изменение одного фактора и регрессия, чувствительная к обходу pipeline. Базовые профили — 366 операций: три повтора control/defect/fixed по 30, concurrent по 12 с гарантированным перекрытием, recovery по 20 последовательных после волны (всего recovery 60). Дополнительно матрица трёх исходов × трёх форм входящего X-Request-ID × control/defect/fixed — 27 операций; три negative bypass controls. Минимум проекта — **396 операций**, отдельно от 369 авторского probe G19. Watchdog 5 с на последовательный запрос/волну; длительность до завершения ASGI и cleanup сохраняется, это не performance SLA.

В defect заранее объявляется затронутая популяция: 100% ожидаемых потерь внутри и 0 вне неё. В control/fixed/concurrent/recovery — 0 потерь в обещанной области, чужих значений и нарушений публичного договора. При внутреннем concern HTTP-контракт может сохраняться и на defect; это нужно объяснить. До возможной reference нужны raw/summary по каждой группе, версии/команды, decision record, честное указание знания посева, независимое review реализации и обработанные findings.

**Предел claims:** локальный Trace L2, без production reconstruction L3, network behavior, worker reuse, crash/disconnect/cancellation, auth/tenant или нового lifecycle coverage. Проект не повторяет известный handler defect S10 и не включает S02/fan-out. После выполнения и review он может стать примером конкретного выбора concern, но не готовым шаблоном для всех сервисов. [HTTP gate](module-gates.md#http), открытые [D20](debt-register.md#d20) и [D26](debt-register.md#d26).

## Эволюция Orders API

<a id="contracts"></a>

**Задание:** [Evolvable Orders API](../slices/evolvable-api-contracts/project-spec/evolvable-orders-api.md). Вход — [Contracts route](routes-and-reuse.md#contracts), HTTP baseline A3 и навыки локальной реализации B1.

**Самостоятельная работа и среда:** минимальный Orders service с create/read/сменой состояния, минимум два клиента с разными ожиданиями, локальные журналы и checks. In-memory store допускается спецификацией. Участник выбирает архитектуру, переходный механизм, модель наблюдения и основание удаления старого поведения.

**Минимальное evidence:** воспроизводимые v0/v1, старые/новые success и invalid paths, значимый schema diff и семантический дефект, который ловит клиент; минимум два сценария отказа при моделировании миграции, stop и один recovery path. При header-based выборе ответа применяется условие проверки кэша из spec. До reference нужны consumer inventory, ADR, migration report, результаты review и ретроспектива. Правильным результатом может быть обоснованное сохранение старого пути при недостатке наблюдений.

**Предел claims и возможность примера:** локальные клиенты не доказывают реальный cross-team adoption или безопасность всех неизвестных consumers. После воспроизведения и review репозиторий может стать примером выбранного компромисса с явно названными слепыми зонами; способ версионирования не становится обязательным образцом. См. [gate](module-gates.md#contracts), [D14](debt-register.md#d14).

## Устойчивый fan-out Quote API

<a id="fanout"></a>

**Задание:** [Resilient fan-out service](../slices/runtime-concurrency-lifecycle/project-spec/resilient-fanout-service.md). Вход — [Performance route](routes-and-reuse.md#performance) и [HTTP lifecycle/tracing](routes-and-reuse.md#http), B1 async и применимый A3/B7 контекст. Собственный HTTP flow теперь полный: content-части [D19/D20](debt-register.md#d19) закрыты G19. Самостоятельное исполнение S01 и resource path остаются разными результатами; переход сюда не засчитывает их.

**Самостоятельная работа и среда:** Quote API, настоящая управляемая HTTP Pricing dependency с normal/slow/error/hanging, async client/pool, нагрузочный генератор и локальные counters/traces. Участник выбирает быстрый отказ либо явный partial result, ownership задач, admission, queue и инженерные альтернативы в пределах spec.

**Минимальное evidence:** исходный контур — 12 concurrent входящих запросов, fan-out 4, pool ≤8; два прогона по 60 с и по 10 с наблюдения после. Healthy Pricing 80 мс, degraded — 25% вызовов по 700 мс. Service-side время от приёма до application outcome: healthy p95 всех входящих ≤450 мс, каждый degraded outcome ≤650 мс; deadline 600 мс, каждая попытка pool wait ≤100 мс. Waiting/in-flight возвращаются к 0 ≤1 с после снятия нагрузки, shutdown ≤2 с. Hanging, burst и реальный server/transport disconnect проверяются отдельно, как требует spec.

До reference нужны baseline/raw report, normal/failure traces, task balance, lifecycle map, таблица событий/исходов, один controlled experiment, ADR с альтернативами и обработанное review. Изменение одного существенного фактора должно различать причину и симптом.

**Предел claims и возможность примера:** эти thresholds относятся к объявленному опыту; они не обещают cleanup после kill/crash, прекращение blocking work или remote side effects. После review проект может иллюстрировать один выбор degradation/ownership с сохранённым baseline; не универсальные concurrency числа. [Gates](module-gates.md#performance), [External L3 boundary](debt-register.md#d24).

## Границы eligibility в Orders service

<a id="architecture"></a>

**Задание:** [Order cancellation policy service](../slices/service-architecture-boundaries/project-spec/order-cancellation-policy-service.md). Вход — [Architecture route](routes-and-reuse.md#architecture), HTTP boundary и существующий runtime client context.

**Самостоятельная работа и среда:** read-only endpoint, реальная локальная БД/ORM и HTTP Carrier stub. Участник выбирает functions/interfaces/objects и способ wiring; сохраняет заданное правило и прежний HTTP contract. Повторное локальное условие для STANDARD + PACKED определяется до реализации.

**Минимальное evidence:** business tests без I/O, фактическая подмена adapter без изменения application/domain, отдельные реальные DB/HTTP mappings, endpoint regression и diff повторного policy change. До reference нужны исходный change path, минимум две альтернативы, incremental migration, стоимость indirection и review report. Fake не заменяет реальный adapter check.

**Предел claims и возможность примера:** один eligibility flow не доказывает transactions, весь External scope или cross-service conventions. После review пример пригоден для обсуждения стоимости границы и её удаления, не как обязательная Clean/Hexagonal структура. [Gate](module-gates.md#architecture), [D05](debt-register.md#d05).

## Portfolio проверок Orders service

<a id="verification"></a>

**Задание:** [Orders verification portfolio](../slices/risk-based-service-verification/project-spec/orders-verification-portfolio.md). Вход — [Verification route](routes-and-reuse.md#verification), готовый S03 contract, S06 boundaries и runtime failure-path context.

**Самостоятельная работа и среда:** один работающий Orders service, production-like application assembly и минимум два представительных клиента. Реальные adapters нужны только если они существуют в выбранном сервисе. Участник выбирает risk inventory, дешёвые правдивые границы, 3–4 fault cards и measurement envelope; новый контракт и deployment platform не проектируются.

**Минимальное evidence:** минимум три разных механизма отказа, включая S10 handler defect; component/HTTP signals различают причины. Consumer inventory сохраняет разные ожидания нового клиента и legacy script. До измерения заданы repetitions/duration, machine baseline, thresholds, минимум одна метрика стоимости и одна качества. После удаления/сужения минимум одной slow/flaky дублирующей check повторяются те же faults и critical paths. До reference нужны исходный/итоговый portfolio, raw summary, решение о release/migration, alternatives и review.

**Предел claims и возможность примера:** ASGI evidence не доказывает proxy/network/deployment, а конечные fault cards — все production failures или межкомандный quality process. После review пример показывает, почему удаление конкретного дублирования безопасно; его suite не копируется как эталон для другого сервиса. [Gate](module-gates.md#verification), [D10](debt-register.md#d10), [D16](debt-register.md#d16).

## Восстанавливаемое подтверждение заказа

<a id="transaction"></a>

**Задание:** [Resilient order confirmation](../slices/transactional-orders-operation/project-spec/resilient-order-confirmation.md). Вход — [Persistence route](routes-and-reuse.md#persistence), S06 application boundary, HTTP/idempotency context и S10 method; нужна B3 readiness выбранного реального PostgreSQL/Psycopg baseline.

**Самостоятельная работа и среда:** одна confirm command, PostgreSQL, publisher и управляемый event sink. Участник выбирает schema/constraints, lifecycle и recovery/lease mechanism, сохраняя contract одной transaction, operation identity и устойчивого event intent. Для unknown commit требуется настоящий protocol window с разрывом соединения, а не exception до commit.

**Минимальное evidence:** отдельно Transaction L3 — F0–F3 state/recovery, отдельно Idempotency L3 — same/different-key races, replay/conflict/retention. Spec требует по 10 F0/F2/F3, 20 F1 с наблюдением обоих допустимых server outcomes, 20 same-key и 20 different-key trials по два одновременно отпущенных запроса, по 5 conflict/new-key-confirmed/retention cases. Наблюдаются authoritative PostgreSQL после quiescence, sink и HTTP results; ноль нарушений invariants и вторых transitions/event records, все F2 обнаружимы после restart, F3 сохраняет event_id. До reference нужны fault/control/recovery snapshots, raw counts, отдельные выводы по двум действиям, ADR и review.

**Предел claims и возможность примера:** стабильный event_id не означает exactly-once delivery; конечный опыт не доказывает все timing/topology combinations. После review пример показывает конкретные failure windows и выбранную recovery boundary, не универсальный outbox recipe. [Gate](module-gates.md#persistence), [D07](debt-register.md#d07).

## Восстанавливаемый fulfillment consumer

<a id="workflow"></a>

**Задание:** [Resilient fulfillment consumer](../slices/recoverable-order-confirmed-consumer/project-spec/resilient-fulfillment-consumer.md). Вход — [Workflow route](routes-and-reuse.md#workflow), S07 event identity, R1 lifecycle и S10 evidence method; отдельно B5 broker и B3 durable-result readiness.

**Самостоятельная работа и среда:** реальные RabbitMQ и PostgreSQL, один consumer, source quorum queue и poison target, один business side effect. Broker/ack/reject policy задана spec; участник выбирает структуру handler, states/observations, SQL и fault hooks, не заменяет broker или DLQ scheme.

**Минимальное evidence:** по 10 process-exit прогонов F0/F1/F2, 10 valid control events, 10 invalid poison events; одно сообщение, один consumer, prefetch 1 и до 30 с на terminal observation. Business row одна; F1/F2 возвращают прежний result; source counters 0/0. Poison profile требует row 0 и message с reason `delivery_limit` в target. Недоступный DLX target оставляет transfer незавершённым. До reference нужны fault markers, delivery/SQL/queue observations, отдельные L2 ownership и L3 recovery conclusions, decision record и review.

**Предел claims и возможность примера:** нет exactly-once delivery, producer/outbox, общего shutdown или multi-team migration evidence. После review пример демонстрирует один consumer workflow в закреплённой семантике; handler не превращается в универсальный inbox. [Gate](module-gates.md#workflow), [D09](debt-register.md#d09).

## Tenant-safe чтение Orders

<a id="identity"></a>

**Задание:** [Tenant-safe Orders read API](../slices/tenant-scoped-orders-authorization/project-spec/tenant-safe-orders-read-api.md). Вход — [Identity route](routes-and-reuse.md#identity), HTTP/application/test boundaries; readiness A3 trust отдельно от умения написать endpoint.

**Самостоятельная работа и среда:** один endpoint, два tenants и missing Order fixture, локальная RSA fixture pair, validator и store. Private key принадлежит test issuer, сервис получает public key. Участник выбирает trust/enforcement placement, ports и audit sink, сохраняя заданный договор; IdP/JWKS/rotation не реализуются.

**Минимальное evidence:** отдельные allowed, unauthenticated, cross-tenant, forged-context и missing-object populations; context после validation, exact HTTP/audit и negative disclosure assertions. Проверяются direct operation call и минимум один дополнительный bypass path, отсутствие context, равенство cross-tenant/missing response. До reference нужны threat/bypass matrix, traceability test/output, component и assembled HTTP results, decision record с альтернативами и review. Credential или claims dump не включаются в отчёт.

**Предел claims и возможность примера:** один tenant rule не доказывает всю IAM security, callback/SSRF или Identity L4. После review пример показывает конкретную границу authority и placement, не универсальную RBAC/ABAC архитектуру. [Gate](module-gates.md#identity), [D03](debt-register.md#d03).

## Cost-bounded Orders export

<a id="export"></a>

**Задание:** [Cost-bounded Orders export API](../slices/cost-bounded-orders-export/project-spec/cost-bounded-orders-export-api.md). Вход — [Identity/cost route](routes-and-reuse.md#identity) и принятый trusted context S05, с отдельной threat/cost readiness.

**Самостоятельная работа и среда:** один процесс, синхронный CSV, tenant-indexed fixtures двух tenants с минимум 3000 Orders на исследуемый tenant. Участник выбирает code boundaries, strict binding/error mapper и evidence; формула cells и порог 2000 заданы, не выбираются по удобству результата.

**Минимальное evidence:** по 20 последовательных ASGI requests normal 400×4, at-limit 500×4, over-limit 501×4, bypass 500×5; recovery normal после 100 bypass. Наблюдаются HTTP/CSV, normalized estimate, server executor/cell deltas, audit; rejected work delta 0, legitimate output корректен. Дополнительно strict/forbidden/extra/tenant input cases. До reference нужны cost/threat и все четыре строки applicability matrix, raw populations, раздельные L2/L3 выводы, false-positive trade-off, decision record и review. Диагностические milliseconds Gate 0 не являются acceptance target.

**Предел claims и возможность примера:** нет time-window quota, общего capacity bound, SQL-cost guarantee или SSRF control. После review пример показывает одну cost unit и повод её пересмотра, не production формулу. [D22](debt-register.md#d22), [D23](debt-register.md#d23), [gate](module-gates.md#identity).

## Tenant Orders summary cache

<a id="cache"></a>

**Задание:** [Resilient Orders summary cache](../slices/tenant-scoped-orders-cache/project-spec/resilient-orders-summary-cache.md). Вход — [Persistence/cache route](routes-and-reuse.md#persistence), S07 commit, S05 trusted tenant, runtime load context. Требуется отдельная B3 cache-store readiness; B5 не переносится на one-process гарантию.

**Самостоятельная работа и среда:** реальные PostgreSQL и Redis, один Uvicorn worker/event loop, общий async client, заданные key/value fixtures. Участник выбирает application/adapters, per-key coordination и способы наблюдения; не меняет fail-closed contract на fallback. TTL 2 с, command budget 250 мс, pool 64 и отключённые retries берутся из spec.

**Минимальное evidence:** cold miss и 20 warm hits; пять bursts ×32, каждый с correct 200, source_read≤1 и ≤150 мс в project envelope; tenant isolation; управляемая late-fill race с freshness ≤2250 мс; pre-GET failure — 32 controlled 503, zero source reads и ≤350 мс; post-read SET failure — 503, no fill и до N reads при продолжающемся отказе; recovery 32 correct 200 v2, source_read≤1, ≤150 мс. Точка времени — от входа read operation до application outcome в одном процессе. Сохраняются rollback, cancellation/no-stuck-waiter и отрицательная демонстрация двух workers. Host-dependent выключение Redis не заменяет управляемый fault profile.

До reference нужны baseline, counters на key, commit/delete/fill timeline, раздельные L2 normal/isolation и L3 race/failure выводы, ADR и review. Отличие kata: её concurrent-miss correctness не наследует project latency threshold; recovery проверяется отдельно.

**Предел claims и возможность примера:** нет cross-worker coalescing, zero-stale, distributed migration или durability Redis. После review пример сохраняет one-process границу и trade-off; не предлагается как распределённый lock recipe. [Gate](module-gates.md#persistence), [D06](debt-register.md#d06).

## Поэтапный Orders rollout

<a id="delivery"></a>

**Задание:** [Evidence-driven Orders rollout](../slices/safe-orders-service-rollout/project-spec/evidence-driven-orders-rollout.md). Вход — [Delivery route](routes-and-reuse.md#delivery), неизменный S03 и готовые S10 checks; hard prerequisites Evolution/Verification/Compatibility и применимая B6/B7 среда.

**Самостоятельная работа и среда:** различимые old/new/fixed, HTTP requests, управление маршрутами, состояние и raw logs. Участник выбирает topology состояния и процессов, подготовку fixed, observation linkage и исполнимый план. Авторская память new/fixed не выдаётся за его storage architecture.

**Минимальное evidence:** план до запуска и три профиля: healthy B–S3; 503 в S1 с запретом S2 и R-old 100 legacy; нарушенный S2 с 20/100 scheduled contract violations, запретом S3 и R-fixed 100+100. После R-fixed читаются все 80 ранее принятых scheduled-заказов с сохранением окон. В каждом 5-секундном окне — заданные spec populations, 80/20 valid/invalid каждой применимой когорты, отсутствие retry; HTTP timeout 1 с, controller guard 5,25 с, не latency SLO. Для healthy/восстановления нарушения и unexpected errors равны 0, exposure точно соответствует таблице spec.

До reference нужны cohort × route × valid/invalid matrix, включая обе legacy-формы на old/new в S1, фактические версии и серверные записи по request ID; первоначальный план, timeline, stop/go decisions, readback и review. После сохранения результатов проверяется cleanup. R-old сам не доказывает доступность записей new; если состояния раздельны, нужна отдельная проверка их доступности согласно spec.

**Предел claims и возможность примера:** общий словарь не доказывает migration/durability после crash; локальный rollout не является Delivery L4. После review пример показывает предел обратимости в выбранной topology; не становится production delivery template. [Gate](module-gates.md#delivery), [D11](debt-register.md#d11).

## Одна правдивая операция Pricing

<a id="pricing"></a>

**Задание:** [Integrate one Pricing operation](../slices/truthful-pricing-client-boundary/project-spec/integrate-one-pricing-operation.md). Вход — собственный [External E0–E4 route](routes-and-reuse.md#external); lifecycle prerequisite, A3 trusted HTTP и B5 applicability только read-only/one-attempt.

**Самостоятельная работа и среда:** Quote ASGI application с явно запущенным lifespan, общий HTTPX client, настоящий loopback HTTP Pricing; один read-only вызов. Участник выбирает внутренние result/error types и mapping boundaries, сравнивает минимум два варианта, не меняет заданные wire outcomes или one-attempt решение.

**Минимальное evidence:** 11-строчная матрица spec по три последовательных операции: control 6, defect 33, fixed 33, recovery 6; четыре negative checks дают 82 входящих и 79 outbound attempts/receipts. Целевая мутация — одно failure→empty; false absence среди девяти failure rows меняется 27/27 → 0/27, full/empty сохраняются. Время от ASGI вызова Quote до полного ответа <500 мс на каждый request; phase timeouts по 100 мс не являются общим deadline. Drain после строки ≤1 с, закрытие client и server/port проверяются в соответствующих bounds ≤1 с. Дополнительные edge cases не меняют знаменатель основной матрицы.

До reference нужны per-ID HTTP bytes/status/media либо exception → adapter outcome → Quote result, независимые attempts/receipts, raw duration/resource observations, config без hidden retry, decision record и обработанное review. Одно исправление kata не заменяет самостоятельного выбора L2.

**Предел claims и возможность примера:** конечные loopback responses не доказывают TLS/proxy/DNS/SSRF, streaming, disconnect/pool saturation, External L3/L4; timeout не означает remote cancellation. После review пример показывает одну интерпретацию результата с альтернативами, а не универсальный vendor client. [Gate](module-gates.md#external), [D24](debt-register.md#d24).

## Checklist завершения и регистрации

Репозиторий становится проверяемым результатом, когда другой инженер может повторить причинную цепочку. До этого ссылка лишь указывает на незавершённую работу.

- [ ] Сохранены control, исходный отказ и исправленный/recovery профиль, где они требуются; команды и fixtures воспроизводят их без ручного исправления данных ради зелёного результата.
- [ ] Raw observations позволяют пересчитать thresholds и увидеть нарушения/пропуски; expected и actual разделены.
- [ ] Для каждого заявляемого действия названы test/output, autonomy и предел доказательства. Разные outcomes не засчитаны по одному недифференцированному green signal.
- [ ] Runtime/failure проверки выполнены на требуемом механизме; версия и topology совпадают с заявлением либо отклонение согласовано и перепроверено.
- [ ] ADR/decision record содержит альтернативы, последствия и trigger пересмотра; ограничения из карточки сохранены рядом с результатом.
- [ ] Reviewer воспроизвёл результаты в объёме выбранной спецификации; findings обработаны, review artifact и ретроспектива сохранены.
- [ ] Результаты сохранены до cleanup; временные процессы/порты/данные очищены там, где это требуется, репозиторий и отчёт доступны для проверки.
- [ ] Только после выполнения и review предлагается регистрация ImplementationReference с точной revision реализации, ссылкой на spec, отчётом и пределами применимости. Досье такую регистрацию не выполняет.

Проверенный проект может быть **примером опыта**, если читатель видит исходную неопределённость, альтернативы и цену выбора. Учебное задание остаётся самостоятельным: пример не превращается в единственную правильную архитектуру или заранее заполненный scaffold следующего участника. Один project reference не означает автоматического proficiency всех его links и не заменяет [module-gate decision](module-gates.md).

## Где начинается L4

Все двенадцать проектов ограничены локальным сервисным действием. Даже если у участника есть несколько процессов, именованные «команды» и подробный migration plan, это не реальный cross-team result. Для обязательных Evolution/Delivery L4 обеих ролей, дополнительных HTTP/Architecture/Compatibility L4 Architecture role и выбранных специализаций нужны реальные владельцы, согласованный технический stage, фактические adoption/migration observations, exceptions и feedback. Конкретные условия находятся только в [D02–D18](debt-register.md#outcome-debt).

Это условие будущей работы в реальном контексте, не задание симулировать организацию в лаборатории. C1 остаётся владельцем организационного участия, B2 оценивает технический механизм и последствия. Новая реализация или policy без этого контекста не закрывает L4.

## Самопроверка перед защитой

Если проект запускается и все tests зелёные, можно ли уже зарегистрировать reference?

<details>
<summary>Ответ</summary>

Сначала нужно проверить, что tests включают нужный механизм и отличаются на исходном отказе, измерения имеют правильную population, решения самостоятельны и review завершён. Например, mock готового no_offers ничего не говорит о malformed HTTP bytes Pricing, а новый успешный POST после rollout не доказывает сохранность прежних scheduled-заказов. Ссылка появляется после проверки этих результатов, не вместо неё.

</details>
