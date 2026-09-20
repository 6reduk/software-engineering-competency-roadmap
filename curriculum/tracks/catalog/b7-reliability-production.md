---
id: b7
kind: track
title: Reliability, Observability & Production Engineering
status: accepted
updated: 2026-08-15
language: ru
---

# B7 Reliability, Observability & Production Engineering

## Mission

Сформировать operational ownership: измерять надёжность, управлять изменениями и восстанавливать mission-critical системы на основе evidence.

## In scope

Observability, SLI/SLO, alerting/on-call, incidents, resilience, performance/capacity, DR, production readiness и operational learning.

## Non-goals

Инфраструктурная реализация и deployment/rollout mechanics — B6; контрактная эволюция конкретного сервиса — B2; store-specific backup/restore/PITR mechanics — B3; distributed design mechanisms — B5; конкретная service/data/ML observability остаётся также ответственностью соответствующего owner track; организационное лидерство — C1. B7 владеет cross-system RTO/RPO strategy, business continuity, DR exercises, production-readiness, change-safety и release-risk gate.

## Clusters

- `b7.cluster.observability-signals` — logs, metrics, traces, profiles и correlation.
- `b7.cluster.sli-slo-error-budgets` — user journeys, indicators, objectives и budgets.
- `b7.cluster.alerting-oncall` — actionable alerts, escalation и sustainable on-call.
- `b7.cluster.incident-response` — detection, coordination, mitigation и communication.
- `b7.cluster.resilience-patterns` — graceful degradation, isolation, failover и recovery.
- `b7.cluster.performance-capacity` — load testing, bottlenecks, capacity и saturation.
- `b7.cluster.dr-continuity` — RTO/RPO, backup validation и continuity exercises.
- `b7.cluster.production-readiness` — readiness reviews, change safety и release risk.
- `b7.cluster.postmortems-learning` — blameless analysis, corrective mechanisms и feedback loops.
- `b7.cluster.toil-automation` — toil measurement, automation и operational ergonomics.

## Hard baseline prerequisites

A2 и A3 baseline.

## Conditional prerequisites

- Advanced production architecture: соответствующие B5/B6 capabilities.

## Strong connections

B1, B2, B3, B4, B5, B6, B8, B9, B10, B11, C1.
