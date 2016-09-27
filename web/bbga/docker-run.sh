#!/usr/bin/env bash

set -u
set -e

source docker-wait.sh

# collect static files
source docker-migrate.sh || echo "Could not migrate, ignoring"

# run uwsgi
exec uwsgi --ini /app/uwsgi.ini
