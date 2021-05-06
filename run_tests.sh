#!/bin/bash
set -x

docker compose -f tests/docker-compose.yml build
docker compose -f tests/docker-compose.yml up -d

echo "Running services tests..."
pytest -v -p no:warnings services/tests/

echo "Running client tests..."
python -m unittest2 discover -s client/tests/ -v

docker compose -f tests/docker-compose.yml down