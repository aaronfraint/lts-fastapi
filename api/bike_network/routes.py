from typing import List
from fastapi import APIRouter, Query

from api.dependencies import db
from api.helpers import sql_string_to_geojson
from .models import network_mods


bike_network_router = APIRouter(
    prefix="/bike-network",
    tags=["bicycle network modifier"],
)


@bike_network_router.get("/modified-links/")
async def get_network_links_with_mods_as_geojson() -> dict:
    """
    Return all network modifications as a geojson
    """

    query = "SELECT * FROM mods_with_geom WHERE design > 0"

    return sql_string_to_geojson(query)


@bike_network_router.post("/network-update/")
async def update_list_of_network_links_with_design_value(
    q: List[int] = Query(None), design: int = Query(None)
) -> None:
    """
    Insert row(s) for each link_id into the bikenetwork_mods table
    """
    await db.execute_many(
        query=network_mods.insert(),
        values=[{"link_id": link_id, "design": design} for link_id in q],
    )

    return None
