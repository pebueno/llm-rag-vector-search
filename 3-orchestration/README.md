# Module 3 — AI Orchestration with Kestra

> LLM Zoomcamp 2026 · [course module](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/03-orchestration) · [homework spec](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/homework/03-orchestration/homework.md)

Modules 1–2 built RAG and agents in Python notebooks. This module moves the same ideas into an
**orchestrator**: [Kestra](https://kestra.io) flows are YAML files. Each task is an LLM call, a RAG step or an agent,
and every run is logged, scheduled and retryable, with token usage recorded per task.

---

## What's in this folder

| Path | What it is |
|------|------------|
| [`docker-compose.yml`](docker-compose.yml) | Kestra 1.3 + Postgres (course file; host ports and a Groq secret added) |
| [`start.sh`](start.sh) | Base64-encodes keys from `.env` into Kestra's `SECRET_*` variables and starts the stack |
| [`import_flows.sh`](import_flows.sh) | Imports every flow in `flows/` through the Kestra API |
| [`flows/`](flows/) | The six course flows, unchanged (Gemini; flows 3, 5 and 6 also need OpenAI or Tavily keys) |
| [`flows/groq/`](flows/groq/) | Homework flows with the provider swapped to Groq; prompts unchanged |
| [`homework/run_flows.py`](homework/run_flows.py) | Runs the homework flows 3× each through the API and saves token usage |
| [`homework/results.json`](homework/results.json) | Raw outputs and token counts from those runs |

## Lessons

| # | Lesson | Key idea |
|---|--------|----------|
| 01 | Intro | Orchestration adds scheduling, retries, logs and governance around AI tasks |
| 02 | Context engineering | Generic chatbots write outdated Kestra YAML because they lack current docs; the fix is context, not a bigger model |
| 03 | Setup | Docker Compose, secrets as base64 `SECRET_*` env vars, importing flows |
| 04 | AI Copilot | The Copilot generates flows using the current plugin schemas (the "5% rule": you fix the last details) |
| 05 | RAG | `IngestDocument` → embeddings in the KV store → `rag.ChatCompletion`; flows 1 vs 2 |
| 06 | Agents | `AIAgent` task: system message + prompt + tools; flows 4 and 5 |
| 07 | Multi-agent | One agent's output becomes another's input (flow 6) |
| 08 | Best practices | Pick deterministic tasks vs agents deliberately; cost, secrets, observability |

---

## Homework 3 results

| Q | Question | Measured | Answer |
|---|----------|----------|--------|
| 1 | Why Copilot beats ChatGPT at Kestra flows | *pending: ChatGPT comparison to be run by hand* | AI Copilot has access to current Kestra plugin documentation |
| 2 | Non-RAG answer about Kestra 1.1 | Confident table of 9 "1.1 features" such as namespaces and secrets integrations, which existed long before 1.1 or are invented | **Vague, generic, or fabricated** |
| 3 | `multilingual_agent` output tokens, short | median 95 (range 72–115, 6 runs) | **60–100 tokens** |
| 4 | Long vs short output tokens | median 144 vs 95 = **1.5×** | between "about the same" and "2–5×", see note |
| 5 | `english_brevity` 3 vs 1 sentence | median 144 vs 103 = **1.4×** | between "about the same" and "2–4×", see note |
| 6 | Deterministic, regulated workflows | — | **Traditional task-based workflows** (predictable, auditable) |

### Why Q3–Q5 aren't clean: the model matters more than the prompt

The course measures with `gemini-2.5-flash`. Without a Gemini key, the flows run on Groq through Kestra's OpenAI
provider (`baseUrl: https://api.groq.com/openai/v1`):

1. **`openai/gpt-oss-120b` (first attempt) is a reasoning model.** Its hidden reasoning tokens count as output: a 1–2 sentence
   "short" summary reported ~235 output tokens, and runs ranged from 95 to 438. The noise was larger than the short-vs-long difference.
   Reasoning tokens are billed even though the user never sees them, which matters for cost monitoring (module 5).
2. **`allam-2-7b` (used for the reported numbers) doesn't reason, but follows length instructions poorly.** "Short (1–2 sentences)" came back
   as ~4 sentences, and "exactly 3 sentences" as ~6. Token ratios therefore come out smaller than the
   prompts intend (1.4–1.5× instead of the 2×+ the instructions imply).

Lesson: token budgets and length controls are model-specific. If cost depends on output length, enforce it
(`max_tokens`, structured output) rather than asking in the prompt. Re-run `flows/` with a Gemini key to get the
reference answers for Q4–Q5.

---

## Decisions and deviations

| Decision | Why |
|----------|-----|
| Groq copies in `flows/groq/` instead of editing course flows | Course flows stay runnable as-is with a Gemini key; the diff is one provider block. |
| `4_simple_agent_3_sentences.yaml` as a separate flow | Q5 edits a flow in the UI; a separate file keeps both versions versioned and re-runnable. |
| Runs via API, 3× per config, median reported | LLM output varies run to run; a single execution isn't a measurement. |
| Configurable host ports (`KESTRA_PORT`, `KESTRA_MGMT_PORT`) | 8081 was taken by another local service. |
| `start.sh` handles base64 encoding | Kestra requires base64-encoded secrets; scripting it keeps raw keys only in the gitignored `.env`. |
| Flow 2 (RAG) not run | Needs an embedding model; Groq has none. Q2 is answered from flow 1's output. |

---

## Running

```bash
cd 3-orchestration
cp .env.example .env          # GEMINI_API_KEY for course flows, GROQ_API_KEY for flows/groq
./start.sh                    # Kestra UI at http://localhost:8080 (admin@kestra.io / Admin1234!)
./import_flows.sh
python homework/run_flows.py  # re-run homework measurements
docker compose down
```

---

## Where this shows up in Sentinel AI

[Sentinel AI](https://github.com/pebueno/sentinel-ai) doesn't use Kestra. Its pipeline is a `Makefile` target (`make ingest`)
that runs three Python scripts in order: generate knowledge base → generate events → embed and load into Postgres.
That works for a one-off demo, but there's no retry, schedule or run history. Those are exactly what this module adds.
A natural next step for Sentinel is a Kestra flow wrapping those three scripts on a schedule.

---

## References

- Course module: [03-orchestration](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/03-orchestration)
- [Kestra AI plugins](https://kestra.io/plugins/plugin-ai) · [Kestra secrets in open source](https://kestra.io/docs/how-to-guides/secrets)
- [Groq OpenAI compatibility](https://console.groq.com/docs/openai) · [Groq reasoning models](https://console.groq.com/docs/reasoning)
