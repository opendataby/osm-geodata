from _helpers import cursor_wrap, dump


@cursor_wrap
def main(cursor):
    sql = """SELECT osm_id,
                    tags->'int_name',
                    tags->'name:be',
                    tags->'name:ru',
                    ST_AsGeoJSON(way)
             FROM osm_polygon
             WHERE osm_id = -59065"""
    cursor.execute(sql)
    dump(__file__, cursor.fetchall(), ('osmid', 'country', 'countryBy', 'countryRu', 'geojson'))


if __name__ == '__main__':
    main()
