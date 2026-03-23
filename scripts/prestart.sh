#! /usr/bin/env bash

# Set PYTHONPATH to include the /app directory
export PYTHONPATH="/app:${PYTHONPATH}"

set -e
set -x

echo "Initialising database session..."

python app/initial_data.py
