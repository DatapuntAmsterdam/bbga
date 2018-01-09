#!/usr/bin/env bash

set -u
set -e
set -x

yes yes | python manage.py migrate --noinput
