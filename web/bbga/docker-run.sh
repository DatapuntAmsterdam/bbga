#!/usr/bin/env bash

set -u
set -e

# collect static files
source docker-migrate.sh || echo "Could not migrate, ignoring"

# run uwsgi
exec uwsgi
