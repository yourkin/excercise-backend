FROM postgres:13

ENV POSTGRES_DB=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

ADD init.sql /docker-entrypoint-initdb.d/
