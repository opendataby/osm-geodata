# Getting geo data from OpenStreetMap

## Scripts that provide next data

- country borders
- regions borders
- regions borders where Minsk included to Misnk region
- subregions borders
- subregions borders where cities of regions subjection included to subregions
- subregions borders where cities of regions subjection and Minsk included to subregions
- cities borders
- cities regions borders
- Minsk public service voronoi division
- BOC eparchy borders
- RCC diocese borders

## Reqirements

- postgres: https://wiki.postgresql.org/wiki/Detailed_installation_guides
- postgis: http://postgis.net/install/
- osm2pgsql: http://wiki.openstreetmap.org/wiki/Osm2pgsql#Installation
- Belarus osm dump: http://gis-lab.info/projects/osm_dump/
- loaded osm data to postgis with osm2pgsql


## Database configuration

    createdb osm

    psql osm -c "CREATE EXTENSION hstore"
    psql osm -c "CREATE EXTENSION postgis"
    psql osm -c "CREATE EXTENSION postgis_topology"

    psql osm -c "CREATE LANGUAGE plpythonu"

    psql -f _first_aggregation_functions.sql osm
    psql -f _voronoi-py.sql osm

## osm2pgsql usage

    osm2pgsql -c -j -G -l -C 4000 -S /lib/share/osm2pgsql/default.style -d osm --prefix=osm BY.osm.pbf

## Additional SQL function

- FIRST aggregation function: https://wiki.postgresql.org/wiki/First/last_%28aggregate%29
- voronoi division function

## Common constants

- osm_polygon -59065 or r59065: Belarus country
- osm_polygon -59195 or r59195: Minsk city
