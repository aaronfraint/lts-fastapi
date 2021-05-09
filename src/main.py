from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import db
from .bikeshare.routes import bikeshare_router

# from .bike_network.routes import bike_network_router
# from .traffic_stress.routes import traffic_stress_router
# from .bike_network.queries import startup_commands

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bikeshare_router)
# app.include_router(bike_network_router)
# app.include_router(traffic_stress_router)


@app.on_event("startup")
async def startup():
    await db.connect()

    # for sql_cmd in startup_commands:

    #     await db.execute(query=sql_cmd)


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
