#!/usr/bin/env bash

set -u
set -e

cd bbga
yes yes | python manage.py migrate --noinput
