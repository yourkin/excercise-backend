#!/usr/bin/env bash

# Read the environment variables
source .env

# Start PostgreSQL
docker-compose -f docker-compose-psql.yml up -d

# Wait for PostgreSQL to start
./wait-for-it.sh db:5432 --timeout=30

if [[ "${ENVIRONMENT}" == "production" ]]; then
  docker-compose -f docker-compose-prod.yml run web pytest -vs
else
  docker-compose -f docker-compose-dev.yml run web pytest -vs ../tests
fi
