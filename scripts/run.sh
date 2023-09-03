#!/usr/bin/env bash

run_from_same_dir() {
  local script_name=$1
  # Get the absolute path of the currently executing script
  DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

  source "$DIR/$script_name"
}

run_from_same_dir common.sh

initialize

# Start PostgreSQL
docker-compose -f docker-compose-psql.yml up -d

case "$1" in
    stack)
        # Start RabbitMQ and Celery for 'stack'
        docker-compose -f docker-compose.rabbitmq-redis.yml up -d
        docker-compose -f docker-compose.celery.yml up -d

        if [[ "${ENVIRONMENT}" == "production" ]]; then
          docker-compose -f docker-compose-prod.yml up --build
        else
          docker-compose -f docker-compose-dev.yml up --build
        fi
        ;;
    test)
        # Start RabbitMQ and Celery for 'test'
        docker-compose -f docker-compose.rabbitmq-redis.yml up -d
        docker-compose -f docker-compose.celery.yml up -d

        if [[ "${ENVIRONMENT}" == "production" ]]; then
          docker-compose -f docker-compose-prod.yml run web pytest -vs ../tests
        else
          docker-compose -f docker-compose-dev.yml run web pytest -vs ../tests
        fi
        ;;
    alembic)
        if [[ "${ENVIRONMENT}" == "production" ]]; then
            BASE_CMD="docker-compose -f docker-compose-prod.yml exec web alembic -c /ex_back/src/ex_back/alembic.ini"
        else
            BASE_CMD="docker-compose -f docker-compose-dev.yml exec web alembic -c /ex_back/src/ex_back/alembic.ini"
        fi
        # Shift to discard the first argument (alembic)
        shift
        $BASE_CMD "$@"
        ;;
    *)
        echo "Invalid option. Use 'stack' to launch the stack, 'test' to run the application tests, or 'alembic' to execute Alembic commands."
        exit 1
        ;;
esac

cleanup
