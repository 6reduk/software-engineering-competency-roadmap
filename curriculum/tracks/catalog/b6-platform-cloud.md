---
id: b6
kind: track
title: Platform, Cloud & Infrastructure Engineering
status: accepted
updated: 2026-08-15
language: ru
---

# B6 Platform, Cloud & Infrastructure Engineering

## Mission

Развить способность создавать воспроизводимую, безопасную и удобную платформу выполнения сервисов и data/ML workloads.

## In scope

Docker, Kubernetes, cloud primitives, IAM, IaC, delivery strategies, platform engineering, scheduling/autoscaling и infrastructure economics.

## Non-goals

Linux/network/security и supply-chain threat-model baseline — A3; application architecture и совместимость API-контракта при изменении — B2; distributed guarantees — B5; release risk gate, SLO и incidents — B7; ML lifecycle — B11. B6 владеет platform enforcement: build provenance, scanning/signing, admission controls, CI/CD, promotion и deployment/rollout mechanics.

## Clusters

- `b6.cluster.containers-docker` — images, runtime isolation, networking, storage и build practices.
- `b6.cluster.kubernetes-workloads` — control plane model, workloads, services, config и storage.
- `b6.cluster.cloud-primitives` — compute, network, storage, managed services и shared responsibility.
- `b6.cluster.iam-secrets-policy` — identities, permissions, secrets и policy enforcement.
- `b6.cluster.iac-configuration` — declarative infrastructure, state, drift и environments.
- `b6.cluster.delivery-strategies` — CI/CD integration, rollout, rollback и promotion.
- `b6.cluster.platform-golden-paths` — self-service, paved roads, APIs и developer experience.
- `b6.cluster.scheduling-autoscaling` — requests/limits, scheduling, autoscaling и quotas.
- `b6.cluster.supply-chain` — artifact provenance, scanning, signing и admission controls.
- `b6.cluster.capacity-cost` — capacity planning, utilization и FinOps boundaries.

## Hard baseline prerequisites

A2 и A3 baseline.

## Conditional prerequisites

- Advanced scaling/resilience: соответствующие B5 capabilities.

## Strong connections

B2, B4, B7, B9, B10, B11, C1.
