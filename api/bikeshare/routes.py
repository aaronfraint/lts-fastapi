from fastapi import APIRouter

from ..helpers import sql_string_to_geojson
from .schemas import Station

bikeshare_router = APIRouter(
    prefix="/bikeshare",
    tags=["philly bikeshare"],
)


@bikeshare_router.get("/indego-station/")
async def get_trips_for_single_indego_station_as_geojson(
    q: int = Station,
) -> dict:
    """
    Accept a station ID

    Return a geojson with number of trips to/from this station to all others
    """

    # print(q)
    # query = f"select * from indego_station_{q};"

    query = "select * from indego_station_3005;"

    return sql_string_to_geojson(query)
