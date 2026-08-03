# Module 2 — Vector Search

> LLM Zoomcamp 2026 · Week 3

Covers semantic search using dense vector embeddings — how to represent text as numbers that capture meaning, how to find similar documents without exact keyword matching, and how to scale from in-memory experiments to production PostgreSQL storage.

---

## Why vector search?

Keyword search finds documents that share words with your query. Vector search finds documents that share *meaning*. 

Example: the query `"how to stop a burglar"` won't match a document titled `"intruder detection best practices"` via keyword search — but in vector space both map to nearly the same point, so they rank highly together.

This matters for RAG because user questions are conversational and documents are formal — they rarely share exact vocabulary.

---

## How embeddings work

A sentence embedding model (e.g. `all-MiniLM-L6-v2`) converts any text into a fixed-size vector of floats:

```
"motion detected at front door" → [0.12, -0.34, 0.87, ..., 0.05]  # 384 dimensions
```

Similar sentences produce vectors that are geometrically close. Similarity is measured by:
- **Cosine similarity** — angle between vectors (most common for text)
- **Dot product** — cosine × magnitude (faster for normalized vectors)
- **L2 distance** — Euclidean distance (used by some indexes)

---

## Lessons

| Lesson | Topic |
|--------|-------|
| 2.1 | Embeddings fundamentals — text to vectors, semantic space |
| 2.2 | In-memory vector search with NumPy — cosine similarity from scratch |
| 2.3 | minsearch — lightweight BM25 + vector hybrid |
| 2.4 | SQLiteSearch — persistent local vector indexing |
| 2.5 | pgvector — PostgreSQL extension for production vector search |
| 2.6 | ONNX Runtime — lightweight embedding without PyTorch overhead |
| 2.7 | Indexing strategies — HNSW vs IVFFlat: speed vs recall tradeoffs |
| 2.8 | Hybrid retrieval — vector + keyword combined, score fusion |

---

## Technologies

| Tool | Role |
|------|------|
| **sentence-transformers** | Generate dense embeddings locally (`all-MiniLM-L6-v2`, 384-dim) |
| **ONNX Runtime** | Lighter alternative to PyTorch for embedding inference |
| **NumPy** | Vector operations, cosine similarity from scratch |
| **minsearch** | In-memory hybrid search — BM25 + vector |
| **SQLiteSearch** | Persistent SQLite-backed vector index for local use |
| **pgvector** | PostgreSQL extension — `vector` column type, `<=>` cosine operator |
| **PostgreSQL 16** | Production vector store with ACID guarantees |
| **Docker** | Spin up pgvector with one command |

---

## Key concepts

**Embedding model choice** — smaller models (`MiniLM`) are fast and sufficient for most RAG use cases. Larger models (`mpnet`, `e5-large`) improve recall at the cost of speed and memory.

**HNSW index** — Hierarchical Navigable Small World. Approximate nearest-neighbor search. Fast queries (~ms) at the cost of slight recall loss. Best for production.

**IVFFlat index** — Inverted File Flat. Groups vectors into clusters, searches only nearby clusters. More memory-efficient than HNSW, slightly lower recall.

**Reciprocal Rank Fusion (RRF)** — combines ranked lists from multiple retrievers without normalising scores: `score = Σ 1/(k + rank_i)`. k=60 is the standard constant.

**Embedding drift** — if your documents or queries shift domain, re-embedding with a fine-tuned model can significantly improve recall.

---

## Running

```bash
docker compose up postgres -d   # starts pgvector
uv sync
uv run jupyter notebook
```

---

## Applied in capstone

pgvector and hybrid RRF are the retrieval backbone of **[Sentinel AI](https://github.com/pebueno/sentinel-ai)**:

- `src/search/vector_search.py` — pgvector queries with cosine distance (`<=>` operator)
- `src/search/keyword_search.py` — minsearch BM25-style over knowledge base
- `src/search/hybrid_search.py` — RRF fusion (K=60, tunable weights per retriever)

Evaluation results on the Sentinel AI dataset:

| Method | Hit Rate @5 | MRR @5 |
|--------|------------|--------|
| Keyword (minsearch) | 1.000 | 0.955 |
| Hybrid (RRF) | 0.932 | 0.554 |
| Vector (pgvector) | 0.068 | 0.037 |

Keyword dominates because synthetic security documents use precise terminology — a known characteristic of domain-specific corpora at small scale.
