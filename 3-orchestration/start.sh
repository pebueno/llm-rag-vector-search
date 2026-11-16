#!/usr/bin/env bash
# Start Kestra with keys from .env.
# Kestra reads secrets from SECRET_<NAME> env vars holding base64-encoded values;
# this script does the encoding so raw keys only live in .env (gitignored).
set -euo pipefail
cd "$(dirname "$0")"
set -a; source .env; set +a

b64() { printf '%s' "${1:-}" | base64 | tr -d '\n'; }
export SECRET_GEMINI_API_KEY="$(b64 "${GEMINI_API_KEY:-}")"
export SECRET_OPENAI_API_KEY="$(b64 "${OPENAI_API_KEY:-}")"
export SECRET_TAVILY_API_KEY="$(b64 "${TAVILY_API_KEY:-}")"
export SECRET_GROQ_API_KEY="$(b64 "${GROQ_API_KEY:-}")"

docker compose up -d
echo "Kestra UI: http://localhost:${KESTRA_PORT:-8080}  (admin@kestra.io / Admin1234!)"
