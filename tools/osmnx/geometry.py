from typing import Dict, Type

import geopandas as gpd
import osmnx as ox
from geopandas import GeoDataFrame
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool


class PlaceWithTags(BaseModel):
    "Name of a place on the map and tags in OSM."
    place: str = Field(description="name of a place on the map.")
    tags: Dict[str, str] = Field(description="open street maps tags.")


@tool("geometry-tool", args_schema=PlaceWithTags, return_direct=True)
def geometry_tool(place: str, tags: Dict[str, str]) -> GeoDataFrame:
    """
    Tool to query geometries from Open Street Map (OSM).
    Use this tool to get geometry of different features of the place
    like building footprints, parks, lakes, hospitals, schools etc.
    Pass the name of the place & tags of OSM as args.
    """
    gdf = ox.geometries_from_place(place, tags)
    gdf = gdf[gdf["geometry"].type.isin({"Polygon", "MultiPolygon"})]
    return gdf[["name", "geometry"]].reset_index(drop=True)
