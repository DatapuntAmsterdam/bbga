#!/usr/bin/env bash

set -u
set -e

cd /app

# collect static files
python manage.py collectstatic --noinput

# migrate database tables
yes yes | python manage.py migrate --noinput

# run import
#python manage.py run_import

#python manage.py run_import /app/data/bbga_csv/metadata_utf8.csv  bbga_data_meta

#python manage.py run_import /app/data/bbga_csv/bbga_tableau
#

# sync geo views
# python manage.py sync_views

# run uwsgi
exec uwsgi --ini /app/uwsgi.ini
