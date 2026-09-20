---
id: b5
kind: track
title: Distributed Systems & System Design
status: accepted
updated: 2026-08-15
language: ru
---

# B5 Distributed Systems & System Design

## Mission

Сформировать способность проектировать системы, корректно работающие при частичных отказах, конкуренции, масштабировании и эволюции.

## In scope

Distributed guarantees, coordination, replication/sharding, messaging, failure handling, общие механизмы и trade-offs caching/load control, multi-region и system design.

## Non-goals

Протокольный/network baseline — A3; DB-engine specifics — B3; применение cache и API abuse/throttling controls на service boundary — B2; cloud/Kubernetes implementation — B6; SRE process — B7; организационная стратегия — C1.

## Clusters

- `b5.cluster.failure-models` — partial failure, timeouts, partitions и uncertainty.
- `b5.cluster.consistency-availability` — consistency models, availability и CAP/PACELC reasoning.
- `b5.cluster.time-order-coordination` — clocks, ordering, leases и coordination.
- `b5.cluster.consensus-leadership` — consensus, leader election и practical boundaries.
- `b5.cluster.replication-sharding` — placement, replication, partitioning и rebalancing.
- `b5.cluster.messaging-events` — queues, logs, event-driven design и delivery semantics.
- `b5.cluster.idempotency-retries` — retries, deduplication, idempotency и poison work.
- `b5.cluster.caching-load-control` — системные модели, механизмы и trade-offs caching, rate limiting, load shedding и backpressure; прикладная интеграция в backend-сервис принадлежит B2.
- `b5.cluster.distributed-transactions` — sagas, outbox, CDC и transactional boundaries.
- `b5.cluster.capacity-multi-region` — capacity, geo-distribution, failover и data locality.
- `b5.cluster.evolution-verification` — compatibility, failure testing и architecture validation.

## Hard baseline prerequisites

A1 и A3 baseline.

## Conditional prerequisites

- Backend/data case studies: соответствующие B2/B3 concepts.

## Strong connections

B2, B3, B4, B6, B7, B10, B11, C1.
