#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$PG_USER" --dbname postgres <<-EOSQL
    CREATE DATABASE $PG_DB;
    GRANT ALL PRIVILEGES ON DATABASE $PG_DB TO $PG_USER;
EOSQL
