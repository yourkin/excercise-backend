FROM postgres:14.8

# Copy initialization scripts
# For example, you can add a *.sql or *.sh script to the /docker-entrypoint-initdb.d directory
# that you want to be executed when the container starts up
COPY ./scripts/ /docker-entrypoint-initdb.d/

# When a container is started for the first time, a new database
# with the specified name will be created and initialized
# with the provided configuration variables.
# Furthermore, it will execute files with extensions .sh, .sql and .sql.gz
# that are found in /docker-entrypoint-initdb.d.
