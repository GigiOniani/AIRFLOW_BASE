FROM postgres:16-alpine

RUN apk add --no-cache postgresql postgresql-contrib &&\
    mkdir -p /var/run/postgresql &&\
    chown -R postgres:postgres /var/run/postgresql &&\
    chmod 2777 /var/run/postgresql &&\
    chown -R postgres:postgres /var/lib/postgresql

RUN apk add --no-cache bash su-exec

ENV PGDATA /var/lib/postgresql/data
RUN mkdir -p "$PGDATA" && chown -R postgres:postgres "$PGDATA" && chmod 700 "$PGDATA"

# Initialize PostgreSQL database
USER postgres
RUN initdb --username postgres -D "$PGDATA" &&\
    echo "host all all 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf" &&\
    echo "listen_addresses='*'" >> "$PGDATA/postgresql.conf" &&\
    pg_ctl -D "$PGDATA" -w start &&\
    psql -c "ALTER USER postgres PASSWORD 'postgres';" &&\
    if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='airflow_db'" )" != '1' ]; then \
        psql -c "CREATE DATABASE airflow_db;" &&\
        psql -c "CREATE USER airflow_user WITH PASSWORD 'airflow_pass';" &&\
        psql -c "GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;" &&\
        psql -c "ALTER DATABASE airflow_db OWNER TO airflow_user;"; \
    fi &&\
    pg_ctl stop

USER root

EXPOSE 5434
CMD ["postgres"]
