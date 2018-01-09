#!/usr/bin/env bash

set -u
set -e

cd ../../bbga && ./manage.py test
