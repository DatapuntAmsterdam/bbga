import sys

from django.core.management import BaseCommand

from bbga_data import import_data

import logging

log = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Import table data from csv

    clear data using:

    - manage.py migrate bbga_data zero
    - manage.py migrate bbga_data

    """
    tables = [
            'bbga_data_cijfers',
            'bbga_data_meta',
    ]

    def add_arguments(self, parser):

        parser.add_argument(
            'csv_source',
            nargs=1,
            type=str,
            help='CSV bron bestand')

        parser.add_argument(
            'table',
            nargs='?',
            type=str,
            default="bbga_data_cijfers",
            help='Doel tabel')

    def handle(self, *args, **options):
        """
        validate and execute import task
        """

        if not options['csv_source']:
            sys.exit(1)

        csv = options['csv_source'][0]
        table = options['table']

        assert table in self.tables

        if table == 'bbga_data_meta':
            # xsl output / converted to utf-8
            # needs some cleanup
            import_data.import_meta_csv(csv, table)
        elif table == 'bbga_data_cijfers':
            # tableaux export (clean)
            import_data.import_variable_csv(csv, table)

        else:
            log.error('nothing imported')
            sys.exit(1)
