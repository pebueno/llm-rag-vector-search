# Module 1 — RAG + Agentic Pipelines

Builds a Retrieval-Augmented Generation pipeline from scratch, then extends it into a full agentic loop where the LLM decides which tools to call and when to stop.

## What's covered

- **Lesson 1-2**: Basic RAG — search → prompt → LLM answer
- **Lesson 3**: Replacing minsearch with a persistent vector store (SQLite → pgvector)
- **Lesson 4-5**: Function/tool calling via Groq's chat completions API
- **Lesson 6-7**: Full agentic loop — multi-turn, multi-tool, iterative reasoning

## Notebooks

| File | Description |
|------|-------------|
| `notebook.ipynb` | Core RAG pipeline — keyword search, prompt construction, Groq LLM |
| `persistent-rag.ipynb` | Persistent RAG with SQLite-backed vector store |
| `sqlite-ingest.ipynb` | Ingestion pipeline: embed documents and store in SQLite |
| `agents.ipynb` | Agentic loop with tool calling — LLM drives search decisions |

## Key files

| File | Description |
|------|-------------|
| `rag_helper.py` | `RAGBase` class — reusable RAG pipeline with Groq chat completions |
| `ingest.py` | Document ingestion: chunking, embedding, storage |

## Stack

- **LLM**: Groq (`qwen/qwen3.6-27b`) via `openai` SDK with `base_url` override
- **Keyword search**: minsearch (in-memory BM25-style)
- **Vector search**: sentence-transformers (`all-MiniLM-L6-v2`, 384-dim)
- **Storage**: SQLite (local) + PostgreSQL/pgvector (persistent)

## Applied in capstone

The agentic loop pattern from this module (`agents.ipynb`) is the core of **[Sentinel AI](https://github.com/pebueno/sentinel-ai)** — see `src/agent/loop.py` and `src/agent/tools.py`.

## Running

```bash
cd 1-rag
cp .env.example .env   # add GROQ_API_KEY
uv sync
uv run jupyter notebook
```
