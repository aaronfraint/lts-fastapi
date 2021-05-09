from fastapi import APIRouter
import shapely
from api.dependencies import db, DATABASE_URL
import geopandas
import json

import asyncpg


bikeshare_router = APIRouter(
    prefix="/bikeshare",
    tags=["philly bikeshare"],
)


def encode_geometry(geometry):
    if not hasattr(geometry, "__geo_interface__"):
        raise TypeError(
            "{g} does not conform to " "the geo interface".format(g=geometry)
        )
    shape = shapely.geometry.asShape(geometry)
    return shapely.wkb.dumps(shape)


def decode_geometry(wkb):
    return shapely.wkb.loads(wkb)


@bikeshare_router.get("/all-indego-stations/")
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
    conn = await asyncpg.connect(DATABASE_URL)

    try:

        await conn.set_type_codec(
            "geometry",  # also works for 'geography'
            encoder=encode_geometry,
            decoder=decode_geometry,
            format="binary",
        )

        res = await conn.fetch(query)

    finally:
        await conn.close()

    gdf = geopandas.GeoDataFrame.from_records(
        res, columns=["station_id", "name", "addressstreet", "geometry"]
    )
    return json.loads(gdf.to_json())


@bikeshare_router.get("/indego-station/")
async def get_trips_for_single_indego_station_as_geojson(
    q: int,
) -> dict:
    """
    Accept a station ID

    Return a geojson with number of trips to/from this station to all others
    """

    # print(q)
    # query = f"select * from indego_station_{q};"

    # query = od_query.replace("in ID_LIST", f"= {int(q)}")

    # query = f"select * from indego_station_{int(q)};"

    # return sql_string_to_geojson(query)

    # return await db.fetch_all(query)

    query = f"""
    select
        station_id,
        origins::float / 75 as origins,
        destinations::float / 75 as destinations,
        (origins::float + destinations::float) / 75 as totalTrips,
        geom as geometry from station_{int(q)};
    """

    conn = await asyncpg.connect(DATABASE_URL)

    try:

        await conn.set_type_codec(
            "geometry",  # also works for 'geography'
            encoder=encode_geometry,
            decoder=decode_geometry,
            format="binary",
        )

        res = await conn.fetch(query)

        # pprint(res)

    finally:
        await conn.close()

    gdf = geopandas.GeoDataFrame.from_records(
        res, columns=["station_id", "origins", "destinations", "totalTrips", "geometry"]
    )  # .set_geometry("geom", inplace=True)
    # print(gdf.columns)  # .set_geometry("geom", inplace=True)
    return json.loads(gdf.to_json())

    # return await db.fetch_all(query)


@bikeshare_router.get("/indego-station-spider/")
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

    conn = await asyncpg.connect(DATABASE_URL)

    try:

        await conn.set_type_codec(
            "geometry",  # also works for 'geography'
            encoder=encode_geometry,
            decoder=decode_geometry,
            format="binary",
        )

        res = await conn.fetch(query)

        # pprint(res)

    finally:
        await conn.close()

    gdf = geopandas.GeoDataFrame.from_records(
        res, columns=["station_id", "origins", "destinations", "totalTrips", "geometry"]
    )
    return json.loads(gdf.to_json())


# TODO: add timeseries output for bar graph
