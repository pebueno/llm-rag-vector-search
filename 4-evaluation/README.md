# Module 4 — Evaluation

> LLM Zoomcamp 2026 · Week 5

Systematic evaluation of RAG systems: measuring whether the right documents are being retrieved (retrieval evaluation) and whether the generated answers are actually correct and useful (answer quality evaluation). Both offline (pre-deployment) and online (post-deployment) strategies.

---

## Why evaluation matters

Without evaluation you're guessing. With evaluation you can:
- Quantify whether retrieval improvements actually help end users
- Compare prompt variants objectively instead of eyeballing examples
- Catch regressions when you change your embedding model or chunking strategy
- Build a feedback loop between production signals and development

---

## Two evaluation layers

### Layer 1: Retrieval evaluation

Measures whether the search pipeline returns the right documents.

**Ground truth generation**: use an LLM to generate `(question → document_id)` pairs — for each document, ask the LLM *"what question does this document answer?"*. This creates a test set without human annotation.

**Metrics:**

| Metric | Formula | Interpretation |
|--------|---------|---------------|
| **Hit Rate @k** | `hits / total` | Fraction of questions where correct doc appears in top-k |
| **MRR @k** | `mean(1/rank)` | Rewards finding the right doc at rank 1 more than rank 5 |

Higher is better for both. MRR is stricter — a hit at rank 5 scores 0.2 vs 1.0 for rank 1.

### Layer 2: Answer quality evaluation (LLM-as-a-judge)

Measures whether the generated answer is actually relevant and correct.

An LLM judge receives `(question, retrieved context, generated answer)` and classifies:
- `RELEVANT` — fully answers the question using context
- `PARTLY_RELEVANT` — partial answer or notable gaps
- `NOT_RELEVANT` — off-topic, wrong, or ignores context

Scales to thousands of examples. No human annotation needed. Works best when the judge model is different from (or larger than) the generation model.

---

## Lessons

| Lesson | Topic |
|--------|-------|
| 4.1 | Offline vs online evaluation — pre-deployment testing vs production monitoring |
| 4.2 | Ground truth generation — LLM-generated (question → document) pairs |
| 4.3 | Hit Rate and MRR — implementation from scratch |
| 4.4 | Comparing retrieval methods — keyword vs vector vs hybrid |
| 4.5 | LLM-as-a-judge — prompt design, classification schema, agreement analysis |
| 4.6 | Cosine similarity scoring — embedding-based answer quality |
| 4.7 | Prompt variant comparison — does a better system prompt produce better answers? |
| 4.8 | Batch evaluation — ThreadPoolExecutor for parallel scoring |
| 4.9 | Online evaluation — integrating real user feedback as a quality signal |

---

## Technologies

| Tool | Role |
|------|------|
| **Groq** | Generation model + judge model (free tier) |
| **sentence-transformers** | Embedding-based cosine similarity scoring |
| **pandas** | Results aggregation and summary statistics |
| **tqdm** | Progress tracking over large evaluation sets |
| **ThreadPoolExecutor** | Parallel evaluation across question sets |
| **matplotlib** | Visualising results — bar charts, distributions |
| **PostgreSQL** | Storing ground truth and results for offline analysis |

---

## Key concepts

**Offline evaluation** — run against a fixed test set before deploying. Catches obvious regressions. Doesn't reflect real user behaviour.

**Online evaluation** — measure quality in production via user feedback (thumbs up/down), implicit signals (session length, follow-up questions), or LLM judge scoring every live response.

**Embedding-based scoring** — compare the embedding of the generated answer to the embedding of a reference answer using cosine similarity. Faster than LLM judge but misses reasoning errors.

**Toxicity assessment** — use a pre-trained classifier to flag harmful or biased outputs. Important for public-facing systems.

**Judge calibration** — the LLM judge's ratings only mean something if it's consistent. Evaluate agreement between human raters and the judge on a sample before trusting it at scale.

---

## Running

```bash
uv sync
uv run jupyter notebook
```

Requires PostgreSQL running for some notebooks:
```bash
docker compose up postgres -d
```

---

## Applied in capstone

Full evaluation suite in **[Sentinel AI](https://github.com/pebueno/sentinel-ai)**:

- `notebooks/01-retrieval-eval.ipynb` — Hit Rate + MRR for keyword vs vector vs hybrid
- `notebooks/02-rag-eval.ipynb` — LLM-as-judge across 3 prompt variants
- `src/monitoring/judge.py` — production judge: scores every live conversation automatically
- `data/ground_truth/` — cached evaluation results (60 Q&A pairs, LLM judge results)

**Results:**

| Method | Hit Rate @5 | MRR @5 |
|--------|------------|--------|
| Keyword | 1.000 | 0.955 |
| Hybrid RRF | 0.932 | 0.554 |
| Vector | 0.068 | 0.037 |

| Prompt variant | RELEVANT | PARTLY_RELEVANT | NOT_RELEVANT |
|---------------|---------|----------------|-------------|
| Baseline | 16% | 0% | 83% |
| With instructions | 0% | 0% | 100% |
| Instructions + rewriting | 0% | 0% | 100% |
