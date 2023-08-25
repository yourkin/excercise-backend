#!/usr/bin/env bash

# Read the environment variables
source .env

# Start PostgreSQL
docker-compose -f docker-compose-psql.yml up -d

# Start RabbitMQ
docker-compose -f docker-compose.rabbitmq-redis.yml up -d

# Wait for PostgreSQL to start
./wait-for-it.sh db:5432 --timeout=30

if [[ "${ENVIRONMENT}" == "production" ]]; then
  docker-compose -f docker-compose-prod.yml up --build
else
  docker-compose -f docker-compose-dev.yml up --build
fi
