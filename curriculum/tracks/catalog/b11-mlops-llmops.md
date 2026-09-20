---
id: b11
kind: track
title: MLOps & LLMOps
status: accepted
updated: 2026-08-15
language: ru
---

# B11 MLOps & LLMOps

## Mission

Сформировать способность превращать ML/LLM experiments в воспроизводимый, управляемый и наблюдаемый production lifecycle.

## In scope

MLflow, LMFlow, Kubeflow, orchestration boundaries с Airflow, versioning/registry, deployment/serving, monitoring/evaluation и ML platform governance.

## Non-goals

Моделирование — B8/B9; LLM product logic — B10; общая data engineering — B4; контейнерная/cloud платформа — B6; общая SRE discipline — B7.

## Clusters

- `b11.cluster.experiment-tracking-mlflow` — runs, artifacts, lineage и reproducible comparison.
- `b11.cluster.data-feature-model-versioning` — datasets, feature definitions/stores, models, code, environments и provenance.
- `b11.cluster.registry-lifecycle` — model versions, aliases/tags, environment promotion, approvals, rollback и governance.
- `b11.cluster.training-pipelines-kubeflow` — components, pipelines, metadata и Kubernetes execution.
- `b11.cluster.orchestration-boundaries` — Airflow/Kubeflow responsibilities и event/schedule triggers.
- `b11.cluster.packaging-serving` — artifacts, containers, batch/online serving и rollout.
- `b11.cluster.monitoring-drift` — data/model drift, quality, latency и feedback loops.
- `b11.cluster.llm-evaluation-tracing` — prompts/models/retrieval versions, traces и eval gates.
- `b11.cluster.lmflow-workflows` — воспроизводимое исполнение, packaging и production integration LMFlow workloads для fine-tuning/inference; сам LMFlow не считается lifecycle-оркестратором, а algorithms и model/adaptation semantics остаются в B9.
- `b11.cluster.ml-platform-architecture` — self-service, tenancy, quotas и developer experience.
- `b11.cluster.governance-security-cost` — access, compliance, lineage, risk и economics.

## Hard baseline prerequisites

A2 и B6 baseline.

## Conditional prerequisites

- Data pipeline modules: соответствующие B4 capabilities.
- Classical ML lifecycle: соответствующие B8 capabilities.
- Training/foundation-model lifecycle: соответствующие B9 capabilities.
- LLM application lifecycle: соответствующие B10 capabilities.
- Advanced production monitoring: соответствующие B7 capabilities.

## Strong connections

B2, B5, C1.
