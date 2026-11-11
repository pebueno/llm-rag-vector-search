# Module 2 — Vector Search

> LLM Zoomcamp 2026 · [course module](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/02-vector-search) · [homework spec](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/homework/02-vector-search/homework.md)

Module 1 searched by **words** (keyword search). This module searches by **meaning**. An embedding model
turns each text into a 384-number vector, and texts with similar meaning end up close together. The module
then scales that from a numpy matrix to a persistent index and to Postgres.

---

## What's in this folder

| File | What it does | Course lessons |
|------|--------------|----------------|
| [`vector_search.ipynb`](vector_search.ipynb) | Embeddings, embedding the FAQ, brute-force search with numpy, minsearch `VectorSearch`, RAG with vector search | 02–06 |
| [`vector_search_persistent.ipynb`](vector_search_persistent.ipynb) | sqlitesearch: ingest once to disk, reopen without re-embedding, RAG. **Extra:** recall benchmark of LSH / IVF / HNSW | 07 |
| [`vector_search_pgvector.ipynb`](vector_search_pgvector.ipynb) | Postgres + pgvector: schema, cosine search with SQL filters, RAG. **Extra:** IVFFlat recall experiment | 08 |
| [`docker-compose.yml`](docker-compose.yml) | `pgvector/pgvector:pg17`, host port from `PG_PORT` | 08 |
| `ingest.py`, `rag_helper.py` | Copied from [module 1](../1-rag/) so this module is self-contained, as in the course | — |

---

## Core idea

```
"Can I still join the course?"      ──► [0.02, -0.11, 0.07, …]  ─┐
"I just found the program, enroll?" ──► [0.03, -0.09, 0.06, …]  ─┤  close together  → similar meaning
"How do I install Docker?"          ──► [-0.08, 0.14, -0.01, …] ─┘  far away
```

- **Model:** `all-MiniLM-L6-v2` (384 dimensions, CPU-friendly, ~80 MB).
- **Similarity:** the model outputs unit-length vectors, so dot product = cosine similarity.
- **Brute-force search:** `scores = X.dot(q)`, one matrix-vector product, exact.
- **ANN search:** approximate nearest neighbours. It narrows to a candidate region first, which is faster at scale but can miss true neighbours.

---

## Findings

These go beyond the lessons. Each was measured in the notebooks, not taken from the course text.

### 1. Vector search helps on paraphrases, but modestly on this data
On "the program has already begun, can I still sign up?", keyword search puts the right FAQ at **#2** and
vector search at **#1**. The bigger difference is in the other hits. Keyword search returns entries that
share words ("can I still *submit*…"); vector search returns entries on the same topic. That matches
the course's advice: start with keyword search and add vectors only when evaluation shows misses.

### 2. "Approximate" can mean losing half the results
Recall@5 against exact search, sqlitesearch, 1,489 docs, default parameters:

| mode | recall@5 |
|------|----------|
| `lsh` | 0.52 |
| `ivf` | 0.88 |
| `hnsw` | ~1.00 |

The lesson says `lsh` is fine for small datasets. With default parameters it misses ~48% of the true
neighbours here. At this size brute force takes under a millisecond, so ANN only costs recall.

### 3. IVFFlat pitfalls in pgvector, and the bug behind Sentinel AI's vector score
Recall@5 against exact search (full table in the notebook):

| setup | recall@5 | rows returned (of 5) |
|-------|----------|----------------------|
| no index (exact) | 1.00 | 5.0 |
| HNSW, forced | ~1.00 | 5.0 |
| IVFFlat after insert, `probes=1` | ~0.6 | 4.9 |
| IVFFlat after insert, `probes=10` | ~0.93 | 5.0 |
| IVFFlat created on **empty** table | 0.17 | 4.9 |
| 60 rows, IVFFlat on empty table, **no `ANALYZE`** | **0.05** | **1.1** |

The last row is exactly how [Sentinel AI](https://github.com/pebueno/sentinel-ai) ingests its 60-document
knowledge base (`CREATE INDEX … ivfflat` before the `INSERT`, no `ANALYZE`). It reproduces the
**0.068 vector Hit Rate** Sentinel reported, which had been written off as a corpus characteristic.
With fresh statistics, Postgres ignores the index on tables this small and recall is 1.0. So the low score
comes from the index, not from vector search. Follow-up for Sentinel: drop the IVFFlat index (exact scan of 60 rows)
and re-run its retrieval evaluation.

General lessons:
- run `EXPLAIN`, because the planner, not `CREATE INDEX`, decides whether an index is used;
- build IVFFlat after loading data, with `lists ≈ rows/1000`, and tune `ivfflat.probes`;
- run `ANALYZE` after bulk loads;
- measure recall against exact search before trusting any ANN index.

---

## Decisions and deviations

| Decision | Why |
|----------|-----|
| CPU-only PyTorch index in `pyproject.toml` | The default `torch` wheel pulls several GB of CUDA libraries. CPU-only keeps the env at ~1.2 GB. |
| `executemany` for pgvector inserts | The lesson inserts row by row. One batched call does the same with far fewer round-trips. |
| `RAGPgVector` takes the search function | The lesson copies the SQL into the class. Passing `pgvector_search` keeps one query definition. |
| `PG_PORT` env var for the host port | 5432 is often taken by other local Postgres instances. Compose and notebook read the same variable. |
| Groq `openai/gpt-oss-120b` for the RAG calls | Same provider and model as [module 1](../1-rag/README.md#decisions-and-deviations-from-the-course). |
| ONNX embedder (lesson 09) done in homework 2 | The homework uses it as the main embedder, so it lives there. |

---

## Running

```bash
cd 2-vector-search
cp .env.example .env          # GROQ_API_KEY; set PG_PORT if 5432 is taken
uv sync
docker compose --env-file .env up -d     # only for vector_search_pgvector.ipynb
uv run jupyter notebook
```

---

## Where this shows up in Sentinel AI

- [`src/search/vector_search.py`](https://github.com/pebueno/sentinel-ai/blob/master/src/search/vector_search.py): pgvector cosine search (`<=>`) with an optional `WHERE category = …` filter. Same pattern as `pgvector_search` here.
- [`src/search/keyword_search.py`](https://github.com/pebueno/sentinel-ai/blob/master/src/search/keyword_search.py): minsearch `Index`, as in module 1.
- [`src/search/hybrid_search.py`](https://github.com/pebueno/sentinel-ai/blob/master/src/search/hybrid_search.py): Reciprocal Rank Fusion (k=60) of both. Hybrid search is course [module 6](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/06-best-practices).
- [`src/ingestion/ingest.py`](https://github.com/pebueno/sentinel-ai/blob/master/src/ingestion/ingest.py): the IVFFlat-before-insert setup analysed in finding 3.

---

## References

- Course module: [02-vector-search](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/02-vector-search)
- [sentence-transformers](https://www.sbert.net/) · [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [minsearch](https://github.com/alexeygrigorev/minsearch) · [sqlitesearch](https://github.com/alexeygrigorev/sqlitesearch)
- [pgvector README: indexing (IVFFlat, HNSW)](https://github.com/pgvector/pgvector#indexing)
- Malkov & Yashunin, [HNSW paper](https://arxiv.org/abs/1603.09320) (2016)
