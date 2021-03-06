#!/bin/sh

set -e
set -u

DIR="$(dirname $0)"

dc() {
	docker-compose -p bbga -f ${DIR}/docker-compose.yml $*
}

trap 'dc kill ; dc down ; dc rm -f' EXIT

rm -rf ${DIR}/backups
mkdir -p ${DIR}/backups

echo "Building dockers"
dc down
dc rm
dc pull
dc build

dc up -d database
dc run importer .jenkins/docker-wait.sh

dc run --rm importer ./import_data.sh

echo "Running backups"
dc exec -T database backup-db.sh bbga
dc down -v
echo "Done"
