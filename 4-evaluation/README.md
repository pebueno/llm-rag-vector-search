# Module 4 — Evaluation

Systematic evaluation of RAG systems: measuring retrieval quality with ground truth datasets and assessing answer quality using an LLM as an automated judge.

## What's covered

- **Retrieval evaluation**: Hit Rate @k, MRR @k
- **Ground truth generation**: using an LLM to generate (question → document) pairs
- **LLM-as-a-judge**: automated answer quality scoring (RELEVANT / PARTLY_RELEVANT / NOT_RELEVANT)
- Comparing retrieval methods: keyword vs vector vs hybrid
- Prompt variant comparison: does a better system prompt produce better answers?

## Notebooks

| File | Description |
|------|-------------|
| `01-retrieval-eval.ipynb` | Hit Rate + MRR evaluation across keyword, vector, and hybrid search |
| `02-rag-eval.ipynb` | LLM-as-judge scoring across 3 prompt variants |

## Key concepts

**Hit Rate @k**: fraction of questions where the correct document appears in the top-k results.

**MRR @k** (Mean Reciprocal Rank): average of 1/rank of the correct document — rewards finding the right doc at rank 1 more than rank 5.

**LLM-as-a-judge**: feed the question + retrieved context + generated answer to a second LLM call and ask it to classify relevance. Scales to thousands of examples without human annotation.

## Results (Sentinel AI dataset)

| Method | Hit Rate @5 | MRR @5 |
|--------|------------|--------|
| **Keyword (minsearch)** | **1.000** | **0.955** |
| Hybrid (RRF) | 0.932 | 0.554 |
| Vector (pgvector) | 0.068 | 0.037 |

Keyword dominates on synthetic data with precise domain terminology. Vector search underperforms at small scale with specialised vocabulary.

## Applied in capstone

Full evaluation notebooks with charts and results are in **[Sentinel AI](https://github.com/pebueno/sentinel-ai)** — see `notebooks/01-retrieval-eval.ipynb` and `notebooks/02-rag-eval.ipynb`.

## Running

```bash
cd 4-evaluation
uv sync
uv run jupyter notebook
```
