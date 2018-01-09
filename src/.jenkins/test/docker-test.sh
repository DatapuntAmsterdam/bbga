#!/usr/bin/env bash

set -u
set -e
set -x

.jenkins/docker-wait.sh

./manage.py test
