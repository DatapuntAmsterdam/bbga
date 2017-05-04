import csv
import logging
import sys
from collections import OrderedDict

from django.conf import settings
from django.db import connection
from django.db.utils import DataError

from bbga_data.models import Meta, Cijfers

log = logging.getLogger(__name__)


def to_int(value):
    if not value:
        return 0
    if value == '.':
        return 0
    return value


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
        ('eenheid', to_int(row[8])),
        ('groep', row[9]),
        ('format', row[10]),  # 'K'
        ('thema_kleurentabel', row[12]),
        ('kleurenpalet', to_int(row[13])),
        ('minimum_aantal_inwoners', to_int(row[14])),
        ('minimum_aantal_woningen', to_int(row[15]))
    ])


def print_row(mapping):
    print('\n\n%30s %40s %10s\n' % ('map', 'rowvalue', 'length'))
    for k, v in mapping.items():
        mv = v[:30] if isinstance(v, str) else 0
        l = len(v) if isinstance(v, str) else 0
        print('%30s %40s %10s' % (k, mv, l))


def import_meta_csv(csv_path, _table):
    with open(csv_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        # skip header

        headers = next(reader, None)

        Meta.objects.all().delete()

        if settings.DEBUG:
            for i, item in enumerate(headers):
                print(i, item)

        for i, row in enumerate(reader):
            try:
                _, _created = Meta.objects.get_or_create(
                    **meta_row_mapping(row)
                )
            except(ValueError, DataError) as e:
                log.error(e)
                log.error(row)
                for ir, v in enumerate(row):
                    print(ir, v)
                print_row(meta_row_mapping(row))
                if i > 3:
                    sys.exit(1)


def import_variable_csv(csv_file, table):
    """
    Import the large cijfers dataset
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
