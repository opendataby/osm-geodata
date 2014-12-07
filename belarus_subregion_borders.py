from _helpers import cursor_wrap, dump


@cursor_wrap
def main(cursor):
    sql = """
        SELECT s.osm_id,
               c.tags->'int_name' AS country, r.tags->'int_name' AS region, s.tags->'int_name' AS subregion,
               c.tags->'name:be' AS countryBy, r.tags->'name:be' AS regionBy, s.tags->'name:be' AS subregionBy,
               c.tags->'name:ru' AS countryRu, r.tags->'name:ru' AS regionRu, s.tags->'name:ru' AS subregionRu,
               ST_AsGeoJSON(s.way)
        FROM osm_polygon c
        LEFT JOIN osm_polygon r ON ST_Contains(c.way, r.way)
        LEFT JOIN osm_polygon s ON ST_Contains(r.way, s.way)
        WHERE c.osm_id = -59065 AND r.admin_level = '4' AND s.admin_level = '6'
    """
    cursor.execute(sql)
    dump(__file__, sorted(cursor.fetchall(), key=lambda item: item[1:4]), (
        'osmid',
        'country', 'region', 'subregion',
        'countryBy', 'regionBy', 'subregionBy',
        'countryRu', 'regionRu', 'subregionRu',
        'geojson',
    ))


if __name__ == '__main__':
    main()
