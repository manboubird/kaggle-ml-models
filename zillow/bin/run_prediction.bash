#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_SCRIPT="${SCRIPT_DIR}/../src/run_xgb.py"

echo "Executing ${MAIN_SCRIPT} ..."
python "${MAIN_SCRIPT}"
echo "Complete executing ${MAIN_SCRIPT} ..."

exit 0
