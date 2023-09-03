function initialize() {
    # Store the current working directory
    ORIGINAL_DIR=$(pwd)

    # Navigate to the parent directory of the script
    cd "$(dirname "$0")/.." || exit

    # Read the environment variables
    source .env

}

function cleanup() {
    # Depending on the environment, use 'down' for dev or 'stop' for prod
    if [[ "${ENVIRONMENT}" == "production" ]]; then
      docker-compose -f docker-compose-prod.yml stop
      docker-compose -f docker-compose-psql.yml stop
      docker-compose -f docker-compose.rabbitmq-redis.yml stop
      docker-compose -f docker-compose.celery.yml stop
    else
      docker-compose -f docker-compose-dev.yml down
      docker-compose -f docker-compose-psql.yml down
      docker-compose -f docker-compose.rabbitmq-redis.yml down
      docker-compose -f docker-compose.celery.yml down
    fi

    # Return to the original directory
    cd "$ORIGINAL_DIR" || exit
}
