---
id: b3
kind: track
title: Transactional & Operational Data Systems
status: accepted
updated: 2026-08-15
language: ru
---

# B3 Transactional & Operational Data Systems

## Mission

Сформировать способность выбирать, проектировать, использовать и эксплуатировать operational data stores, сохраняя глубокую PostgreSQL/relational основу.

## In scope

Реляционная модель, SQL, transactions/MVCC, storage/index/optimizer, migrations, replication, partitioning, recovery и выбор operational non-relational store.

## Non-goals

Application persistence architecture — B2; analytical warehouses/Spark — B4; распределённые алгоритмы и общая consistency theory — B5; cross-system RTO/RPO strategy, business continuity и DR exercises — B7; vector retrieval — B10. B3 владеет store-specific backup/restore/PITR mechanics и проверкой восстанавливаемости данных.

## Clusters

- `b3.cluster.relational-model-schema` — relations, keys, constraints, normalization и data modeling.
- `b3.cluster.sql-querying` — SQL semantics, joins, aggregation, windows и query composition.
- `b3.cluster.transactions-concurrency` — ACID, isolation, MVCC, locks, anomalies и deadlocks.
- `b3.cluster.storage-wal-recovery` — pages, WAL, checkpoints и crash recovery.
- `b3.cluster.indexes-optimizer` — index structures, plans, statistics и cardinality.
- `b3.cluster.schema-evolution` — migrations, compatibility и online changes.
- `b3.cluster.replication-ha` — replication, failover и consistency implications.
- `b3.cluster.partitioning-scaling` — partitioning, connection scaling и границы vertical/horizontal scale.
- `b3.cluster.backup-restore-dr` — backup, restore, PITR и disaster recovery.
- `b3.cluster.security-operations` — access, auditing, maintenance и operational diagnostics.
- `b3.cluster.operational-nonrelational-stores` — key-value, document, wide-column и search stores; data/query/consistency/operations trade-offs и выбор SQL/NoSQL.

## Hard baseline prerequisites

Нет.

## Conditional prerequisites

- Эксплуатационные модули: A3 Linux/network/security baseline.

## Strong connections

B2, B4, B5, B6, B7, B10, C1.
