ARG POPSTGRES_VERSION=10.4-alpine
FROM postgres:${POPSTGRES_VERSION}

ENV POSTGRES_USER raven_adm
ENV POSTGRES_PASSWORD raven_adm
ENV POSTGRES_DB db_raven

RUN mkdir -p /tablespace/data \
    && mkdir -p /tablespace/index \
    && chown -R postgres:postgres /tablespace \
    && chmod 777 /tablespace/data \
    && chmod 777 /tablespace/index 

COPY initial.sql /docker-entrypoint-initdb.d/
