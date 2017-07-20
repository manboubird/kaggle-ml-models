#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_DIR="${SCRIPT_DIR}/../input"

PROPERTY_CSV="properties_2016.csv"
TRAIN_CSV="train_2016_v2.csv"

LINE_NUM=100

output=""

for f in "${PROPERTY_CSV}" "${TRAIN_CSV}";do
  output="$(printf "${output}\n\n ${f}\n")"
  output="$(printf "${output}\n $(head -n "${LINE_NUM}" "${INPUT_DIR}/${f}" | csvlook -z 100)")"
done
echo "${output}" # | less -S
