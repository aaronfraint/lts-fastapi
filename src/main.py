from typing import List

# import databases
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# from config import DATABASE_URL

app = FastAPI()
# database = databases.Database(DATABASE_URL)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


@app.get("/")
def homepage():
    """"""
    return {"message": "hello world"}


# @app.get("/island-merge/")
# async def merge_islands(q: List[int] = Query(None)):
#     """
#     Accept a list of link IDs.

#     Return the number of islands that would merge, and their ID values.
#     """

#     if not q:
#         return {"message": "Please provide at least one link ID"}

#     if len(q) == 1:
#         id_list = f"({q[0]})"
#     else:
#         id_list = tuple(q)

#     # query = f"""
#     #     select strong::int
#     #     from islands i
#     #     where st_intersects(
#     #         geom, (
#     #         select st_collect(geom) from network_links nl where gid in {id_list}
#     #         )
#     #     )
#     # """

#     query = f"""
#         select island_id::int
#         from links_and_islands
#         where link_id in {id_list}
#     """

#     query_result = await database.fetch_all(query)

#     island_id_list = [x["island_id"] for x in query_result]

#     return {"id_list": island_id_list}