#!/bin/bash
DB_USER="local_db"
DB_NAME="local_db"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
CONTAINER=$(docker-compose -f "$DIR"/../docker-compose.yml ps | grep hr_system_db | cut -d' ' -f1)
read -r -e -p "SQL dump filename (has to be in the same folder): " FILE_PATH
docker exec -it "$CONTAINER" /usr/bin/psql -U ${DB_USER} -d postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'local_db' AND pid <> pg_backend_pid();"
docker exec -it "$CONTAINER" /usr/bin/psql -U ${DB_USER} -d postgres -c "drop database local_db;"
docker exec -it "$CONTAINER" /usr/bin/psql -U ${DB_USER} -d postgres -c "create database local_db;"
docker exec -i "$CONTAINER" /usr/bin/psql -U ${DB_USER} -d ${DB_NAME} < "${FILE_PATH}"
