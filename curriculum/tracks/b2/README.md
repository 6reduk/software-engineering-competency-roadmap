---
id: b2.index.pilot-blueprint
kind: index
title: B2 Backend & API Engineering — pilot blueprint
owner_track: b2
status: accepted
updated: 2026-09-08
language: ru
---

# B2 Backend & API Engineering — blueprint

## Назначение

M1.4 описывает структуру пилотного трека. M1.5 проверяет её первым полным thin slice. Каноническая единица компетенции — capability, а не module, cluster, технология или вопрос интервью.

## Состав

- [Modules](modules.md) — 10 стабильных учебных/release-пакетов.
- [Capabilities](capabilities.md) — 19 наблюдаемых инженерных действий.
- [LevelOutcomes](level-outcomes.md) — применимые проявления L1–L5 и evidence criteria.
- [Prerequisites](prerequisites.md) — внутренний DAG и внешние baseline/conditional dependencies.
- [Scenarios](scenarios.md) — рабочие и interview-сценарии, на которых проверяется модель.
- [Coverage map](coverage-map.md) — планируемое и фактическое покрытие типами артефактов.
- [Role requirements](role-requirements.md) — предварительная authoritative-проекция outcomes на две первые роли.
- [Consolidation dossier](consolidation/README.md) — принятые маршруты, критерии module gates, долг и готовность самостоятельных реализаций; обновление после S01 принято gate G20 как явное однопрофильное исключение без новых coverage relationships и module-gate decisions.

## Реализованные slices

- [M1.5 — Evolvable API contracts](slices/evolvable-api-contracts/README.md): два engineering briefs, interview, kata и project specification вокруг сценария S03; gate G4 — `accepted`.
- [M1.7 — Runtime concurrency lifecycle](slices/runtime-concurrency-lifecycle/README.md): два engineering briefs, interview, kata и project specification вокруг сценария S08; gate G4b — `accepted`.
- [M1.8.1 — Service architecture boundaries](slices/service-architecture-boundaries/README.md): engineering brief, interview, kata и project specification вокруг сценария S06; gate G5 — `accepted`.
- [M1.8.3 — Risk-based service verification](slices/risk-based-service-verification/README.md): engineering brief, interview, kata и project specification вокруг сценария S10; gate G6 — `accepted`.
- [M1.8.5 — Transactional Orders operation](slices/transactional-orders-operation/README.md): engineering brief, interview, kata и project specification вокруг сценария S07; gate G7 — `accepted`.
- [M1.8.7 — Recoverable OrderConfirmed consumer](slices/recoverable-order-confirmed-consumer/README.md): engineering brief, interview, kata и project specification вокруг сценария S09; gate G8 — `accepted`.
- [M1.8.9 — Tenant-scoped Orders authorization](slices/tenant-scoped-orders-authorization/README.md): engineering brief, interview, kata и project specification вокруг сценария S05; gate G9 — `accepted`.
- [M1.8.11 — Cost-bounded Orders export](slices/cost-bounded-orders-export/README.md): принятый engineering brief, interview, kata и project specification вокруг operation-cost половины S14; SSRF-половина не входит в slice.
- [M1.8.13 — Tenant-scoped Orders cache](slices/tenant-scoped-orders-cache/README.md): материалы в `accepted` — engineering brief, interview, kata и project specification вокруг S15; Cache L2/L3 без cross-worker guarantee и Cache L4.
- [M1.8.15 — Safe Orders service rollout](slices/safe-orders-service-rollout/README.md): пять материалов в `accepted` вокруг S11; G14 подтвердил Delivery L1–L3, измеренные стадии, stop и recovery при ограниченной обратимости. Авторский Gate 0 — `confirmed`, disposable-стенд удалён.

- [M1.8.17 — Правдивая граница клиента Pricing](slices/truthful-pricing-client-boundary/README.md): пять материалов в `accepted`, External L1/L2; Gate 0 независимо подтверждён профилем A, G16 принят как явное однопрофильное исключение. Module completion не заявлен.

