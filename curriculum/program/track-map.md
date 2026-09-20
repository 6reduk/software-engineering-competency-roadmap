---
artifact: competency-map
status: accepted
updated: 2026-08-15
---

# Карта вертикальных треков

Программа организована в три слоя: инженерный фундамент, технические вертикали и интегрирующий leadership/architecture-трек. Вертикаль — не список библиотек, а законченная область ответственности с проектированием, реализацией, эксплуатацией и диагностикой.

## A. Инженерный фундамент

### A1. Computer Science & Problem Solving

Алгоритмы и структуры данных, оценка сложности, дискретные основы, базовая вероятность и статистика, численные представления, принципы ОС, процессы/потоки, память, файловые системы, конкурентность.

### A2. Software Engineering Practice

Git, дизайн и качество кода, тестирование, debugging, profiling, dependency management, API и backward compatibility, refactoring, документация, code review, CI/CD fundamentals.

### A3. Networks, Linux & Security Foundations

Linux, shell, процессы и права, TCP/IP, DNS, TLS, HTTP, reverse proxy, аутентификация/авторизация, секреты, threat modeling и базовая безопасность цепочки поставки.

## B. Технические вертикали

### B1. Python Engineering

Python language model, типизация, data model, итераторы и контекстные менеджеры, exceptions, packaging, async/concurrency/parallelism, performance, CPython internals и production-практики.

### B2. Backend & API Engineering

Проектирование сервисов и API, FastAPI, Pydantic, ASGI, HTTP, authentication, background work, интеграции, testing, performance, deployment и эволюция контрактов.

### B3. Transactional & Operational Data Systems

Реляционная модель и SQL, PostgreSQL, схемы и ограничения, транзакции и изоляция, MVCC, индексы, планы запросов, блокировки, миграции, репликация, partitioning, backup/recovery, эксплуатация и выбор operational SQL/NoSQL stores.

### B4. Data Engineering & Analytical Platforms

Batch/stream модели, форматы и качество данных, Spark, оркестрация через Airflow, lake/warehouse/lakehouse, BigQuery, Snowflake, partitioning/clustering, lineage, стоимость и эксплуатация data pipelines.

### B5. Distributed Systems & System Design

Consistency, availability, consensus на уровне практического понимания, очереди и event-driven системы, caching, sharding, idempotency, rate limiting, failure modes, capacity planning, multi-region и архитектурные компромиссы.

### B6. Platform, Cloud & Infrastructure Engineering

Контейнеры, Docker, Kubernetes, cloud primitives, IAM, networking, storage, Infrastructure as Code, release strategies, platform engineering, developer experience и управление стоимостью.

### B7. Reliability, Observability & Production Engineering

Логи, метрики, traces, SLI/SLO, alerting, incident response, postmortem, resilience, load/performance testing, capacity, disaster recovery и operational readiness.

### B8. Classical Machine Learning & Data Science

Постановка задачи, данные и leakage, статистические основы, feature engineering, scikit-learn, выбор метрик, validation, интерпретация, эксперименты и воспроизводимость.

### B9. Deep Learning & Foundation Models

Нейросетевые основы, optimization, PyTorch как основной framework, Keras 3 как обязательная multi-backend comparative API, TensorFlow-specific data/distribution/export/deployment capabilities, Hugging Face ecosystem, transformers, fine-tuning, inference и оценка моделей.

### B10. LLM Applications, Retrieval & Agentic Systems

Embeddings, chunking, retrieval, reranking, FAISS, Pinecone, RAG, structured output, tool use, agents/workflows, LangChain, evaluation, tracing, prompt/context engineering, security и cost/latency trade-offs.

### B11. MLOps & LLMOps

Experiment tracking, reproducibility, registry и lifecycle через MLflow; pipelines и ML-платформы через Kubeflow; orchestration boundaries с Airflow; deployment, monitoring, drift/evaluation; LMFlow для LLM fine-tuning и inference workflows. Docker/Kubernetes здесь применяются, но изучаются фундаментально в B6.

## C. Интегрирующая вертикаль

### C1. Engineering Leadership & Architecture

Работа с требованиями и ограничениями, ADR/RFC, архитектурные коммуникации, roadmap и техническая стратегия, build/buy, управление рисками и техническим долгом, межкомандные интерфейсы, миграции, governance, mentoring, incident leadership, экономика решений и влияние без формальной власти.

Этот трек начинается не после остальных, а идёт параллельно. Он регулярно использует кейсы и проекты из B1–B11.

## Размещение исходно названных технологий

| Технология | Основной трек | Связанные треки |
|---|---|---|
| Python | B1 | A1, A2, B2, B8–B11 |
| FastAPI | B2 | B1, B3, B6, B7 |
| scikit-learn | B8 | B3, B4, B11 |
| PyTorch, TensorFlow | B9 | B8, B11 |
| Hugging Face | B9 | B10, B11 |
| LangChain | B10 | B2, B11 |
| MLflow | B11 | B8, B9 |
| LMFlow | B11 | B9, B10 |
| Kubeflow | B11 | B6, B7 |
| Airflow | B4 | B11 |
| Docker, Kubernetes | B6 | B2, B7, B11 |
| PostgreSQL | B3 | B2, B5, B7 |
| Spark | B4 | B5, B6 |
| BigQuery, Snowflake | B4 | B3, B6 |
| FAISS, Pinecone | B10 | B3, B5, B6 |
