FROM postgres:latest

ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=0000
ENV POSTGRES_DB=magic-store

COPY create.sql /docker-entrypoint-initdb.d/
EXPOSE 5432