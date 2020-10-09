# -*- coding: utf-8 -*-
"""
Import font-awesome icons into the database
"""
import os
import dotenv

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DATABASE_VAR = 'DJANGO_DATABASE_URL'
SVG_DIR = 'node_modules/@fortawesome/fontawesome-free/svgs/solid'


def dbconn(var=DATABASE_VAR):
    conn = psycopg2.connect(os.environ[var])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn



def scan_svg(directory=SVG_DIR):
    for filename in os.listdir(directory):
        if filename.endswith('.svg'):
            yield (filename[:-4], os.path.join(directory, filename))


def import_icons():
    conn = dbconn()
    with conn.cursor() as cursor:
        cursor.execute('delete from main_icon where true')
        count = 0
        for name, path in scan_svg():
            with open(path, 'r') as fp:
                print(f"{name:<40}\r", end='')
                count += 1
                svg = fp.read()
                cursor.execute(f"insert into main_icon (name, svg) values ('{name}', '{svg}')")
        print(f"done. {count} icons imported          ")

if __name__ == '__main__':
    dotenv.load_dotenv('../.env')
    import_icons()
