---
artifact: b5-modules-blueprint
title: "Модули B5 по системному результату"
owner_track: b5
status: accepted
updated: 2026-09-17
language: ru
---

# Модули B5 по системному результату

Модули собирают действия по единому профессиональному результату. [Defaults](README.md#notation) применяются к каждой записи. Это навигационные дома будущего содержания, без заявления о выпуске или завершении.

<a id="bound-system-guarantees"></a>

## `b5.module.bound-system-guarantees` — Определять допустимый результат при частичном отказе

**Scope:** Модель участников, неизвестного исхода и обещания чтения образует один системный договор.

**Clusters:** `b5.cluster.failure-models`, `b5.cluster.consistency-availability`.

**Develops:** `b5.capability.model-partial-failures`, `b5.capability.choose-read-guarantees`.

**Non-goals:** Ремонт сети, диагностика конкретного DB engine и SLO.

<a id="preserve-authority-across-failures"></a>

## `b5.module.preserve-authority-across-failures` — Сохранять право на действие при смене владельца

**Scope:** Причинный порядок, полномочия и смена лидера связываются с допустимостью эффекта у ресурса.

**Clusters:** `b5.cluster.time-order-coordination`, `b5.cluster.consensus-leadership`.

**Develops:** `b5.capability.reconstruct-causal-order`, `b5.capability.exclude-stale-actors`, `b5.capability.assess-leadership-guarantees`.

**Non-goals:** Формальные доказательства протоколов, реализация consensus и production runbook.

<a id="place-state-with-bounded-failure-cost"></a>

## `b5.module.place-state-with-bounded-failure-cost` — Размещать состояние с явной ценой отказа и роста

**Scope:** Размещение, перенос владения и модель региональной ёмкости сохраняют договор данных при изменении состава участников.

**Clusters:** `b5.cluster.replication-sharding`, `b5.cluster.capacity-multi-region`.

**Develops:** `b5.capability.choose-state-placement`, `b5.capability.plan-shard-ownership-transfer`, `b5.capability.assess-regional-capacity`.

**Non-goals:** Store tuning, production topology, cloud provisioning, DR-процесс и численные эксплуатационные нормативы.

<a id="compose-delivery-and-business-effects"></a>

## `b5.module.compose-delivery-and-business-effects` — Согласовывать доставку и бизнес-эффекты

**Scope:** Доставка, повтор, фиксация и компенсация рассматриваются как разные границы одного межсистемного результата.

**Clusters:** `b5.cluster.messaging-events`, `b5.cluster.idempotency-retries`, `b5.cluster.distributed-transactions`.

**Develops:** `b5.capability.define-delivery-contract`, `b5.capability.bound-repeat-effects`, `b5.capability.control-retry-propagation`, `b5.capability.compose-state-and-publication`, `b5.capability.choose-cross-system-atomicity`.

**Non-goals:** SDK, SQL outbox, endpoint implementation и реализация transaction coordinator.

<a id="bound-staleness-and-overload"></a>

## `b5.module.bound-staleness-and-overload` — Ограничивать распространение устаревания и перегрузки

**Scope:** Системный cache и управление потоком связывают обещание свежести с ценой работы зависимых участников.

**Clusters:** `b5.cluster.caching-load-control`.

**Develops:** `b5.capability.bound-cache-staleness`, `b5.capability.control-system-load`.

**Non-goals:** Прикладное размещение cache, API abuse controls, настройка платформы и SRE-процесс.

<a id="preserve-guarantees-through-change"></a>

## `b5.module.preserve-guarantees-through-change` — Сохранять межсистемный договор при эволюции

**Scope:** Смешанные версии и различающие истории позволяют оценить сохранность общего договора.

**Clusters:** `b5.cluster.evolution-verification`.

**Develops:** `b5.capability.preserve-mixed-version-contract`, `b5.capability.design-distinguishing-histories`.

**Non-goals:** Код тестового стенда, rollout automation, migration SQL и эксплуатационный допуск.