Интеграционный milestone M1.8.15 — [самостоятельный Orders rollout](slices/safe-orders-service-rollout/project-spec/evidence-driven-orders-rollout.md) в отдельном репозитории: планирование L2 и сохранение обязательств при восстановлении L3 проверяются раздельно. Регистрация материалов не является принятием milestone или module gate.

Интеграционный milestone M1.8.17 — [одна read-only операция Pricing](slices/truthful-pricing-client-boundary/project-spec/integrate-one-pricing-operation.md): самостоятельный выбор внутренней модели L2, фактический HTTP response/failure, one-attempt решение и измеренный lifecycle. [Kata L1](slices/truthful-pricing-client-boundary/kata/stop-failure-to-empty-collapse.md) отдельно проверяет применение заданного договора на одном failure→empty defect. Принятие milestone не является module-gate decision.

- [M1.8.20 — Локализация потери request context](slices/request-context-loss-diagnosis/README.md): четыре материала в `accepted` вокруг S01 — собственные index/interview/kata/project-spec HTTP Runtime; learn-переходы используют принятые C1/R1. Gate 0 независимо воспроизведён профилем A, G19 принят как явное однопрофильное исключение. Module completion не заявлен.

Интеграционный milestone M1.8.20 — [сохранить контекст через собственный refactor](slices/request-context-loss-diagnosis/project-spec/preserve-context-through-refactor.md): участник выбирает диагностический concern и границу изменения, локализует первую потерю, сохраняет HTTP-контракт и проверяет изоляцию/recovery. Это задание на Trace L2 в отдельном репозитории, не зарегистрированная реализация и не module-gate decision.

## Инварианты

1. Capability принадлежит B2 и формулируется действием на границе backend-сервиса.
2. Знание Python/runtime принадлежит B1; протоколы/сеть/security foundations — A3; данные — B3; распределённые гарантии — B5; platform implementation — B6; общая reliability discipline — B7; организационное лидерство — C1.
3. Module развивает несколько capabilities; capability может входить в несколько modules.
4. Не каждая capability имеет outcomes на каждом уровне.
5. FastAPI/Pydantic/ASGI используются как основная реализация пилота, но capability остаётся переносимой на другой backend stack.
6. Planned coverage не является доказательством освоения и не означает, что artifact уже существует.

## Aggregate catalog notation M1.4

Файлы `modules.md`, `capabilities.md` и `level-outcomes.md` — governance-каталоги blueprint, а не content Artifacts. Их frontmatter с полем `artifact` отслеживает состояние work package и не создаёт новый semantic kind.

До создания track repository entity records хранятся компактно со следующими правилами раскрытия:

- file-level entity defaults: `owner_track: b2`, `status: accepted`, `updated: 2026-08-15`, `language: ru`; frontmatter каталога описывает состояние bounded work package и может иметь иной workflow status до gate acceptance;
- Module: `id` и `title` задаёт heading, `kind: module`; body обязан содержать scope, develops и non-goals;
- Capability: table row задаёт `id`, `title`, `primary_cluster`, action и primary module, `kind: capability`;
- LevelOutcome: section задаёт `capability`, row задаёт `id`, `level`, action/context/autonomy и evidence, `kind: level-outcome`;
- relationship target всегда записывается полным semantic ID; локальные labels вроде `S03` не являются semantic IDs;
- при материализации в track repository defaults разворачиваются в обязательные metadata каждой entity без изменения semantic ID.

Это временная serialization M1.4, а не новая сущность метамодели. Её пригодность входит в G3; после двух slices формат может быть заменён schema/validator согласно D-024.

## Gate G3

Blueprint принимается, если:

- каждую capability можно проверить действием и evidence;
- уровни отличаются автономностью, неопределённостью, масштабом или последствиями;
- internal prerequisite graph ацикличен;
- внешнее ownership не копируется;
- два выбранных slices собираются из общей модели без специальных сущностей;
- role requirements ссылаются на конкретные outcomes, а не наследуют весь track-level target.
