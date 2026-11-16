"""Run the homework flows in Kestra 3 times each and record token usage.

Requires Kestra running (../start.sh) with flows/groq/ imported (../import_flows.sh).
Usage: python homework/run_flows.py   -> writes homework/results.json
"""
import json
import statistics
import subprocess
import time
from pathlib import Path

BASE = "http://localhost:8080/api/v1"
AUTH = "admin@kestra.io:Admin1234!"
NAMESPACE = "zoomcamp.groq"
RUNS = 3  # LLM output varies between runs; report the median


def api(*args):
    out = subprocess.run(["curl", "-s", "-u", AUTH, *args], capture_output=True, text=True, encoding="utf-8").stdout
    return json.loads(out)


def execute(flow, inputs):
    form = [arg for k, v in inputs.items() for arg in ("-F", f"{k}={v}")]
    execution = api("-X", "POST", f"{BASE}/executions/{NAMESPACE}/{flow}?wait=true", *form)
    while execution["state"]["current"] not in ("SUCCESS", "FAILED", "KILLED", "WARNING"):
        time.sleep(3)
        execution = api(f"{BASE}/executions/{execution['id']}")
    return {t["taskId"]: t.get("outputs", {}) for t in execution["taskRunList"]}


def main():
    results = {}

    outputs = execute("1_chat_without_rag", {})
    results["1_chat_without_rag"] = {"text": outputs["chat_without_rag"]["textOutput"]}

    configs = [
        ("4_simple_agent", "short"),
        ("4_simple_agent", "long"),
        ("4_simple_agent_3_sentences", "long"),
    ]
    for flow, length in configs:
        runs = []
        for _ in range(RUNS):
            outputs = execute(flow, {"summary_length": length})
            runs.append({
                task: {
                    "output_tokens": outputs[task]["tokenUsage"]["outputTokenCount"],
                    "text": outputs[task]["textOutput"],
                }
                for task in ("multilingual_agent", "english_brevity")
            })
        results[f"{flow}:{length}"] = {
            "runs": runs,
            "median_output_tokens": {
                task: statistics.median(r[task]["output_tokens"] for r in runs)
                for task in ("multilingual_agent", "english_brevity")
            },
        }

    path = Path(__file__).parent / "results.json"
    path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    for key, value in results.items():
        print(key, value.get("median_output_tokens", ""))


if __name__ == "__main__":
    main()
