#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<-EOSQL
    CREATE DATABASE $PG_DB;
    GRANT ALL PRIVILEGES ON DATABASE $PG_DB TO $POSTGRES_USER;
EOSQL
