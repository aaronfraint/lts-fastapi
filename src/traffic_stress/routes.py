from typing import List
from fastapi import APIRouter, Query

from ..dependencies import db

traffic_stress_router = APIRouter(
    prefix="/traffic-stress",
    tags=["traffic stress"],
)


@traffic_stress_router.get("/island-merge/")
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

    query_result = await db.fetch_all(query)

    island_id_list = [x["island_id"] for x in query_result]

    return {"id_list": island_id_list}
