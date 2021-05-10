from fastapi import APIRouter

# from src.dependencies import DATABASE_URL
# import geopandas
# import json

# import asyncpg


from .db import postgis_query_to_geojson

bikeshare_router = APIRouter(
    prefix="/indego",
    tags=["philly bikeshare"],
)


@bikeshare_router.get("/all/")
async def get_all_indego_stations() -> dict:
    """
    Serve a geojson of all station points
    """
    query = """
        select
            id as station_id,
            name,
            addressstreet,
            geom as geometry
        from
            station_shapes
    """
    return await postgis_query_to_geojson(
        query, ["station_id", "name", "addressstreet", "geometry"]
    )


@bikeshare_router.get("/trip-points/")
async def get_trips_for_single_indego_station_as_geojson(
    q: int,
) -> dict:
    """
    Accept a station ID

    Return a geojson with number of trips to/from this station to all others
    """

    query = f"""
    select
        station_id,
        origins::float / 75 as origins,
        destinations::float / 75 as destinations,
        (origins::float + destinations::float) / 75 as totalTrips,
        geom as geometry from station_{int(q)};
    """
    return await postgis_query_to_geojson(
        query, ["station_id", "origins", "destinations", "totalTrips", "geometry"]
    )


@bikeshare_router.get("/trip-spider/")
async def get_spider_diagram_for_single_indego_station_as_geojson(
    q: int,
) -> dict:
    """
    Accept a station ID

    Return a geojson with number of trips to/from this station to all others
    """

    query = f"""
        with raw as (
            select
                station_id,
                origins::float / 75 as origins,
                destinations::float / 75 as destinations,
                (origins::float + destinations::float) / 75 as totalTrips,
                st_makeline((select geom from station_shapes where id = {int(q)}), geom) as geom 
            from station_{int(q)}
        )
        select station_id, origins, destinations , totalTrips,
        st_setsrid(ST_CurveToLine('CIRCULARSTRING(' || st_x(st_startpoint(geom)) || ' ' || st_y(st_startpoint(geom)) || ', ' || st_x(st_centroid(ST_OffsetCurve(geom, st_length(geom)/10, 'quad_segs=4 join=bevel'))) || ' ' || st_y(st_centroid(ST_OffsetCurve(geom, st_length(geom)/10, 'quad_segs=4 join=bevel'))) || ', ' || st_x(st_endpoint(geom)) || ' ' ||  st_y(st_endpoint(geom)) || ')'), 4326) AS geometry
        from raw
        where station_id != {int(q)}

    """
    return await postgis_query_to_geojson(
        query, ["station_id", "origins", "destinations", "totalTrips", "geometry"]
    )
