#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
CONTAINER=$(docker-compose -f "$DIR"/../docker-compose.yml ps | grep hr_system_django | head -n 1 | cut -d' ' -f1)
read -r -e -p "App name: " APP_NAME
read -r -e -p "Squash from: " SQUASH_FROM
read -r -e -p "Squash to: " SQUASH_TO
docker exec -it --env DATABASE_URL='postgres://local_db:local_db@hr_system_db/local_db' "$CONTAINER" python /app/manage.py squashmigrations "${APP_NAME}" "${SQUASH_FROM}" "${SQUASH_TO}"
