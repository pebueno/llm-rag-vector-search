#!/usr/bin/env bash
# Import every flow in flows/ into the running Kestra instance.
set -euo pipefail
cd "$(dirname "$0")"
PORT="$(grep -E '^KESTRA_PORT=' .env 2>/dev/null | cut -d= -f2)"
for f in flows/*.yaml; do
  curl -sf -X POST -u 'admin@kestra.io:Admin1234!' \
    "http://localhost:${PORT:-8080}/api/v1/flows/import" -F "fileUpload=@$f" >/dev/null
  echo "imported $f"
done
