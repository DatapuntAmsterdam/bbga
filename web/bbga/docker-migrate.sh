#!/usr/bin/env bash

set -u
set -e

source docker-wait.sh 
yes yes | python manage.py migrate --noinput
