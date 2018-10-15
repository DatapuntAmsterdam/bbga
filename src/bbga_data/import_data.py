import csv
import logging
import sys
from collections import OrderedDict

from django.conf import settings
from django.core.exceptions import FieldError
from django.db import connection
from django.db.utils import DataError

from bbga_data.models import Cijfers, Meta

log = logging.getLogger(__name__)


def to_int(value):
    if not value:
        return 0
    if value == '.':
        return 0
    return value


# List of known headers
META_HEADERS = [
    "sort",
    "begrotingsprogramma",
    "thema",
    "variabele",
    "label",
    "labelkort",
    "definitie",
    "bron",
    "peildatum",
    "verschijningsfrequentie",
    "rekeneenheid",
    "symbool",
    "groep",
    "format",
    "kleurenpalet",
    "legendacode",
    "berekende variabelen",
    "sd minimum bevtotaal",
    "sd minimum wvoorrbag",
    "thema kerncijfertabel",
    "geenkerncijfer",
]


def meta_row_mapping(row):
    return OrderedDict([
        ('sort', row['sort']),
        ('thema', row['thema']),
        ('variabele', row['variabele']),
        ('label', row['label']),
        ('definitie', row['definitie']),
        ('bron', row['bron']),
        ('peildatum', row['peildatum']),
        ('verschijningsfrequentie', row['verschijningsfrequentie']),
        ('eenheid', to_int(row['rekeneenheid'])),
        ('symbool', row['symbool']),
        ('groep', row['groep']),
        ('format', row['format']),  # 'K'
        ('thema_kleurentabel', row['thema kerncijfertabel']),
        # ('kleurenpalet', to_int(row['kleurenpalet'])),
        ('legendacode', to_int(row['legendacode'])),
        ('minimum_aantal_inwoners', to_int(row['sd minimum bevtotaal'])),
        ('minimum_aantal_woningen', to_int(row['sd minimum wvoorrbag']))
    ])


def print_row(mapping):
    print('\n\n%30s %40s %10s\n' % ('map', 'rowvalue', 'length'))
    for i, (k, v) in enumerate(mapping.items()):
        mv = v[:30] if isinstance(v, str) else 0
        length = len(v) if isinstance(v, str) else 0
        print('%2d %30s %40s %10s' % (i, k, mv, length))


def create_row_mapping(headers, row):
    rowmap = {}
    error_msg = "Header errors: \n"
    errors = ""
    for k, v in zip(headers, row):
        k = k.lower()
        k = k.replace('_', ' ')

        if k not in META_HEADERS:
            errors = f"{errors} {k} is an unknown header.\n"
        rowmap[k] = v

    if errors:
        log.error('%s %s', error_msg, errors)
        raise ValueError(errors)

    return rowmap


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

            rowdata = create_row_mapping(headers, row)

            try:
                _, _created = Meta.objects.get_or_create(
                    **meta_row_mapping(rowdata)
                )
            except(ValueError, DataError, FieldError) as e:
                log.error(e)
                log.error(row)

                for ir, (h, v) in enumerate(zip(headers, row)):
                    print('%2s %35s : %s' % (i, h, v))

                log.debug('Parsed Row mapping')
                print_row(meta_row_mapping(rowdata))
                log.debug('Actual Row mapping')
                print_row(rowdata)

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
