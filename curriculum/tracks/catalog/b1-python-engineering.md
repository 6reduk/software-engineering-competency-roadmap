---
id: b1
kind: track
title: Python Engineering
status: accepted
updated: 2026-08-15
language: ru
---

# B1 Python Engineering

## Mission

Развить способность писать, диагностировать и оптимизировать production Python, опираясь на корректную модель языка и runtime.

## In scope

Python data/object model, typing, language protocols, packaging, concurrency, CPython/runtime и Python-specific performance/tooling.

## Non-goals

Общие testing/design practices — A2; HTTP/service architecture — B2; deployment — B6; ML frameworks — B8–B11.

## Clusters

- `b1.cluster.object-data-model` — objects, names, identity, mutability, protocols и special methods.
- `b1.cluster.functions-scope-abstractions` — call model, closures, decorators и abstraction boundaries.
- `b1.cluster.typing-interfaces` — annotations, protocols, generics и gradual typing.
- `b1.cluster.iteration-laziness` — iterators, generators, comprehensions и lazy pipelines.
- `b1.cluster.errors-resources` — exceptions, context managers и deterministic cleanup.
- `b1.cluster.modules-packaging` — imports, environments, packaging и dependency isolation.
- `b1.cluster.concurrency-async-parallelism` — threads, processes, async, cancellation и synchronization.
- `b1.cluster.runtime-memory` — CPython execution, frames, allocation, reference counting и GC.
- `b1.cluster.metaprogramming-descriptors` — descriptors, class creation, introspection и controlled metaprogramming.
- `b1.cluster.performance-native-boundaries` — profiling, optimization, serialization и native/runtime boundaries.

## Hard baseline prerequisites

Нет.

## Conditional prerequisites

Нет.

## Strong connections

B2, B4, B8, B9, B10, B11.
