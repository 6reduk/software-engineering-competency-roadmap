---
artifact: b5-capabilities-blueprint
title: "Канонические действия B5"
owner_track: b5
status: accepted
updated: 2026-09-17
language: ru
---

# Канонические действия B5

Каждая строка — одно действие с единственным primary cluster и primary module. [Формат](README.md#notation) задаёт metadata; соседние связи вынесены в [Related](prerequisites.md#related), а не дублируют действия.

| ID | Title | Primary cluster | Действие и граница | Primary module |
|---|---|---|---|---|
| <a id="model-partial-failures"></a>`b5.capability.model-partial-failures` | Строить модель частичных отказов | `b5.cluster.failure-models` | Разделяет отказ участника, потерю связи, паузу и неизвестный исход по границам подтверждения. | `b5.module.bound-system-guarantees` |
| <a id="choose-read-guarantees"></a>`b5.capability.choose-read-guarantees` | Выбирать договор видимости чтения | `b5.cluster.consistency-availability` | Определяет допустимые истории чтений и цену доступности и задержки при разных моделях согласованности. | `b5.module.bound-system-guarantees` |
| <a id="reconstruct-causal-order"></a>`b5.capability.reconstruct-causal-order` | Восстанавливать причинный порядок | `b5.cluster.time-order-coordination` | Отделяет причинность и конкурентность от показаний несогласованных часов. | `b5.module.preserve-authority-across-failures` |
| <a id="exclude-stale-actors"></a>`b5.capability.exclude-stale-actors` | Исключать эффекты устаревшего владельца | `b5.cluster.time-order-coordination` | Связывает lease или epoch с проверкой полномочия в точке принятия эффекта. | `b5.module.preserve-authority-across-failures` |
| <a id="assess-leadership-guarantees"></a>`b5.capability.assess-leadership-guarantees` | Оценивать границы согласования и смены лидера | `b5.cluster.consensus-leadership` | Выбирает модель agreement и progress для решений участников без реализации протокола. | `b5.module.preserve-authority-across-failures` |
| <a id="choose-state-placement"></a>`b5.capability.choose-state-placement` | Выбирать размещение и репликацию состояния | `b5.cluster.replication-sharding` | Связывает границу подтверждения с placement и независимостью отказов. | `b5.module.place-state-with-bounded-failure-cost` |
| <a id="plan-shard-ownership-transfer"></a>`b5.capability.plan-shard-ownership-transfer` | Определять безопасный перенос владения шардами | `b5.cluster.replication-sharding` | Описывает маршрутизацию и допустимые записи при partitioning и rebalancing. | `b5.module.place-state-with-bounded-failure-cost` |
| <a id="define-delivery-contract"></a>`b5.capability.define-delivery-contract` | Определять договор доставки и повторного чтения | `b5.cluster.messaging-events` | Разделяет queue/log, публикацию, acknowledgement, порядок и replay по потребителям. | `b5.module.compose-delivery-and-business-effects` |
| <a id="bound-repeat-effects"></a>`b5.capability.bound-repeat-effects` | Ограничивать бизнес-эффекты повторного исполнения | `b5.cluster.idempotency-retries` | Определяет идентичность операции, область дедупликации и жизненный цикл результата между участниками. | `b5.module.compose-delivery-and-business-effects` |
| <a id="control-retry-propagation"></a>`b5.capability.control-retry-propagation` | Ограничивать распространение повторов и poison work | `b5.cluster.idempotency-retries` | Определяет системные условия повторения, прекращения и изоляции неуспешной работы. | `b5.module.compose-delivery-and-business-effects` |
| <a id="bound-cache-staleness"></a>`b5.capability.bound-cache-staleness` | Определять системную границу устаревания cache | `b5.cluster.caching-load-control` | Сопоставляет пути обновления, invalidation и допустимую видимость между узлами. | `b5.module.bound-staleness-and-overload` |
| <a id="control-system-load"></a>`b5.capability.control-system-load` | Управлять нагрузкой и деградацией между участниками | `b5.cluster.caching-load-control` | Выбирает границы admission, rate limiting, backpressure и load shedding в системном потоке. | `b5.module.bound-staleness-and-overload` |
| <a id="compose-state-and-publication"></a>`b5.capability.compose-state-and-publication` | Согласовывать фиксацию состояния и публикацию | `b5.cluster.distributed-transactions` | Сравнивает transactional boundaries, outbox и CDC на уровне межсистемной гарантии. | `b5.module.compose-delivery-and-business-effects` |
| <a id="choose-cross-system-atomicity"></a>`b5.capability.choose-cross-system-atomicity` | Выбирать границу атомарности и компенсации | `b5.cluster.distributed-transactions` | Сопоставляет координированное решение и saga с бизнес-инвариантом и необратимыми эффектами. | `b5.module.compose-delivery-and-business-effects` |
| <a id="assess-regional-capacity"></a>`b5.capability.assess-regional-capacity` | Оценивать системную ёмкость и региональный компромисс | `b5.cluster.capacity-multi-region` | Связывает workload, locality, межрегиональную задержку и модель потери мощности. | `b5.module.place-state-with-bounded-failure-cost` |
| <a id="preserve-mixed-version-contract"></a>`b5.capability.preserve-mixed-version-contract` | Сохранять договор при смешанных версиях | `b5.cluster.evolution-verification` | Определяет совместимость смыслов и переходные состояния независимо меняющихся участников. | `b5.module.preserve-guarantees-through-change` |
| <a id="design-distinguishing-histories"></a>`b5.capability.design-distinguishing-histories` | Проектировать различающие проверки системной гарантии | `b5.cluster.evolution-verification` | Выбирает наблюдения, позволяющие отличить нарушение, допустимый исход и недостаток свидетельств. | `b5.module.preserve-guarantees-through-change` |

Разделение не является квотой: failure model и договор чтения имеют по одному действию; порядок и authority, placement и перенос владения, дедупликация и распространение retry, свежесть и нагрузка, публикация и компенсация, совместимость и проверка требуют разных результатов. Consensus и региональная ёмкость оставлены отдельными действиями в ограниченной модельной глубине.
