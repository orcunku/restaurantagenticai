#!/usr/bin/env bash
set -euo pipefail
cd /workspaces/restaurantagenticai

if [ ! -f .env ]; then
  cp .env.example .env
fi

python -m pip install --upgrade pip
python -m pip install -e '.[dev]'

echo
echo "Codespace setup complete."
echo "Run: ./scripts/start-demo.sh"
echo "Then open the forwarded port 8000 (Restaurant AI Demo)."
