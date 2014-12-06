from _helpers import cursor_wrap, dump


eparchies = {
    'Минско-Могилевская диоцезия': [
        'Минск',
        'Минская область',
        'Могилёвская область',
    ],
    'Витебская диоцезия': [
        'Витебская область',
    ],
    'Пинская диоцезия': [
        'Брестская область',
        'Гомельская область',
    ],
    'Гродненская диоцезия': [
        'Гродненская область',
    ],
}


@cursor_wrap
def main(cursor):
    base_sql = """
        (
            SELECT '{}' AS diocese, ST_AsGeoJSON(ST_Union(c.way))
            FROM osm_polygon c
            WHERE c.admin_level IN ('4') AND c.tags->'name:ru' IN ({})
            GROUP BY diocese
        )
    """
    sql = " UNION ".join(base_sql.format(diocese, ','.join("'{}'".format(item) for item in items))
                         for diocese, items in eparchies.items())
    cursor.execute(sql)
    dump(__file__, sorted(cursor.fetchall(), key=lambda item: item[0]),
         ('diocese', 'geojson'))


if __name__ == '__main__':
    main()
