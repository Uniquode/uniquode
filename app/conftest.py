import os
import sys
import pytest
from django.db import connections

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DATABASE_DEFAULT = 'uniquode'
DATABASE_TEST = 'uniquode_test'


def run_sql(sql):
    conn = psycopg2.connect(os.environ['DJANGO_DATABASE_URL'])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.yield_fixture(scope='session')
def django_db_setup():
    from django.conf import settings

    run_sql(f'DROP DATABASE IF EXISTS {DATABASE_TEST}')
    run_sql(f'CREATE DATABASE {DATABASE_TEST} TEMPLATE {DATABASE_DEFAULT}')

    settings.DATABASES['default']['NAME'] = DATABASE_TEST

    yield

    for connection in connections.all():
        connection.close()

    run_sql(f'DROP DATABASE {DATABASE_TEST}')

sys.path.append(os.path.join(os.path.dirname(__file__), 'tests', 'helpers'))
os.environ['DJANGO_MODE'] = 'test'
