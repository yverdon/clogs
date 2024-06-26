#!/usr/bin/env bash

set -e


MAKE_MIGRATIONS=0
BUILD=

while getopts 'bm' opt; do
  case "$opt" in
    b)
      echo "-> Rebuild docker image"
      BUILD="--build"
      ;;
    m)
      echo "-> Make migrations"
      MAKE_MIGRATIONS=1
      ;;
    ?|h)
      echo "Usage: $(basename $0) [-bm]"
      exit 1
      ;;
  esac
done

docker compose down -v --remove-orphans || true
docker compose up ${BUILD} -d

if  [[ ${MAKE_MIGRATIONS} -eq 1 ]]; then
  find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
  find . -path "*/migrations/*.pyc"  -delete
  docker compose exec clogs python manage.py makemigrations
fi

docker compose exec clogs python manage.py collectstatic --no-input
docker compose exec clogs python manage.py migrate
docker compose exec clogs python manage.py populate_users
