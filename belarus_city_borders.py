from _helpers import cursor_wrap, dump


@cursor_wrap
def main(cursor):
    sql = """
        SELECT ct.osm_id,
               c.tags->'int_name' AS country, '' AS region, '' AS subregion, ct.tags->'int_name' AS city,
               c.tags->'name:be' AS countryBy, '' AS regionBy, '' AS subregionBy, ct.tags->'name:be' AS cityBy,
               c.tags->'name:ru' AS countryRu, '' AS regionRu, '' AS subregionRu, ct.tags->'name:ru' AS cityRu,
               ST_AsGeoJSON(ct.way)
        FROM osm_polygon c
        LEFT JOIN osm_polygon ct ON ST_Contains(c.way, ct.way)
        WHERE c.osm_id = -59065 AND ct.admin_level = '4'
        AND ct.tags->'place' IN ('city', 'town')

        UNION

        SELECT ct.osm_id,
               c.tags->'int_name' AS country, r.tags->'int_name' AS region, '' AS subregion, ct.tags->'int_name' AS city,
               c.tags->'name:be' AS countryBy, r.tags->'name:be' AS regionBy, '' AS subregionBy, ct.tags->'name:be' AS cityBy,
               c.tags->'name:ru' AS countryRu, r.tags->'name:ru' AS regionRu, '' AS subregionRu, ct.tags->'name:ru' AS cityRu,
               ST_AsGeoJSON(ct.way)
        FROM osm_polygon c
        LEFT JOIN osm_polygon r ON ST_Contains(c.way, r.way)
        LEFT JOIN osm_polygon ct ON ST_Contains(r.way, ct.way)
        WHERE c.osm_id = -59065 AND r.admin_level = '4' AND ct.admin_level = '6'
        AND ct.tags->'place' IN ('city', 'town')

        UNION

        SELECT ct.osm_id,
               c.tags->'int_name' AS country, r.tags->'int_name' AS region, s.tags->'int_name' AS subregion, ct.tags->'int_name' AS city,
               c.tags->'name:be' AS countryBy, r.tags->'name:be' AS regionBy, s.tags->'name:be' AS subregionBy, ct.tags->'name:be' AS cityBy,
               c.tags->'name:ru' AS countryRu, r.tags->'name:ru' AS regionRu, s.tags->'name:ru' AS subregionRu, ct.tags->'name:ru' AS cityRu,
               ST_AsGeoJSON(ct.way)
        FROM osm_polygon c
        LEFT JOIN osm_polygon r ON ST_Contains(c.way, r.way)
        LEFT JOIN osm_polygon s ON ST_Contains(r.way, s.way)
        LEFT JOIN osm_polygon ct ON ST_Contains(s.way, ct.way)
        WHERE c.osm_id = -59065 AND r.admin_level = '4' AND s.admin_level = '6'
        AND ct.tags->'place' IN ('city', 'town')
    """
    cursor.execute(sql)
    dump(__file__, sorted(cursor.fetchall(), key=lambda item: item[1:5]), (
        'osmid',
        'country', 'region', 'subregion', 'city',
        'countryBy', 'regionBy', 'subregionBy', 'cityBy',
        'countryRu', 'regionRu', 'subregionRu', 'cityRu',
        'geojson',
    ))


if __name__ == '__main__':
    main()
