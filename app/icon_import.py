#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
import (and export) font-awesome icons
"""
import json
import os
import sys
import dotenv
import argparse
from django.template.defaultfilters import slugify
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
            yield {
                'name': filename[:-4],
                'path': os.path.join(directory, filename),
                'tags': []
            }


def read_svg(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
        for record in data:
            yield record


def get_cursor(conn) -> psycopg2.extensions.cursor:
    return conn.cursor()


def get_content_type_and_tags(conn):

    with get_cursor(conn) as cursor:
        cursor.execute("select id from django_content_type where app_label='main' and model='icon'")
        content_id = cursor.fetchone()[0]

    taginfo = {}
    # pre-fetch the list of all known tags
    with get_cursor(conn) as cursor:
        cursor.execute("select id, name from taggit_tag")
        # map name to id
        for id, name in cursor.fetchmany(100000):
            taginfo[name] = id

    return content_id, taginfo


def dump_svg(directory=SVG_DIR):
    conn = dbconn()

    content_id, taginfo = get_content_type_and_tags(conn)
    # main query
    with get_cursor(conn) as cursor:
        cursor.execute("select id, name from main_icon")
        for icon_id, icon_name in cursor.fetchmany(100000):
            # get any tags
            with get_cursor(conn) as tags_cursor:
                tags_cursor.execute("select tt.name \n" +
                                    "  from taggit_taggeditem ti \n" +
                                    "  left join taggit_tag tt on ti.tag_id = tt.id \n" +
                                    " where ti.content_type_id = %s\n" +
                                    "   and ti.object_id = %s", (content_id, icon_id))
                tags = [tag for (tag,) in tags_cursor.fetchmany(1000000)]
            yield {
                'name': icon_name,
                'path': f"{os.path.join(directory, icon_name)}.svg",
                'tags': tags
            }


def import_icons(source=scan_svg, *args):
    conn = dbconn()

    content_id, taginfo = get_content_type_and_tags(conn)

    with get_cursor(conn) as cursor:
        cursor.execute('delete from main_icon where true')

    count = 0
    for record in source(*args):
        name, path, tags = record.get('name'), record.get('path'), record.get('tags')
        if name and path:
            with open(path, 'r') as fp:
                print(f"\r{name:<40}", end='')
                count += 1
                record['svg'] = fp.read()

                with get_cursor(conn) as cursor:
                    cursor.execute("insert into main_icon (name, svg) values (%(name)s, %(svg)s) returning id", record)
                    icon_id = cursor.fetchone()[0]

                # now sort out the tags
                tags = record.get('tags')
                if icon_id and tags:
                    # --- upsert tags ---
                    # check the list of tags to see if any are not yet known
                    # remove all existing tags for this record
                    with get_cursor(conn) as cursor:
                        cursor.execute(
                            "delete from taggit_taggeditem where content_type_id=%s and object_id=%s",
                            (icon_id, content_id))
                    for tag in tags:
                        if tag not in taginfo:
                            # insert new tags
                            with get_cursor(conn) as cursor:
                                cursor.execute(
                                    "insert into taggit_tag (name, slug) values (%s, %s) returning id",
                                    (tag, slugify(tag)))
                                # and record the associated id
                                taginfo[tag] = cursor.fetchone()[0]
                        # --- refresh tags ---
                        # and insert the tag for this icon anew
                        with get_cursor(conn) as cursor:
                            cursor.execute(
                                "insert into taggit_taggeditem (object_id, content_type_id, tag_id) "
                                "values (%s, %s, %s)", (icon_id, content_id, taginfo[tag]))

    print(f"\nDone. {count} icons imported")


def main(args: argparse.Namespace):
    if args.define:
        for define in args.define:
            envstr = define.split('=', 1)
            if len(envstr) < 2:
                raise ValueError('-D input must be in KEY=VALUE format')
            os.environ[envstr[0]] = os.environ[envstr[1]]
    if args.input:
        input_func = read_svg
        input_args = args.input
    else:
        input_func = scan_svg
        input_args = args.dir
    # interpretation of -json and/or -import differs if '--list' is used
    if args.list:
        for data in input_func(input_args):
            name, path, tags = data['name'], data['path'], data['tags']
            print(f'{{name: {name}, path: {path}, tags: {tags}')
    elif args.json:
        all_data = [data for data in input_func(input_args)]
        with open(args.json, 'a' if args.append else 'w') as fp:
            json.dump(all_data, fp, indent=2)
    elif args.source:
        all_data = [data for data in dump_svg(args.dir)]
        with open(args.source, 'a' if args.append else 'w') as fp:
            json.dump(all_data, fp, indent=2)
    else:
        import_icons(input_func, input_args)

if __name__ == '__main__':
    """
    enhanced to provide the following functions:
        - default - directly import SVGs into db
        - output records as json to a named file
        - read records from a json file and import into db
        - list icons, from SVG dir or json file
    """

    dotenv.load_dotenv('../.env')

    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), description=__doc__)

    parser.add_argument('-D', '--define', type=str, action='append', nargs='*',
                        help='Override environment variables [key=value] multiple allowed')
    parser.add_argument('-d', '--dir', type=str, action='store', default=SVG_DIR,
                        help='Override the location (directory) of svg files')
    parser.add_argument('-j', '--json', action='store',
                        help='Output records as json instead of importing into database')
    parser.add_argument('-a', '--append', action='store',
                        help='Append output to json instead of overwriting')
    parser.add_argument('-i', '--input', action='store',
                        help=f'Import named json file instead of scanning {SVG_DIR}')
    parser.add_argument('-s', '--source', action='store',
                        help=f'Export icon data from db as json and store in named file')
    parser.add_argument('-l', '--list', action='store_true',
                        help='List scanned or read icon definitions')

    argv = parser.parse_args()
    main(argv)
