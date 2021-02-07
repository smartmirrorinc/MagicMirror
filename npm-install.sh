#!/usr/bin/env bash
set -euo pipefail

npm install &&
cd modules &&
for f in $(ls | grep MMM-); do
    npm install
done
