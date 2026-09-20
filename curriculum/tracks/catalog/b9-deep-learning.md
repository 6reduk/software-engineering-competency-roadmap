---
id: b9
kind: track
title: Deep Learning & Foundation Models
status: accepted
updated: 2026-08-15
language: ru
---

# B9 Deep Learning & Foundation Models

## Mission

Сформировать способность обучать, адаптировать, оценивать и эффективно исполнять neural/foundation models, понимая математические и системные ограничения.

## In scope

Neural foundations, PyTorch как основной framework, Keras 3 multi-backend API, TensorFlow-specific ecosystem/runtime capabilities, training systems, transformers, Hugging Face, fine-tuning и inference optimization.

## Non-goals

Classical ML/evaluation baseline — B8; application RAG/agents — B10; lifecycle/platform — B11; общий Kubernetes — B6.

## Clusters

- `b9.cluster.tensors-autodiff` — tensors, computation graphs, gradients и autodiff.
- `b9.cluster.architectures-representations` — MLP/CNN/RNN/attention и representation learning.
- `b9.cluster.optimization-regularization` — losses, optimizers, initialization, regularization и stability.
- `b9.cluster.pytorch-core` — modules, autograd, datasets, training loops и compilation.
- `b9.cluster.tensorflow-keras` — Keras 3 multi-backend portability и comparative workflows; TensorFlow-specific data, distribution, export/deployment и ecosystem boundaries.
- `b9.cluster.training-systems` — data loading, checkpoints, mixed precision и reproducibility.
- `b9.cluster.distributed-training` — data/model parallelism, communication и scaling constraints.
- `b9.cluster.transformers-foundation-models` — architecture, tokenization, pretraining и model families.
- `b9.cluster.hugging-face-ecosystem` — models, datasets, tokenizers, Trainer и Hub boundaries.
- `b9.cluster.finetuning-adaptation` — transfer learning, PEFT, instruction tuning и adaptation choices.
- `b9.cluster.inference-evaluation` — serving formats, batching, quantization, latency и model evaluation.

## Hard baseline prerequisites

A1, B1 и B8.

## Conditional prerequisites

Нет.

## Strong connections

B4, B6, B7, B10, B11, C1.
