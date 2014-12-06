from _helpers import cursor_wrap, dump


@cursor_wrap
def main(cursor):
    sql = """
        SELECT r.osm_id, c.name AS country, r.name AS region, ST_AsGeoJSON(r.way)
        FROM osm_polygon c
        LEFT JOIN osm_polygon r ON ST_Contains(c.way, r.way)
        WHERE c.osm_id = -59065 AND r.admin_level = '4'
        AND r.osm_id IN (-59189, -59506, -59161, -59275, -59195, -59752, -59162)
    """
    cursor.execute(sql)
    dump(__file__, sorted(cursor.fetchall(), key=lambda item: item[1:3]),
         ('osmid', 'country', 'region', 'geojson'))


if __name__ == '__main__':
    main()
