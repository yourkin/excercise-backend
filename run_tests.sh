#!/usr/bin/env bash

# Read the environment variables
source .env

if [[ "${ENVIRONMENT}" == "production" ]]; then
  docker-compose run web pytest -vs
else
  docker-compose run web pytest -vs ../tests
fi