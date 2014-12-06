from _helpers import cursor_wrap, dump


@cursor_wrap
def main(cursor):
    sql = "SELECT osm_id, name, ST_AsGeoJSON(way) FROM osm_polygon WHERE osm_id = -59065"
    cursor.execute(sql)
    dump(__file__, cursor.fetchall(), ('osmid', 'country', 'geojson'))


if __name__ == '__main__':
    main()
