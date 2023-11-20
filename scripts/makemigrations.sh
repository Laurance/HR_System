#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
CONTAINER=$(docker-compose -f "$DIR"/../docker-compose.yml ps | grep hr_system_django | head -n 1 | cut -d' ' -f1)
docker exec -it --env DATABASE_URL='postgres://local_db:local_db@hr_system_db/local_db' "$CONTAINER" python /app/manage.py makemigrations
