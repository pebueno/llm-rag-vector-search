# Module 1 — Agentic RAG

> LLM Zoomcamp 2026 · Week 1–2

Builds a Retrieval-Augmented Generation (RAG) pipeline from scratch and evolves it into a full **agentic loop** — where the LLM autonomously decides which tools to call, when to search again, and when it has enough context to answer.

---

## What is RAG?

Without RAG, an LLM answers purely from its training data — it can't know about your documents, your system, or anything that happened after its cutoff. RAG fixes this by:

1. Taking the user's question
2. Searching a knowledge base for relevant documents
3. Injecting those documents into the prompt as context
4. Letting the LLM generate a grounded answer

The result is an LLM that speaks about *your* data, not just its general knowledge.

---

## What is an Agentic Loop?

Standard RAG is one-shot: search once, answer once. An **agentic loop** lets the LLM decide:

- Which tool to call (search? query DB? call an API?)
- What arguments to pass (rewrite the query? filter by date?)
- Whether the results are good enough, or whether to search again
- When to stop and produce a final answer

This is implemented via **function/tool calling** — the LLM returns structured JSON describing which function to call. The host code executes it and feeds results back. Repeat until done.

```
User question
    ↓
LLM decides: call search_knowledge_base("motion detector sensitivity")
    ↓
Tool executes → returns 5 documents
    ↓
LLM decides: call query_events(event_type="alarm_triggered", days=7)
    ↓
Tool executes → returns 3 events
    ↓
LLM decides: enough context → generate final answer
    ↓
Answer returned to user
```

---

## Lessons

| Lesson | Topic |
|--------|-------|
| 1.1 | Introduction to RAG — problem framing, pipeline overview |
| 1.2 | Keyword search with minsearch — BM25-style in-memory indexing |
| 1.3 | Prompt engineering for RAG — context injection, system roles |
| 1.4 | LLM integration — Groq via OpenAI-compatible SDK |
| 1.5 | Function/tool calling — schema definition, JSON parsing |
| 1.6 | Agentic loop — multi-turn, multi-tool, termination logic |
| 1.7 | Persistent RAG — SQLite-backed indexes, stateful pipelines |

---

## Notebooks

| File | Description |
|------|-------------|
| `notebook.ipynb` | Core RAG pipeline — keyword search, prompt construction, Groq LLM |
| `persistent-rag.ipynb` | Stateful RAG with SQLite-backed vector store |
| `sqlite-ingest.ipynb` | Ingestion: embed documents and store in SQLite |
| `agents.ipynb` | Full agentic loop — tool calling, multi-turn, stop conditions |

## Key files

| File | Description |
|------|-------------|
| `rag_helper.py` | `RAGBase` class — reusable RAG pipeline with Groq chat completions |
| `ingest.py` | Document ingestion: chunking, embedding, storage |

---

## Technologies

| Tool | Role |
|------|------|
| **Groq** | LLM inference — free tier, fast, supports tool calling |
| **openai SDK** | Client library — Groq is OpenAI-API-compatible |
| **minsearch** | In-memory keyword search (BM25-style), zero infrastructure |
| **sentence-transformers** | Local embeddings — `all-MiniLM-L6-v2`, 384 dimensions |
| **SQLite** | Persistent local vector store for notebook experiments |
| **Python** | Tool execution host, prompt assembly, agentic loop logic |

---

## Key concepts

**Prompt template** — wraps retrieved context + user question into a structured prompt the LLM can reason over.

**Tool schema** — JSON Schema definition of a callable function. The LLM reads this and returns `{"name": "search", "arguments": {"query": "..."}}`.

**Max iterations** — safety limit on the agentic loop to prevent infinite tool-calling cycles.

**Query rewriting** — before searching, the LLM rewrites the user question into precise search terms. Reduces vocabulary mismatch between conversational queries and indexed documents.

---

## Running

```bash
cp .env.example .env   # add GROQ_API_KEY
uv sync
uv run jupyter notebook
```

---

## Applied in capstone

The agentic loop from `agents.ipynb` is the core of **[Sentinel AI](https://github.com/pebueno/sentinel-ai)**:

- `src/agent/loop.py` — production agentic loop (max 5 iterations, result truncation, empty-response fallback)
- `src/agent/tools.py` — two tools: `search_knowledge_base` (hybrid search) and `query_events` (SQL over event log)
