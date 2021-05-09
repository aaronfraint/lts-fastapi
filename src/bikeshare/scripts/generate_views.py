import os
import asyncio
import databases
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
DATABASE_URL = os.environ.get("DATABASE_URL")


db = databases.Database(DATABASE_URL)

query_template = """
    with origins as (
    select
        start_station as station_id,
        count(*) as origins
        from trips
        where end_station = STATION_ID
        group by start_station
    ),
    destinations as (
    select
        end_station as station_id,
        count(*) as destinations
        from trips
        where start_station = STATION_ID
        group by end_station
    ),
    numeric_data as (
        select o.station_id, o.origins, d.destinations
        from origins o
        full outer join destinations d on o.station_id = d.station_id
    )
    select ss.geom, ss.name, nd.* from station_shapes ss
    inner join numeric_data nd on ss.id = nd.station_id
"""


async def main():
    await db.connect()

    ids = await db.fetch_all("SELECT DISTINCT id FROM station_shapes ORDER BY id asc")

    for id in ids:
        station_id = id["id"]

        # await db.execute(query=f"DROP VIEW IF EXISTS station_detail_{station_id}")

        query = f"""
            CREATE TABLE station_{station_id} AS
        """ + query_template.replace(
            "STATION_ID", str(station_id)
        )

        # print(query)

        await db.execute(query=query)

        print("Completed", station_id)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
