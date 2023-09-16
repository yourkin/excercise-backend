#!/bin/bash
set -e

# Check if role exists and create if not
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<-EOSQL
DO
\$do\$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_roles
      WHERE  rolname = 'postgres') THEN

      CREATE ROLE postgres WITH LOGIN PASSWORD '$POSTGRES_PASSWORD';
      ALTER ROLE postgres CREATEDB;
      ALTER ROLE postgres SUPERUSER;

   END IF;
END
\$do\$;
EOSQL
