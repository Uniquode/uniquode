import os
import pytest
from django.db import connections

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DATABASE_DEFAULT = 'uniquode'
DATABASE_TEST = 'uniquode_test'
os.environ['DJANGO_MODE'] = 'test'


def run_sql(sql, var='DJANGO_DATABASE_URL'):
    conn = psycopg2.connect(os.environ[var])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.yield_fixture(scope='session')
def django_db_setup():
    from django.conf import settings

    # override default url so we can terminate sessions as sa
    run_sql("SELECT pg_terminate_backend(pid) "
            "FROM postgres.pg_catalog.pg_stat_activity "
            f"WHERE datname='{DATABASE_DEFAULT}'", var='DJANGO_POSTGRES_URL')

    run_sql(f'DROP DATABASE IF EXISTS {DATABASE_TEST}')
    run_sql(f'CREATE DATABASE {DATABASE_TEST} TEMPLATE {DATABASE_DEFAULT}')

    settings.DATABASES['default']['NAME'] = DATABASE_TEST

    yield

    for connection in connections.all():
        connection.close()

    run_sql(f'DROP DATABASE {DATABASE_TEST}')
