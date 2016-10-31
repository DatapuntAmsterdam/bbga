#!/usr/bin/env bash

set -u
set -e

source docker-wait.sh
exec python manage.py test