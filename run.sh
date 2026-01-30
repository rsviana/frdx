#!/usr/bin/env bash

## Criado para rodar com mais facilidade no MacOS - o mesmo vem apresentando problemas no empacotamento.

set -euo pipefail
cd "$(dirname "$0")"

source .venv/bin/activate

export PYTHONPATH="$(pwd)/src"
python -m frd.cli "$@"
