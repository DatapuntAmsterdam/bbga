#!/usr/bin/env bash

set -u
set -e

# wait for postgres
while ! nc -z ${BBGA_DB_PORT_5432_TCP_ADDR} ${BBGA_DB_PORT_5432_TCP_PORT}
do
	echo "Waiting for postgres..."
	sleep 0.1
done
