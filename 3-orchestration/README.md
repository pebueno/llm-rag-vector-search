# Module 3 — Orchestration

> LLM Zoomcamp 2026 · Week 4

Covers building reliable, reproducible pipelines for getting data into a RAG system — from raw documents to searchable embeddings — and orchestrating multi-step AI workflows where multiple agents collaborate on complex tasks.

---

## Why orchestration matters

A RAG system is only as good as its ingestion pipeline. Without orchestration:
- Re-running ingestion duplicates data
- Failures mid-pipeline leave the system in a broken state
- There's no visibility into what ran, when, and whether it succeeded
- Scaling to new data sources requires rewriting everything

**Orchestration** makes pipelines: idempotent, observable, schedulable, and composable.

---

## Lessons

| Lesson | Topic |
|--------|-------|
| 3.1 | Why context engineering matters — why generic LLMs fail on private data |
| 3.2 | Ingestion pipeline design — extract → chunk → embed → store |
| 3.3 | Idempotent pipelines — safe to re-run without duplicating data |
| 3.4 | Kestra introduction — flows, tasks, triggers, namespaces |
| 3.5 | RAG workflow in Kestra — orchestrated end-to-end ingestion |
| 3.6 | AI Copilot in Kestra — LLM-assisted flow generation |
| 3.7 | Autonomous agents — LLM makes multi-step decisions without fixed paths |
| 3.8 | Multi-agent systems — specialized agents collaborating on complex tasks |
| 3.9 | Production readiness — cost, security, observability, tool availability |

### Workshop: Data Ingestion with dlt

| Topic | Description |
|-------|-------------|
| dlt pipelines | Declarative data loading from filesystem, REST APIs |
| DuckDB | In-process analytical queries over loaded data |
| marimo dashboards | Interactive Python notebooks for LLM trace analysis |

---

## Technologies

| Tool | Role |
|------|------|
| **Kestra** | Open-source orchestration platform — YAML-defined flows, UI, scheduling |
| **dlt** | Declarative data loading library — sources, destinations, schemas |
| **DuckDB** | In-process OLAP database — fast analytical queries over ingested data |
| **marimo** | Reactive Python notebooks for data exploration |
| **Docker Compose** | Run Kestra + dependencies locally |
| **Python** | Pipeline logic, chunking, embedding generation |

---

## Key concepts

**Idempotency** — running a pipeline twice should produce the same result as running it once. Achieved via upserts, checksums, or deduplication on a unique key.

**Context engineering** — carefully designing what context the LLM receives. The wrong context produces hallucinations; the right context produces accurate answers. Orchestration controls how context is built.

**Autonomous agents** — unlike fixed RAG (search → answer), agents dynamically decide which tools to use, how many times, and in what order. Orchestration manages their lifecycle and retry logic.

**Multi-agent systems** — specialized agents (retriever, reasoner, validator, summarizer) collaborate. One agent's output becomes another's input. Orchestration defines the topology.

**Observability** — knowing whether your pipeline succeeded, how long each step took, and why it failed. Kestra provides this via a UI and structured logs.

---

## Running

```bash
docker compose up -d    # starts Kestra + dependencies
uv sync
uv run jupyter notebook
```

---

## Applied in capstone

The ingestion pipeline pattern is implemented in **[Sentinel AI](https://github.com/pebueno/sentinel-ai)**:

- `src/ingestion/generate_knowledge_base.py` — calls Groq to generate 60 security documents across 10 categories
- `src/ingestion/generate_events.py` — generates 2006 synthetic home security events
- `src/ingestion/ingest.py` — creates pgvector schema, embeds documents, loads all data
- `Makefile` — `make ingest` wraps all three steps as a reproducible pipeline
