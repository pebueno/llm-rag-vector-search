# Module 4 — Evaluation

> LLM Zoomcamp 2026 · [course module](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/04-evaluation) · [homework spec](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/homework/04-evaluation/homework.md)

Modules 1–3 built search, RAG and agents, and judged them by eyeballing a few queries. This module replaces
that with numbers. A **ground truth** of questions with known answers lets every change to search or prompts be
scored, compared and either kept or reverted.

---

## What's in this folder

| File | What it does | Course lessons |
|------|--------------|----------------|
| [`search_eval.ipynb`](search_eval.ipynb) | Relevance lists, Hit Rate, MRR on the FAQ; boost tuning with a validation/test split | 01–06 |
| [`llm_judge.ipynb`](llm_judge.ipynb) | LLM-as-a-judge over RAG answers, with a calibration check on known-bad answers | 11–14 |
| [`homework.ipynb`](homework.ipynb) | Homework 4: question generation, text vs vector vs hybrid on the lesson pages, RRF `k` tuning, truncation experiment | — |
| [`eval_utils.py`](eval_utils.py) | `hit_rate`, `mrr`, `evaluate(ground_truth, search_fn, is_relevant)`, Groq structured output with rate-limit handling | — |
| `embedder.py`, `download.py` | Course's ONNX embedder (homework 2), `all-MiniLM-L6-v2` without PyTorch | 02-vector-search/09 |
| `data/` | Course-prepared ground truth (FAQ and lesson pages) and RAG answers | — |

Lesson 14 (agent evaluation: saving tool-call trajectories) was read but has no code here.

---

## The two layers

| Layer | Question it answers | How |
|-------|---------------------|-----|
| **Retrieval** | Did search return the right document? | Ground truth `(question → document)`, then **Hit Rate@5** (right doc anywhere in top 5) and **MRR@5** (mean of 1/rank) |
| **Answer** | Is the generated answer correct? | **LLM-as-a-judge**: a second model compares the answer to a reference and returns a structured verdict |

The ground truth itself is LLM-generated: for each document, an LLM writes questions it answers, worded differently
from the source so the test isn't trivially easy.

---

## Homework 4 results

| Q | Measured | Answer |
|---|----------|--------|
| 1 | Avg input tokens generating questions for 3 pages: 1,483 | **1400** |
| 2 | Text search top-1 for the first question: `03-rag.md` | **03-rag.md** |
| 3 | Vector search top-1: `01-intro.md` | **01-intro.md** |
| 4 | Text search Hit Rate: 0.758 | **0.76** |
| 5 | Vector search MRR: 0.549 | **0.55** |
| 6 | Hybrid MRR by k: 1 → 0.648, 50/100/200 → 0.638 | **1** |

Homework 2 Q1 (ONNX `v[0]` for "How does approximate nearest neighbor search work?"): **−0.02**.

---

## Findings

Measured in the notebooks, beyond what the lessons state.

### 1. The intuitive boost was the worst one
Module 1 used `question: 3.0` because matching the FAQ question "felt" most important. In the grid search it's the
**worst** question boost. Answer-weighted boosts win (MRR 0.54 → 0.63), and the gain holds on held-out documents
(test MRR 0.520 → 0.612). Generated and real questions share vocabulary with *answers*, not with short question titles.

### 2. "Keyword beats vector" was partly a truncation artifact

| Vector setup (lesson pages, 360 questions) | Hit Rate | MRR |
|---------------------------------------------|----------|-----|
| 2000-char chunks, tokenizer truncates at 128 tokens (homework) | 0.725 | 0.549 |
| 2000-char chunks, 256 tokens | 0.808 | 0.636 |
| 500-char chunks, 128 tokens | 0.828 | 0.665 |
| *Text search, for reference* | *0.758* | *0.594* |

The shipped ONNX tokenizer silently truncates at 128 tokens, while a 2000-char chunk is ~530 tokens, so vector search
embedded about a quarter of each chunk. Fixing that puts vector **above** text. Before comparing retrievers, check that
each one actually sees the whole document. The embedding model's max sequence length is a chunking constraint.

### 3. Hybrid search wins, and its `k` hardly matters
Hybrid (RRF) reaches Hit Rate 0.84 against 0.76 for text and 0.73 for vector: the two retrievers miss different questions.
Changing `k` from 1 to 200 moves MRR by only 0.01.

### 4. A judge has to be tested before it is trusted
On 40 course RAG answers the judge said "good" for 95%, and both "bad" verdicts were justified on reading. The key check
is calibration: 10 answers deliberately paired with the wrong question were **all** rejected. That test only covers easy
negatives (wrong topic). Subtle errors need a small human-labelled set.

---

## Decisions and deviations

| Decision | Why |
|----------|-----|
| Groq `openai/gpt-oss-120b` with `chat.completions.parse` | Course uses OpenAI `responses.parse`; Groq supports structured output through chat completions. A different model family from the course's answer generator, so the judge isn't grading itself. |
| Course-prepared ground truth instead of regenerating | Regenerating ~80 FAQ records + 72 pages would use a large share of the free-tier budget. Homework Q1 still generates a sample to show the method. |
| Judge 40 sampled answers, sequentially | Free tier: 1,000 requests/day, 8k tokens/minute. Parallel calls only hit the per-minute limit sooner. |
| `evaluate()` takes an `is_relevant` function | The lessons hard-code FAQ `id` matching; the homework needs `filename` matching. One function serves both. |
| Validation/test split for boost tuning | Tuning and reporting on the same questions overstates the gain. |
| Data URLs from `04-evaluation/` and `02-vector-search/embed/` | The homework's `cohorts/2026/...` URLs return 404 after a repo restructure. |

---

## Running

```bash
cd 4-evaluation
cp .env.example .env            # GROQ_API_KEY
uv sync
uv run python download.py       # ONNX model into models/ (homework only)
uv run jupyter notebook
```

---

## Where this shows up in Sentinel AI

[Sentinel AI](https://github.com/pebueno/sentinel-ai) has the same two layers:
[`notebooks/01-retrieval-eval.ipynb`](https://github.com/pebueno/sentinel-ai/blob/master/notebooks/01-retrieval-eval.ipynb)
(Hit Rate / MRR for keyword, vector and hybrid) and
[`notebooks/02-rag-eval.ipynb`](https://github.com/pebueno/sentinel-ai/blob/master/notebooks/02-rag-eval.ipynb) plus
[`src/monitoring/judge.py`](https://github.com/pebueno/sentinel-ai/blob/master/src/monitoring/judge.py) (LLM judge).

This module explains two of its reported results:
- **Vector Hit Rate 0.068**: reproduced in [module 2](../2-vector-search/README.md#3-ivfflat-pitfalls-in-pgvector-and-the-bug-behind-sentinel-ais-vector-score)
  as an IVFFlat index built on an empty table. Sentinel also embeds title + summary + full content with a 256-token
  model limit, so finding 2 (truncation) likely applies as well.
- **Judge: 100% NOT_RELEVANT for two prompt variants.** A judge that rejects almost everything fails the same calibration
  test as one that accepts everything. Feeding it known-good and known-bad answers is the next step there.

Both are follow-ups in the Sentinel repo, not fixed here.

---

## References

- Course module: [04-evaluation](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/04-evaluation)
- Cormack, Clarke & Büttcher, [Reciprocal Rank Fusion](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) (SIGIR 2009)
- Zheng et al., [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) (2023)
- [Groq structured outputs](https://console.groq.com/docs/structured-outputs)
