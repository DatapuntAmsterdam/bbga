#!/bin/bash

set -e
set -u
set -x

echo 'Download latest BBGA file'

python download_latest.py

echo 'convert meta data to utf-8'

iconv -f iso-8859-1 -t UTF-8 -o /app/data/metadata_utf8.csv /app/data/metadata.csv

echo 'Clear current data'

#python manage.py migrate bbga_data zero
# migrate database tables

yes yes | python manage.py migrate --noinput

echo 'Loading Meta data'

python manage.py run_import /app/data/metadata_utf8.csv  bbga_data_meta

echo 'Loading bbga cijfers ~1.000.000 rows'

python manage.py run_import /app/data/bbga.csv

echo 'Import BBGA DONE'
