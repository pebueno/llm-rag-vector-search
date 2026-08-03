# Module 2 — Vector Search

Deep dive into embedding-based retrieval: how vectors represent meaning, how similarity search works at scale, and how to choose between indexing strategies.

## What's covered

- Dense embeddings with `sentence-transformers`
- Cosine similarity vs dot product vs L2 distance
- pgvector — PostgreSQL extension for vector similarity search
- HNSW vs IVFFlat indexes: speed vs recall tradeoffs
- Hybrid search: combining keyword (BM25) + vector scores

## Notebooks

| File | Description |
|------|-------------|
| `01-embeddings.ipynb` | Generating embeddings, visualising vector space |
| `02-pgvector.ipynb` | Setting up pgvector, inserting vectors, querying by similarity |
| `03-hybrid.ipynb` | Reciprocal Rank Fusion (RRF) — combining keyword and vector results |

## Stack

- **Embeddings**: `sentence-transformers` (`all-MiniLM-L6-v2`, 384-dim)
- **Vector DB**: pgvector (PostgreSQL 16 extension)
- **Keyword search**: minsearch / BM25
- **Fusion**: Reciprocal Rank Fusion (K=60)

## Applied in capstone

pgvector and hybrid RRF search power the knowledge base in **[Sentinel AI](https://github.com/pebueno/sentinel-ai)** — see `src/search/vector_search.py` and `src/search/hybrid_search.py`.

## Running

```bash
cd 2-vector-search
docker compose up postgres -d   # starts pgvector
uv sync
uv run jupyter notebook
```
