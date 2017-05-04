#!/usr/bin/env bash

set -u
set -e

# wait for postgres
while ! nc -z ${DATABASE_PORT_5432_TCP_ADDR:-database} ${DATABASE_PORT_5432_TCP_PORT:-5406}
do
	echo "Waiting for postgres..."
	echo "${DATABASE_PORT_5432_TCP_ADDR:-database} ${DATABASE_PORT_5432_TCP_PORT:-5406}"
	sleep 1
done
