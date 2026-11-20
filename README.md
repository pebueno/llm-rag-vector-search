# LLM Zoomcamp 2026 — Pedro Ivo Bueno Sartório

My notebooks, homework and experiments from [LLM Zoomcamp 2026](https://github.com/DataTalksClub/llm-zoomcamp)
by DataTalks.Club: building RAG systems and agents, then measuring and operating them.

Every module folder has a README with the lesson map, homework answers, **decisions I made (and why)**, and
**findings**: results I measured that go beyond, or disagree with, the course text.

---

## Progress

| # | Module | Folder | Status | Highlights |
|---|--------|--------|--------|------------|
| 1 | Agentic RAG | [`1-rag/`](1-rag/) | ✅ lessons + homework | RAG from scratch, function calling, agent loop; context budgeting under free-tier limits |
| 2 | Vector Search | [`2-vector-search/`](2-vector-search/) | ✅ lessons | Embeddings, sqlitesearch, pgvector; ANN recall benchmark; IVFFlat experiment |
| 3 | Orchestration | [`3-orchestration/`](3-orchestration/) | ✅ lessons + homework | Kestra flows for RAG and agents; reasoning tokens vs token budgets |
| 4 | Evaluation | [`4-evaluation/`](4-evaluation/) | ✅ lessons + homework (incl. homework 2 search) | Hit Rate / MRR, validated boost tuning, calibrated LLM judge, truncation finding |
| 5 | Monitoring | [`5-monitoring/`](5-monitoring/) | ⏳ not started | — |
| 6 | Best Practices | — | ⏳ not started | Hybrid search, reranking, LangChain |
| 7 | Project | — | ⏳ not started | Capstone |

## Findings worth reading

1. **An IVFFlat index built on an empty table returns ~1 row instead of 5.** It reproduces my Sentinel AI project's
   0.068 vector hit rate, previously written off as normal for the corpus. [Module 2](2-vector-search/README.md#3-ivfflat-pitfalls-in-pgvector-and-the-bug-behind-sentinel-ais-vector-score)
2. **"Keyword beats vector" was partly a truncation artifact.** The ONNX tokenizer reads 128 of ~530 tokens per chunk.
   With that fixed, vector search overtakes keyword. [Module 4](4-evaluation/README.md#2-keyword-beats-vector-was-partly-a-truncation-artifact)
3. **The intuitive keyword boost was the worst one tested.** Validated on held-out data: +18% MRR. [Module 4](4-evaluation/README.md#1-the-intuitive-boost-was-the-worst-one)
4. **"Approximate" search can lose half the true neighbours.** LSH with default parameters: recall@5 = 0.52. [Module 2](2-vector-search/README.md#2-approximate-can-mean-losing-half-the-results)
5. **Reasoning models hide their cost in output tokens.** A "1–2 sentence" summary billed ~235 tokens. [Module 3](3-orchestration/README.md#why-q3q5-arent-clean-the-model-matters-more-than-the-prompt)

---

## Stack and course deviations

| | Course | Here | Why |
|---|--------|------|-----|
| LLM provider | OpenAI (`gpt-5.4-mini`) | [Groq](https://console.groq.com), `openai/gpt-oss-120b` | Free tier; OpenAI-compatible SDK with a different `base_url` |
| API | Responses API | `chat.completions` | Groq implements chat completions only |
| Kestra flows | Gemini | Course flows kept; Groq copies in `3-orchestration/flows/groq/` | Run without a Gemini key; one provider block differs |

Free-tier limits (1,000 requests/day, 8,000 tokens/minute) shaped several decisions. Each README documents where.

---

## Setup

Each module is its own [uv](https://docs.astral.sh/uv/) project:

```bash
cd <module-folder>
cp .env.example .env      # GROQ_API_KEY from console.groq.com (free)
uv sync
uv run jupyter notebook
```

Module 2 (pgvector) and module 3 (Kestra) also need Docker. See their READMEs.

---

## Related project

**[Sentinel AI](https://github.com/pebueno/sentinel-ai)**: a home-security assistant (FastAPI, Streamlit, pgvector,
Groq, Grafana) with an agentic RAG over an event log and a knowledge base. I built it before working through
modules 2–5. Each module README has a "Where this shows up in Sentinel AI" section that maps the course concepts
onto its code and lists the issues this study uncovered there.
