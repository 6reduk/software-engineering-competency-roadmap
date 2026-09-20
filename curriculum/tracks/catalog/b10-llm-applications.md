---
id: b10
kind: track
title: LLM Applications, Retrieval & Agentic Systems
status: accepted
updated: 2026-08-14
language: ru
---

# B10 LLM Applications, Retrieval & Agentic Systems

## Mission

Развить способность строить полезные, проверяемые и безопасные LLM-приложения с управляемыми quality, latency и cost.

## In scope

LLM interaction model, prompting/structured output/tools, embeddings, FAISS/Pinecone, retrieval/RAG, LangChain/workflows/agents, evaluation и production risks.

## Non-goals

Обучение моделей — B9; общая backend architecture — B2; database/distributed foundations — B3/B5; production ML lifecycle — B11.

## Clusters

- `b10.cluster.model-interaction` — tokens, context, decoding, limitations и uncertainty.
- `b10.cluster.prompting-structured-output` — instructions, schemas, validation и constrained outputs.
- `b10.cluster.tool-use-workflows` — tools, state, workflows и control boundaries.
- `b10.cluster.embeddings-similarity` — embedding models, distance, normalization и semantic limits.
- `b10.cluster.ingestion-chunking` — parsing, chunking, metadata и document lifecycle.
- `b10.cluster.vector-indexes` — FAISS, Pinecone, indexing, filtering и operational trade-offs.
- `b10.cluster.retrieval-reranking-rag` — retrieval strategies, reranking, context assembly и grounding.
- `b10.cluster.langchain-agentic-systems` — framework use, orchestration, memory/state и agent boundaries.
- `b10.cluster.evaluation` — offline/online evals, judges, datasets, regressions и human review.
- `b10.cluster.observability-cost-latency` — tracing, caching, routing, budgets и performance.
- `b10.cluster.security-safety` — prompt injection, data exposure, tool abuse и output risks.
- `b10.cluster.production-architecture` — fallback, vendor/model portability, quotas и graceful degradation.

## Hard baseline prerequisites

B1 и B2 baseline.

## Conditional prerequisites

- Evaluation-модули: соответствующие B8 concepts.
- Local models/fine-tuning/inference: соответствующие B9 capabilities.
- Stateful retrieval/distributed production: соответствующие B3/B5 concepts.

## Strong connections

B4, B6, B7, B11, C1.
