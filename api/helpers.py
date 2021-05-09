import json
import sqlalchemy
import geopandas as gpd

from .dependencies import DATABASE_URL


def sql_string_to_geojson(query: str, uri: str = DATABASE_URL) -> dict:
    """
    - Query the database via `geopandas` / `sqlalchemy`
    - Get the result as a geodataframe

    Args:
        query (str): SQL query
        uri (str): database connection string


    Returns:
        geodata as dictionary
    """
    engine = sqlalchemy.create_engine(uri)

    gdf = gpd.read_postgis(query, engine)

    engine.dispose()

    return json.loads(gdf.to_json())
