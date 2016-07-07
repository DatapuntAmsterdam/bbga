#!/bin/bash

set -e
set -u

# wait for database to load
source docker-wait.sh

echo 'unzipping latest bbga file'

unzip $(ls -Art data/*.zip | tail -n 1) -f -d /app/unzipped/

echo 'convert meta data to utf-8'

cd /app/unzipped/

iconv -f WINDOWS-1251 -t UTF-8 -o metadata_utf8.csv metadata.csv

cd /app

echo 'Clear current data'

#python manage.py migrate bbga_data zero
# migrate database tables
yes yes | python manage.py migrate --noinput


echo 'Loading Meta data'

python manage.py run_import /app/unzipped/metadata_utf8.csv  bbga_data_meta

echo 'Loading bbga cijfers ~1.000.000 row'

python manage.py run_import /app/unzipped/bbga_tableau.csv

echo 'Import BBGA DONE'
