# Module 5 — Monitoring

> LLM Zoomcamp 2026 · Week 6

Production monitoring for LLM applications: logging every conversation, tracking quality degradation over time, collecting and acting on user feedback, and visualising system health in real-time dashboards.

---

## Why monitoring matters

Evaluation (module 4) tells you how good your system is *before* deployment. Monitoring tells you how it's performing *after* — with real users, real questions, and real edge cases that your test set never covered.

Without monitoring:
- You don't know when answer quality degrades
- You can't tell which questions the system struggles with
- You have no signal to guide future improvements
- Incidents are discovered by users, not by you

---

## What to monitor

| Category | Signals |
|----------|---------|
| **Quality** | Relevance score (LLM judge), user feedback (thumbs up/down), follow-up rate |
| **Performance** | Response time (p50, p95, p99), token usage, agent iterations |
| **Reliability** | Error rate, timeout rate, tool call failures |
| **Cost** | Input + output tokens per query, total daily spend |
| **Usage** | Queries per day, unique users, most common question types |

---

## Lessons

| Lesson | Topic |
|--------|-------|
| 5.1 | Monitoring strategy — what to measure and why |
| 5.2 | Conversation logging — PostgreSQL schema for conversation history |
| 5.3 | User feedback integration — thumbs up/down, rating widgets |
| 5.4 | Online LLM-as-judge — scoring every response automatically post-generation |
| 5.5 | Grafana setup — connecting to PostgreSQL, auto-provisioning via YAML |
| 5.6 | Dashboard design — 5 essential panels for LLM monitoring |
| 5.7 | Streamlit dashboards — custom Python charts for product teams |
| 5.8 | Alerting — threshold-based alerts on quality degradation |
| 5.9 | Feedback loops — using production signals to improve retrieval and prompts |

---

## Technologies

| Tool | Role |
|------|------|
| **PostgreSQL** | Central store for all conversation + monitoring data |
| **Grafana** | Production-grade dashboard — connects directly to PostgreSQL |
| **Streamlit** | Custom Python dashboards — faster to build, more flexible layout |
| **psycopg2** | Python → PostgreSQL driver |
| **JSONB** | PostgreSQL JSON column type — stores tool call logs without schema migration |
| **SentenceTransformers** | Embed answers for cosine similarity scoring |
| **Docker Compose** | Run Grafana + PostgreSQL as managed services |

---

## Conversation schema

Every conversation logged to PostgreSQL includes:

```sql
CREATE TABLE conversations (
    id              SERIAL PRIMARY KEY,
    timestamp       TIMESTAMPTZ,
    question        TEXT,
    answer          TEXT,
    model           TEXT,
    iterations      INTEGER,       -- how many agent tool calls
    tool_calls      JSONB,         -- full tool call log
    input_tokens    INTEGER,
    output_tokens   INTEGER,
    response_time   FLOAT,
    feedback        SMALLINT,      -- 1 = thumbs up, -1 = thumbs down
    relevance_score TEXT,          -- LLM judge: RELEVANT / PARTLY_RELEVANT / NOT_RELEVANT
    relevance_reason TEXT
);
```

---

## Grafana

Grafana connects directly to PostgreSQL and auto-provisions dashboards via YAML — no manual panel configuration:

```
grafana/
├── provisioning/
│   ├── datasources/postgres.yml    # DB connection
│   └── dashboards/dashboards.yml   # folder mapping
└── dashboards/
    └── sentinel.json               # dashboard definition (panels, queries)
```

Key panels:
- **Total conversations** — stat card with total count
- **Avg response time** — with colour thresholds (green/yellow/red)
- **Conversations per day** — time series with `date_trunc('day', timestamp)`
- **Relevance distribution** — pie chart of RELEVANT / PARTLY / NOT_RELEVANT
- **Token usage** — input + output tokens over time
- **Response time trend** — scatter for spotting slowdowns

---

## Key concepts

**Online vs offline evaluation** — offline uses a fixed test set; online monitors every real request. Both are necessary.

**Feedback signal** — user thumbs up/down is the most direct quality signal. Even 5% feedback rate across thousands of queries provides statistically significant data.

**Quality drift** — model providers update models without notice, retrieval indexes go stale, user question patterns shift. Monitoring catches drift before users complain.

**SLO (Service Level Objective)** — define targets before going live: e.g. p95 response time < 30s, relevance score RELEVANT > 60%. Dashboard alerts when you breach them.

---

## Running

```bash
docker compose up postgres grafana -d
uv sync
uv run jupyter notebook

# Grafana UI
open http://localhost:3000   # admin / admin
# Dashboards → Sentinel → Sentinel AI Monitoring
```

---

## Applied in capstone

Full monitoring stack in **[Sentinel AI](https://github.com/pebueno/sentinel-ai)**:

- `src/monitoring/database.py` — `save_conversation()`, `save_feedback()`, `save_relevance_score()`, `get_dashboard_stats()`
- `src/monitoring/judge.py` — LLM judge called automatically after every `/ask` response
- `app/dashboard.py` — Streamlit dashboard with 6 live charts
- `grafana/dashboards/sentinel.json` — auto-provisioned Grafana dashboard with 9 panels
- `grafana/provisioning/` — YAML datasource + folder config, zero manual setup
