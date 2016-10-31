# settings file names

from django.db import connection


def import_csv(csv_path):
    with connection.cursor() as c:
        sql_stmt = """

        """
        c.execute(sql_stmt)
