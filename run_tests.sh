#!/usr/bin/env bash

# Read the environment variables
source .env

if [[ "${ENVIRONMENT}" == "production" ]]; then
  docker-compose -f -f docker-compose-prod.yml run web pytest -vs
else
  docker-compose -f docker-compose-dev.yml run web pytest -vs ../tests
fi