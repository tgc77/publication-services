#!/bin/bash
set -x

echo "Running services tests..."
pytest -v -p no:warnings services/tests/
