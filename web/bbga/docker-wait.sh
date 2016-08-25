#!/usr/bin/env bash

set -u
set -e

# wait for postgres
while ! nc -z ${DATABASE_PORT_5432_TCP_ADDR} ${DATABASE_PORT_5432_TCP_PORT}
do
	echo "Waiting for postgres..."
	echo "${DATABASE_PORT_5432_TCP_ADDR} ${DATABASE_PORT_5432_TCP_PORT}"
	sleep 1
done
