---
id: b4
kind: track
title: Data Engineering & Analytical Platforms
status: accepted
updated: 2026-08-14
language: ru
---

# B4 Data Engineering & Analytical Platforms

## Mission

Развить способность строить надёжные и экономически управляемые data pipelines и analytical platforms от источника до потребления.

## In scope

Batch/stream processing, Spark, Airflow, formats/lakes, BigQuery/Snowflake, data quality, lineage, governance и cost/performance.

## Non-goals

OLTP internals — B3; общие distributed algorithms — B5; инфраструктурная платформа — B6; ML modeling — B8; ML lifecycle — B11.

## Clusters

- `b4.cluster.data-contracts-quality` — schemas, contracts, validation и quality controls.
- `b4.cluster.batch-spark` — distributed batch execution, Spark и optimization.
- `b4.cluster.streaming-event-time` — streams, event time, windows и delivery semantics.
- `b4.cluster.orchestration-airflow` — DAGs, scheduling, retries, backfills и orchestration boundaries.
- `b4.cluster.formats-storage-lakes` — columnar formats, object storage, lakes и table formats.
- `b4.cluster.warehouses` — BigQuery, Snowflake, modeling, partitioning и clustering.
- `b4.cluster.lineage-governance` — metadata, lineage, ownership, privacy и retention.
- `b4.cluster.pipeline-reliability` — observability, replay, idempotency и recovery.
- `b4.cluster.performance-cost` — query/compute optimization и cost controls.
- `b4.cluster.serving-consumption` — marts, semantic boundaries и downstream contracts.

## Hard baseline prerequisites

A1 и A2 baseline.

## Conditional prerequisites

- SQL/warehouse-модули: B3 relational model, SQL и data modeling.
- Spark/Python-модули: B1 baseline.

## Strong connections

B5, B6, B7, B8, B11, C1.
