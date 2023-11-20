#!/bin/bash
DB_USER="local_db"
DB_NAME="local_db"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
CONTAINER=$(docker-compose -f "$DIR"/../docker-compose.yml ps | grep hr_system_db | cut -d' ' -f1)
docker exec -it "$CONTAINER" /usr/bin/pg_dump -U ${DB_USER} -d ${DB_NAME}
