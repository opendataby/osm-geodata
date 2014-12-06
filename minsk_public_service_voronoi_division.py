import csv

from _helpers import cursor_wrap, dump


def sort_numbers(args):
    name, geojson = args
    if name.isdigit():
        return name.zfill(10)
    return name


@cursor_wrap
def main(cursor):
    spamreader = csv.reader(open("jes_minsk_edit_v14.csv", "r"))
    normalized_data = [[c for c in row] for i, row in enumerate(spamreader) if i > 0]
    data = [(j, so, ",".join(["'{}'".format(ni.strip()) for ni in n.split(",")]))
            for i, r, j, s, sf, so, n, no, nno in normalized_data]

    house_sql = "SELECT '{}' jes, p.way FROM osm_polygon p, osm_polygon i WHERE " \
                "i.osm_id = -59195 AND ST_Contains(i.way, p.way) AND " \
                "p.tags->'addr:street' = '{}' AND p.tags->'addr:housenumber' IN ({})"
    houses_sql = " UNION ".join([house_sql.format(*args) for args in data])
    houses_by_jes_sql = "SELECT p.jes, ST_Union(p.way) way FROM ({}) p GROUP BY p.jes".format(houses_sql)

    points_of_houses_by_jes_sql = "SELECT DISTINCT p.jes, (ST_DumpPoints(p.way)).geom way FROM ({}) p".format(houses_by_jes_sql)
    voronoi_sql = "SELECT way FROM py_voronoi('({}) p', 'p.way', 'SELECT way FROM osm_polygon WHERE osm_id = -59195') " \
                  "AS (id integer, way geometry)".format(points_of_houses_by_jes_sql.replace("'", "''"))
    result_sql = "SELECT p.jes, ST_AsGeoJSON(ST_Intersection(ST_Union(v.way), ST_Union(t.way))) FROM ({}) v, ({}) p, osm_polygon t " \
                 "WHERE ST_Contains(v.way, p.way) AND t.osm_id = -59195 " \
                 "GROUP BY p.jes".format(voronoi_sql, points_of_houses_by_jes_sql)
    cursor.execute(result_sql)
    dump(__file__, sorted(cursor.fetchall(), key=sort_numbers),
         ('publicService', 'geojson'))


if __name__ == '__main__':
    main()
