
import sys
import csv
import logging

from collections import OrderedDict

# settings file names

from django.conf import settings
from django.db import connection
from django.db.utils import DataError
from bbga_data.models import Meta, Cijfers

log = logging.getLogger(__name__)


def to_int(value):
    return value if value != '.' else 0


def meta_row_mapping(row):
    return OrderedDict([
        ('sort', row[0]),
        ('thema', row[1]),
        ('variabele', row[2]),
        ('label', row[3]),
        ('definitie', row[4]),
        ('bron', row[5]),
        ('peildatum', row[6]),
        ('verschijningsfrequentie', row[7]),
        ('eenheid', row[8]),
        ('groep', row[9]),
        ('format', row[10]),
        ('thema_kleurentabel', row[11]),
        ('kleurenpalet', to_int(row[12])),
        ('minimum_aantal_inwoners', to_int(row[13])),
        ('minimum_aantal_woningen', to_int(row[14]))
    ])


def print_row(mapping):
    for k, v in mapping.items():
        mv = v[:30] if type(v) == str else 0
        l = len(v) if type(v) == str else 0
        print('%30s %40s %10s' % (k, mv, l))


def import_meta_csv(csv_path, table):

    with open(csv_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        # skip header
        headers = next(reader, None)

        if settings.DEBUG:
            for i, item in enumerate(headers):
                print(i, item)

        for i, row in enumerate(reader):
            try:
                _, created = Meta.objects.get_or_create(
                    **meta_row_mapping(row)
                )
            except DataError:
                log.error(row)
                print_row(meta_row_mapping(row))
                sys.exit(1)


def import_variable_csv(csv_file, table):
    """
    """
    log.debug('removing old variable data')
    # clear old data
    Cijfers.objects.all().delete()

    columns = ['jaar', 'gebiedcode15', 'variabele', 'waarde']

    sql_statement = """
    COPY {} ({})
    FROM STDIN
    WITH
    CSV
    DELIMITER ';'
    HEADER
    """.format(table, ", ".join(columns))

    log.debug('loading new variable data')

    with connection.cursor() as c:
        with open(csv_file, 'r') as open_file:
            c.copy_expert(sql_statement, open_file)
