#!/bin/bash

# The base command for running Alembic inside the docker container
BASE_CMD="docker-compose -f docker-compose-dev.yml exec web alembic -c /ex_back/src/ex_back/alembic.ini"

# Execute the command with all arguments passed to the script
$BASE_CMD "$@"
