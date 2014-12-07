from itertools import chain

from _helpers import cursor_wrap, dump


subregion_cities = [
    # Брестская область
    (-71116, -3629362),  # Барановичский район: Барановичи
    (-59188, -72615),  # Брестский район: Брест
    (-71119, -1749248),  # Пинский район: Пинск

    # Витебская область
    (-59504, -68614),  # Витебский район: Витебск
    (-70671, -1749242),  # Полоцкий район: Новополоцк

    # Гомельская область
    (-1469691, -163244),  # Гомельский район: Гомель

    # Гродненская область
    (-59273, -130921),  # Гродненский район: Гродно

    # Минская область
    (-59190, -59195),  # Минский район: Минск
    (-69554, -79911),  # Смолевичский район: Жодино

    # Могилёвская область
    (-59148, -167857),  # Бобруйский район: Бобруйск
    (-62147, -62145),  # Могилёвский район: Могилев
]


@cursor_wrap
def main(cursor):
    sql_main = """
        SELECT s.osm_id,
              c.tags->'int_name' AS country, r.tags->'int_name' AS region, s.tags->'int_name' AS subregion,
              c.tags->'name:be' AS countryBy, r.tags->'name:be' AS regionBy, s.tags->'name:be' AS subregionBy,
              c.tags->'name:ru' AS countryRu, r.tags->'name:ru' AS regionRu, s.tags->'name:ru' AS subregionRu,
              ST_AsGeoJSON(s.way)
        FROM osm_polygon c
        LEFT JOIN osm_polygon r ON ST_Contains(c.way, r.way)
        LEFT JOIN osm_polygon s ON ST_Contains(r.way, s.way)
        WHERE c.osm_id = -59065 AND r.admin_level = '4' AND s.admin_level = '6'
        AND s.osm_id NOT IN ({})
    """
    sql_union = """
        SELECT FIRST(osm_id),
               FIRST(country), FIRST(region), FIRST(subregion),
               FIRST(countryBy), FIRST(regionBy), FIRST(subregionBy),
               FIRST(countryRu), FIRST(regionRu), FIRST(subregionRu),
               ST_AsGeoJSON(ST_Union(way))
        FROM (
            SELECT * FROM (
                SELECT {0} AS osm_id,
                       c.tags->'int_name' AS country, r.tags->'int_name' AS region, s.tags->'int_name' AS subregion,
                       c.tags->'name:be' AS countryBy, r.tags->'name:be' AS regionBy, s.tags->'name:be' AS subregionBy,
                       c.tags->'name:ru' AS countryRu, r.tags->'name:ru' AS regionRu, s.tags->'name:ru' AS subregionRu,
                       s.way
                FROM osm_polygon c
                LEFT JOIN osm_polygon r ON ST_Contains(c.way, r.way)
                LEFT JOIN osm_polygon s ON ST_Contains(r.way, s.way)
                WHERE c.osm_id = -59065 AND r.admin_level = '4' AND s.admin_level = '6' AND s.osm_id IN ({1})

                UNION

                SELECT {0} AS osm_id,
                       NULL AS country, NULL AS region, NULL AS subregion,
                       NULL AS countryBy, NULL AS regionBy, NULL AS subregionBy,
                       NULL AS countryRu, NULL AS regionRu, NULL AS subregionRu,
                       s.way
                FROM osm_polygon s
                WHERE s.osm_id IN ({1})
            ) s ORDER BY ST_AREA(way) DESC
        ) s
    """
    sql = 'UNION'.join(
        [sql_main.format(', '.join(map(str, chain.from_iterable(subregion_cities))))] +
        [sql_union.format(sub_or_city[0], ', '.join(map(str, sub_or_city))) for sub_or_city in subregion_cities]
    )
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
