#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTEBOOK_DIR="${SCRIPT_DIR}/../notebooks"
PORT=9001

jupyter-notebook \
  --notebook-dir="${NOTEBOOK_DIR}" \
  --port=${PORT} \
  --no-browser
