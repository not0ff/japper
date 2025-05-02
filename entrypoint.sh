#!/usr/bin/env bash
set -e

until pg_isready -h db -p 5432 -U "${POSTGRES_USER}"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
 >&2 echo "Postgres is up - continuing"

flask db upgrade --directory src/migrations
exec gunicorn --bind 0.0.0.0:8000 wsgi:app
