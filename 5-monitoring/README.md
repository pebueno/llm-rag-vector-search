# Module 5 — Monitoring

Production monitoring for LLM applications: logging every conversation to PostgreSQL, tracking quality metrics over time, and visualising them in Grafana and Streamlit dashboards.

## What's covered

- Storing conversations: question, answer, model, tokens, response time, feedback
- User feedback loops: thumbs up/down linked to conversation records
- LLM judge integration: scoring every answer automatically after generation
- Grafana: auto-provisioned dashboards via YAML, querying PostgreSQL directly
- Streamlit dashboards: custom Python charts for product-facing monitoring

## What to monitor

| Metric | Why it matters |
|--------|---------------|
| Response time | Detect slowdowns, timeout thresholds |
| Token usage | Cost tracking, context window pressure |
| Relevance score | Answer quality over time (LLM judge) |
| User feedback | Ground truth signal from real users |
| Agent iterations | How many tool calls per question (efficiency) |

## Grafana setup

Dashboard is auto-provisioned from YAML — no manual panel creation needed:

```bash
docker compose up grafana -d
# open localhost:3000 (admin/admin)
# Dashboards → Sentinel → Sentinel AI Monitoring
```

## Applied in capstone

Full monitoring stack in **[Sentinel AI](https://github.com/pebueno/sentinel-ai)** — see `src/monitoring/database.py`, `src/monitoring/judge.py`, `app/dashboard.py`, and `grafana/`.

## Running

```bash
cd 5-monitoring
docker compose up postgres grafana -d
uv sync
uv run jupyter notebook
```
