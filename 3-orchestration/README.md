# Module 3 — Orchestration

Building reliable ingestion pipelines: loading documents, generating embeddings, and loading into a vector store in a reproducible, automated way.

## What's covered

- Ingestion pipeline design: extract → transform → embed → load
- Idempotent pipelines — safe to re-run without duplicating data
- Scheduling and triggering pipelines (Kestra, cron, manual)
- Handling failures: retries, partial loads, progress tracking

## Notebooks

| File | Description |
|------|-------------|
| `01-ingestion-pipeline.ipynb` | End-to-end document ingestion pipeline |
| `02-scheduling.ipynb` | Scheduling pipelines with Kestra |

## Stack

- **Pipeline**: Python (`src/ingestion/`)
- **Orchestration**: Kestra (optional) or plain Python scripts
- **Storage**: PostgreSQL + pgvector

## Applied in capstone

The ingestion pipeline pattern from this module is implemented in **[Sentinel AI](https://github.com/pebueno/sentinel-ai)** — see `src/ingestion/ingest.py`, `src/ingestion/generate_knowledge_base.py`, and `src/ingestion/generate_events.py`.

## Running

```bash
cd 3-orchestration
uv sync
uv run jupyter notebook
```
