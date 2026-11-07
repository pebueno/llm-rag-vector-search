# Module 1 — Agentic RAG

> LLM Zoomcamp 2026 · [course module](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/01-agentic-rag) · [homework spec](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/homework/01-agentic-rag/homework.md)

Build a RAG pipeline from plain Python (keyword search + prompt + LLM), then turn it into an
**agent**: the LLM gets a `search` tool and decides itself when to search, what to search for,
and when to stop.

---

## What's in this folder

| File | What it does | Course lessons |
|------|--------------|----------------|
| [`notebook.ipynb`](notebook.ipynb) | RAG from scratch: LLM without context, manual context, FAQ dataset, minsearch index, prompt building | 03–07 |
| [`rag_helper.py`](rag_helper.py) | `RAGBase`: the same pipeline as a class with swappable `index` and `llm_client` | 08 |
| [`ingest.py`](ingest.py) | Downloads the DataTalks.Club FAQ and builds a minsearch index | 04–05, 09 |
| [`sqlite-ingest.ipynb`](sqlite-ingest.ipynb) | Ingestion as a separate process: writes the FAQ into a persistent `faq.db` | 09 |
| [`persistent-rag.ipynb`](persistent-rag.ipynb) | Query side: opens `faq.db` and plugs it into `RAGBase` without re-indexing | 09 |
| [`agents.ipynb`](agents.ipynb) | Function calling, then the agentic loop, plus typo and off-topic tests | 11–14 |
| [`homework.ipynb`](homework.ipynb) | Homework 1: RAG and an agent over the course's own lesson pages | — |

Lessons 01–02 (intro, environment), 10 and 12 (recaps) and 15–16 (agent frameworks: toyaikit,
PydanticAI, OpenAI Agents SDK) were read but have no code here.

> **Search here is keyword search only.** `minsearch.Index` and `sqlitesearch.TextSearchIndex`
> rank by TF-IDF over tokens. No embeddings are involved; those start in [module 2](../2-vector-search/).

---

## RAG in one picture

```
question ──► search(index) ──► top-5 docs ──► prompt = instructions + question + docs ──► LLM ──► answer
```

Without the search step the model answers from training data. For "Can I still join the course?"
it invents generic advice about enrollment windows and waiting lists. With the FAQ entries in the prompt it gives the course's
actual policy. Compare the first and second LLM calls in `notebook.ipynb`.

## Agent in one picture

```
messages = [system, user]
loop (max N iterations):
    response = LLM(messages, tools=[search])
    if response has tool_calls:
        run each tool, append results as role="tool" messages
    else:
        return response.content        # model decided it has enough
```

Plain RAG always does exactly one search with the user's exact words. The agent can rewrite the
query, search several times, or not search at all (off-topic questions).

---

## Homework 1 results

Knowledge base: the 72 lesson pages of the course at commit `8c1834d`.
Model: `openai/gpt-oss-120b` on Groq (course reference: `gpt-5.4-mini` on OpenAI).

| Q | Question | Measured | Answer |
|---|----------|----------|--------|
| 1 | Number of lesson pages | 72 | **72** |
| 2 | Top result for "How does the agentic loop keep calling the model…" | `01-agentic-rag/lessons/14-agentic-loop.md` | **14-agentic-loop.md** |
| 3 | Prompt tokens, RAG over full pages | 7,176 | **7000** |
| 4 | Chunks with size=2000, step=1000 | 295 | **295** |
| 5 | Token reduction with chunking | 7,176 → 2,359 (3.0×) | **3× fewer** |
| 6 | Agent `search` calls | 3 | **4** (closest) |

**Takeaways**

- **Chunking cuts cost 3× here and also improves precision.** A match deep inside a long page no
  longer drags the whole page into the prompt.
- **Context grows with every tool call.** The agent keeps every search result in `messages`. With
  5 chunks per search, the 4th call exceeded Groq's free-tier 8k tokens/minute. Trimming tool output
  (3 chunks, only `filename` + `content`) fixed it. Production agents need the same budgeting.

