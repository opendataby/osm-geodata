from _helpers import cursor_wrap, dump


@cursor_wrap
def main(cursor):
    sql = """
        SELECT s.osm_id, c.name AS country, r.name AS region, s.name AS subregion, ST_AsGeoJSON(s.way)
        FROM osm_polygon c
        LEFT JOIN osm_polygon r ON ST_Contains(c.way, r.way)
        LEFT JOIN osm_polygon s ON ST_Contains(r.way, s.way)
        WHERE c.osm_id = -59065 AND r.admin_level = '4' AND s.admin_level = '6'
    """
    cursor.execute(sql)
    dump(__file__, sorted(cursor.fetchall(), key=lambda item: item[1:4]),
         ('osmid', 'country', 'region', 'subregion', 'geojson'))


if __name__ == '__main__':
    main()
