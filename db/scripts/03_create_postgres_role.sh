#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE ROLE postgres WITH LOGIN PASSWORD 'your_password';
    ALTER ROLE postgres CREATEDB;
    ALTER ROLE postgres SUPERUSER;
EOSQL
