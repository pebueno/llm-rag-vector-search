# Module 5 — Monitoring

> LLM Zoomcamp 2026 · [course module](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/05-monitoring) · [homework spec](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/homework/05-monitoring/homework.md)

**Status: not started.** No code in this folder yet.

## What the module covers

Offline evaluation ([module 4](../4-evaluation/)) can't show how a RAG system behaves with real users. This module
builds online monitoring: a Streamlit chat app, per-call metrics (tokens, cost, latency), conversations stored in
PostgreSQL, thumbs-up/down feedback, a built-in LLM judge, and Streamlit and Grafana dashboards.

| # | Lesson |
|---|--------|
| 01 | Intro |
| 02 | Assistant setup |
| 03 | Chat app (Streamlit) |
| 04 | Capturing metrics (`LLMCallRecord`, cost) |
| 05 | Database (PostgreSQL, saving conversations) |
| 06 | Querying data |
| 07 | Streamlit dashboard |
| 08 | User feedback |
| 09 | Built-in judge |
| 10 | Feedback dashboard |
| 11 | Synthetic data |
| 12 | Grafana dashboards |
| 13 | Docker Compose |
| 14 | Next steps (OpenTelemetry, alerting) |

The homework instruments the module 1 RAG with **OpenTelemetry** traces, persists spans to SQLite and builds a
dashboard from them.

## Carried over from earlier modules

- Reasoning models bill hidden tokens as output ([module 3](../3-orchestration/README.md)), so cost tracking must use reported usage, not text length.
- An online judge needs the calibration check from [module 4](../4-evaluation/README.md#4-a-judge-has-to-be-tested-before-it-is-trusted) before its scores go on a dashboard.
