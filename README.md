# LLM Zoomcamp 2026 — Pedro Ivo Bueno Sartório

Exercises, notebooks, and notes from [LLM Zoomcamp 2026](https://github.com/DataTalksClub/llm-zoomcamp) by DataTalks.Club.

All modules use **Groq** (free tier) instead of OpenAI, adapted via the `openai` SDK with a custom `base_url`.

---

## Modules

| # | Module | Topics | Folder |
|---|--------|--------|--------|
| 1 | [RAG + Agentic Pipelines](1-rag/) | Retrieval-Augmented Generation, function calling, agentic loops | `1-rag/` |
| 2 | [Vector Search](2-vector-search/) | Embeddings, pgvector, similarity search, indexing strategies | `2-vector-search/` |
| 3 | [Orchestration](3-orchestration/) | Ingestion pipelines, workflow automation, data loading | `3-orchestration/` |
| 4 | [Evaluation](4-evaluation/) | Retrieval metrics, LLM-as-a-judge, Hit Rate, MRR | `4-evaluation/` |
| 5 | [Monitoring](5-monitoring/) | PostgreSQL logging, Grafana dashboards, feedback loops | `5-monitoring/` |

---

## Capstone Project

All module concepts are applied end-to-end in the capstone:

**[Sentinel AI — Home Security Intelligence Assistant](https://github.com/pebueno/sentinel-ai)**

A production-grade agentic RAG system that lets you query your home security event logs and knowledge base in plain English. Built with FastAPI, Streamlit, pgvector, Groq, and Grafana.

---

## Setup

Each module has its own `pyproject.toml`. Navigate into the module folder and run:

```bash
uv sync         # install dependencies
uv run jupyter notebook   # open notebooks
```

Requires a [Groq API key](https://console.groq.com) (free) set as `GROQ_API_KEY` in a `.env` file.
