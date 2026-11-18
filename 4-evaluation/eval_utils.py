"""Evaluation helpers shared by the module 4 notebooks and homework.

Adapted from the course's evaluation_utils.py for Groq: chat.completions.parse
instead of the Responses API, and a wait on Groq's free-tier per-minute limit.
"""
import os
import time

from dotenv import load_dotenv
from openai import APIStatusError, OpenAI
from tqdm.auto import tqdm

load_dotenv()

MODEL = "openai/gpt-oss-120b"

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def llm_structured(instructions, user_prompt, output_type, model=MODEL, attempts=4):
    """Return (parsed pydantic object, usage).

    Groq's free tier allows 8000 tokens/minute across calls; on a 413/429 for
    that limit, wait for the window to reset and retry.
    """
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": user_prompt},
    ]
    for attempt in range(attempts):
        try:
            response = client.chat.completions.parse(
                model=model, messages=messages, response_format=output_type
            )
            return response.choices[0].message.parsed, response.usage
        except APIStatusError as e:
            rate_limited = e.status_code in (413, 429) and "per minute" in str(e)
            if not rate_limited or attempt == attempts - 1:
                raise
            time.sleep(61)


def hit_rate(relevance):
    """Share of queries with at least one relevant result."""
    return sum(1 in line for line in relevance) / len(relevance)


def mrr(relevance):
    """Mean reciprocal rank of the first relevant result (0 when none)."""
    total = 0.0
    for line in relevance:
        for rank, rel in enumerate(line):
            if rel == 1:
                total += 1 / (rank + 1)
                break
    return total / len(relevance)


def evaluate(ground_truth, search_function, is_relevant, progress=True):
    """Run search for every question and compute Hit Rate and MRR.

    is_relevant(query_record, result) -> bool decides what counts as a hit,
    so the same function works for FAQ ids and for lesson filenames.
    """
    records = tqdm(ground_truth) if progress else ground_truth
    relevance = [
        [int(is_relevant(q, doc)) for doc in search_function(q["question"])]
        for q in records
    ]
    return {"hit_rate": hit_rate(relevance), "mrr": mrr(relevance)}
