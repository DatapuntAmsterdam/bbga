#!/usr/bin/env bash

set -u
set -e

yes yes | python manage.py migrate --noinput
