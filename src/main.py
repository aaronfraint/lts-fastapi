import json
from typing import List
import os
import databases
import sqlalchemy
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import geopandas as gpd

load_dotenv(find_dotenv())
DATABASE_URL = os.environ.get("DATABASE_URL")

app = FastAPI()
database = databases.Database(DATABASE_URL)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metadata = sqlalchemy.MetaData()

network_mods = sqlalchemy.Table(
    "bikenetwork_mods",
    metadata,
    sqlalchemy.Column("link_id", sqlalchemy.Integer),
    sqlalchemy.Column("design", sqlalchemy.Integer),
)


@app.on_event("startup")
async def startup():
    await database.connect()

    await database.execute(
        query="""
        create table if not exists bikenetwork_mods (
            link_id int,
            design int
        );
    """
    )

    await database.execute(
        query="""
        create or replace view mods_with_geom as (
            select mods.*, st_transform(nl.geom, 4326) as geom from bikenetwork_mods mods 
            left join network_links nl on mods.link_id = nl.gid
        )
        """
    )


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
def homepage():
    """"""
    return {"message": "hello world"}


@app.get("/modified-links/")
async def get_links_with_mods():
    """
    Return all network modifications as a geojson
    """
    engine = sqlalchemy.create_engine(DATABASE_URL)

    sql = "SELECT * FROM mods_with_geom WHERE design > 0"

    gdf = gpd.read_postgis(sql, engine)

    engine.dispose()

    return json.loads(gdf.to_json())


@app.post("/network-update/")
async def update_network(q: List[int] = Query(None), design: int = Query(None)):
    """
    Insert row(s) for each link_id into the bikenetwork_mods table
    """
    await database.execute_many(
        query=network_mods.insert(),
        values=[{"link_id": link_id, "design": design} for link_id in q],
    )


@app.get("/island-merge/")
async def merge_islands(q: List[int] = Query(None)):
    """
    Accept a list of link IDs.

    Return the number of islands that would merge, and their ID values.
    """

    if not q:
        return {"message": "Please provide at least one link ID"}

    if len(q) == 1:
        id_list = f"({q[0]})"
    else:
        id_list = tuple(q)

    query = f"""
        select island_id::int
        from links_and_islands
        where link_id in {id_list}
    """

    query_result = await database.fetch_all(query)

    island_id_list = [x["island_id"] for x in query_result]

    return {"id_list": island_id_list}