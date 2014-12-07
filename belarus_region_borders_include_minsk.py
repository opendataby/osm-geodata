from _helpers import cursor_wrap, dump


@cursor_wrap
def main(cursor):
    sql = """
        SELECT r.osm_id,
               c.tags->'int_name' AS country, r.tags->'int_name' AS region,
               c.tags->'name:be' AS countryBy, r.tags->'name:be' AS regionBy,
               c.tags->'name:ru' AS countryRu, r.tags->'name:ru' AS regionRu,
               ST_AsGeoJSON(r.way)
        FROM osm_polygon c
        LEFT JOIN osm_polygon r ON ST_Contains(c.way, r.way)
        WHERE c.osm_id = -59065 AND r.admin_level = '4'
        AND r.osm_id IN (-59189, -59506, -59161, -59275, -59162)

        UNION

        SELECT -59752,
               FIRST(c.tags->'int_name') AS country, FIRST(r.tags->'int_name') AS region,
               FIRST(c.tags->'name:be') AS countryBy, FIRST(r.tags->'name:be') AS regionBy,
               FIRST(c.tags->'name:ru') AS countryRu, FIRST(r.tags->'name:ru') AS regionRu,
               ST_AsGeoJSON(ST_Union(r.way))
        FROM osm_polygon c
        LEFT JOIN osm_polygon r ON ST_Contains(c.way, r.way)
        WHERE c.osm_id = -59065 AND r.admin_level = '4'
        AND r.osm_id IN (-59752, -59195)
    """
    cursor.execute(sql)
    dump(__file__, sorted(cursor.fetchall(), key=lambda item: item[1:3]), (
        'osmid',
        'country', 'region',
        'countryBy', 'regionBy',
        'countryRu', 'regionRu',
        'geojson',
    ))


if __name__ == '__main__':
    main()
