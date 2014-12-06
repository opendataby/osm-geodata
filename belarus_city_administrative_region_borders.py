from _helpers import cursor_wrap, dump


@cursor_wrap
def main(cursor):
    sql = """
        SELECT cr.osm_id, c.name AS country, '' AS region, '' AS subregion, ct.name AS city, cr.name AS region, ST_AsGeoJSON(cr.way)
        FROM osm_polygon c
        LEFT JOIN osm_polygon ct ON ST_Contains(c.way, ct.way)
        LEFT JOIN osm_polygon cr ON ST_Contains(ct.way, cr.way)
        WHERE c.osm_id = -59065
        AND ct.admin_level = '4' AND ct.tags->'place' = 'city'
        AND cr.admin_level = '9'

        UNION

        SELECT cr.osm_id, c.name AS country, r.name AS region, '' AS subregion, ct.name AS city, cr.name AS region, ST_AsGeoJSON(cr.way)
        FROM osm_polygon c
        LEFT JOIN osm_polygon r ON ST_Contains(c.way, r.way)
        LEFT JOIN osm_polygon ct ON ST_Contains(r.way, ct.way)
        LEFT JOIN osm_polygon cr ON ST_Contains(ct.way, cr.way)
        WHERE c.osm_id = -59065
        AND r.admin_level = '4' AND ct.admin_level = '6' AND ct.tags->'place' = 'city'
        AND cr.admin_level = '9'

        UNION

        SELECT cr.osm_id, c.name AS country, r.name AS region, s.name AS subregion, ct.name AS city, cr.name AS region, ST_AsGeoJSON(cr.way)
        FROM osm_polygon c
        LEFT JOIN osm_polygon r ON ST_Contains(c.way, r.way)
        LEFT JOIN osm_polygon s ON ST_Contains(r.way, s.way)
        LEFT JOIN osm_polygon ct ON ST_Contains(s.way, ct.way)
        LEFT JOIN osm_polygon cr ON ST_Contains(ct.way, cr.way)
        WHERE c.osm_id = -59065
        AND r.admin_level = '4' AND s.admin_level = '6' AND ct.admin_level NOT IN ('4', '6') AND ct.tags->'place' = 'city'
        AND cr.admin_level = '9'
    """
    cursor.execute(sql)
    dump(__file__, sorted(cursor.fetchall(), key=lambda item: item[1:6]),
        ('osmid', 'country', 'region', 'subregion', 'city', 'cityAdministrativeRegion', 'geojson'))


if __name__ == '__main__':
    main()
