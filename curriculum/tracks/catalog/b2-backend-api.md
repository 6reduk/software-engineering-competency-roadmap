---
id: b2
kind: track
title: Backend & API Engineering
status: accepted
updated: 2026-08-15
language: ru
---

# B2 Backend & API Engineering

## Mission

Научить проектировать, реализовывать и эволюционировать backend-сервисы и API с корректными контрактами, безопасностью, производительностью и operational ownership.

## In scope

Service boundaries, HTTP/API semantics, FastAPI/Pydantic/ASGI, validation/errors, auth integration, persistence/messaging integration, безопасная интеграция application cache, API abuse/throttling controls на service boundary, testing и service evolution.

## Non-goals

Язык Python как таковой — B1; теория БД и cache-store semantics — B3; общие distributed guarantees и механизмы caching/load control — B5; deployment/rollout mechanics и platform IAM/network controls — B6; release risk gates и общая SRE discipline — B7. B2 владеет контрактной эволюцией сервиса, размещением и наблюдаемым поведением cache, quota/rate/abuse controls внутри приложения и на границе сервиса.

## Clusters

- `b2.cluster.request-runtime` — request lifecycle, ASGI, middleware и resource scopes.
- `b2.cluster.api-contracts` — HTTP semantics, resource modeling, compatibility и versioning.
- `b2.cluster.validation-serialization-errors` — schemas, validation, serialization и error contracts.
- `b2.cluster.identity-access-boundaries` — authn/authz integration и tenant boundaries.
- `b2.cluster.service-architecture` — layers, dependencies, domain boundaries и modularity.
- `b2.cluster.persistence-transactions` — repositories, units of work и transaction boundaries.
- `b2.cluster.async-background-integration` — async I/O, background work, messaging и external calls.
- `b2.cluster.testing-contracts` — unit/integration/contract/E2E testing сервиса.
- `b2.cluster.performance-resource-control` — latency, throughput, connection pools, limits и backpressure.
- `b2.cluster.evolution-delivery` — migrations, rollout, backward compatibility и deprecation.

## Hard baseline prerequisites

B1 и A3 baseline.

## Conditional prerequisites

- Persistence-модули: B3 relational model, SQL и transaction boundaries.

## Strong connections

A2, B3, B5, B6, B7, B10, C1.
