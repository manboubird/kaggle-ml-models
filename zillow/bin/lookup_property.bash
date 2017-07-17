#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_DIR="${SCRIPT_DIR}/../input"
PROPERTY_CSV="properties_2016.csv"

head -n 100 "${INPUT_DIR}/${PROPERTY_CSV}" | csvlook | less -S