---

## Decisions and deviations from the course

| Decision | Why |
|----------|-----|
| **Groq instead of OpenAI** | Free tier. Groq is OpenAI-compatible, so it's the same `openai` SDK with a different `base_url`. |
| **`chat.completions` instead of the Responses API** | The course uses `client.responses.create`. Groq only implements `chat.completions`. Differences: tool calls arrive in `message.tool_calls` instead of `response.output`, and tool results are sent as `role: "tool"` messages instead of `function_call_output` items. |
| **`openai/gpt-oss-120b` instead of `llama-3.3-70b-versatile`** | Groq retired the Llama model (it returns 404). gpt-oss-120b is the strongest free model on Groq and the closest to the course's OpenAI models. |
| **Homework: subclass `RAGBase`** | Keeps the lesson helper intact and shows which methods are schema-specific (`search`, `build_context`) versus what changed to report token usage (`llm`, `rag`). |
| **Homework: hand-written agent loop instead of toyaikit** | No extra dependency, and every step of the loop is visible. Frameworks generate the same tool JSON from type hints and docstrings. |
| **`chat()` helper that waits 61s on 413/429 "tokens per minute"** | Free tier counts 8k tokens/minute across calls. A full-page RAG prompt is ~7k, so two calls in a row trip the limit. |

### Observed model behaviour

The lesson shows the agent fixing the typo "Olama" to "Ollama" by itself. gpt-oss-120b retried
three "Olama" variants and then said the FAQ had no answer. It stayed grounded and didn't
hallucinate, but it was less resourceful. Self-correction depends on the model, not on the loop.

---

## Key concepts

- **Text vs keyword fields (minsearch).** Text fields are tokenised and ranked; keyword fields are
  exact-match filters (like SQL `WHERE`).
- **Boosting.** `boost_dict={"question": 3.0}` makes a match in the FAQ question count 3× a match
  in the answer.
- **Tool schema.** A JSON Schema the model reads to decide when to call a function and with what
  arguments. The `description` fields are prompt engineering.
- **Iteration cap.** The loop must have a hard stop. A confused model can otherwise call tools forever.
- **Ingestion vs query separation.** Indexing runs once (`sqlite-ingest`). The query side only opens
  the DB (`persistent-rag`), so restarting the app doesn't re-download or re-index.

---

## Running

```bash
cd 1-rag
cp .env.example .env        # add GROQ_API_KEY from console.groq.com
uv sync
uv run jupyter notebook
```

Run `sqlite-ingest.ipynb` before `persistent-rag.ipynb`, because the latter reads `faq.db`.

---

## Where this shows up in Sentinel AI

[Sentinel AI](https://github.com/pebueno/sentinel-ai) is my home-security assistant project.
Its agent ([`src/agent/loop.py`](https://github.com/pebueno/sentinel-ai/blob/master/src/agent/loop.py))
uses the same `chat.completions` loop as `agents.ipynb`, with three production additions:

- a hard cap of 5 iterations;
- tool results truncated to 8,000 characters before they go back into the context;
- a follow-up prompt when the model returns empty content after tool calls.

It has two tools instead of one: `search_knowledge_base` (documents) and `query_events` (SQL over
an event log). See [`src/agent/tools.py`](https://github.com/pebueno/sentinel-ai/blob/master/src/agent/tools.py).

---

## References

- Course module: [01-agentic-rag](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/01-agentic-rag)
- [minsearch](https://github.com/alexeygrigorev/minsearch) · [sqlitesearch](https://github.com/alexeygrigorev/sqlitesearch) · [gitsource](https://github.com/alexeygrigorev/gitsource)
- [Groq OpenAI compatibility](https://console.groq.com/docs/openai) · [Groq tool use](https://console.groq.com/docs/tool-use)
- [Groq rate limits](https://console.groq.com/docs/rate-limits)
