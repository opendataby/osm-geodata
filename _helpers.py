from collections import defaultdict
from contextlib import contextmanager
import csv
from datetime import datetime
import functools
import json

import psycopg2


@contextmanager
def cursor_context():
    conn = psycopg2.connect(dbname='osm', user='', password='',
                            host='127.0.0.1', port='5432')
    cursor = conn.cursor()
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, cursor)
    yield cursor
    cursor.close()
    conn.close()


def timing(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = fn(*args, **kwargs)
        print(datetime.now() - start)
        return result
    return wrapper


def cursor_wrap(fn):
    @timing
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        with cursor_context() as cursor:
            kwargs.update(cursor=cursor)
            return fn(*args, **kwargs)
    return wrapper


def osm_id(id, type=None):
    assert type in [None, 'n', 'w', 'r']
    id = str(id)
    if type:
        return type + id.strip('-')
    if id.isdigit():
        return 'w' + id
    if id[0] == '-' and id[1:].isdigit():
        return 'r' + id[1:]
    assert id.startswith(('n', 'w', 'r'))
    return id


def minify_json(geojson):
    if isinstance(geojson, str):
        geojson = json.loads(geojson)
    return json.dumps(geojson, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'))


processes = defaultdict(lambda: lambda value: value, {
    'osmid': osm_id,
    'geojson': minify_json,
})


def dump(file_name, items, fields):
    with open(file_name.replace('.py', '.csv'), 'w') as file:
        writer = csv.writer(file)
        writer.writerow(fields)
        writer.writerows([
            [processes[field](value) for field, value in zip(fields, item)]
            for item in items
        ])
