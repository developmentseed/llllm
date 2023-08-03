from typing import Type, Dict, Union

import osmnx as ox
import geopandas as gpd
from pydantic import BaseModel, Field
from langchain.tools import BaseTool


class PlaceWithTags(BaseModel):
    "Name of a place on the map and tags in OSM."

    place: str = Field(..., description="name of a place on the map.")
    tags: Dict[str, str] = Field(
        ...,
        description="open street maps tags as dict",
    )


class OSMnxGeometryTool(BaseTool):
    """Tool to query geometries from Open Street Map (OSM)."""

    name: str = "geometry"
    args_schema: Type[BaseModel] = PlaceWithTags
    description: str = """Use this tool to get geometry of different features of the place like building footprints, parks, lakes, hospitals, schools etc. \
    Pass the name of the place & tags of OSM as args.
    
    Example tags: {'building': 'yes'} or {'leisure': 'park'} or {'amenity': 'hospital'} or {'amenity': 'school'} etc.
    """
    return_direct = True

    def _run(self, place: str, tags: Dict[str, str]) -> gpd.GeoDataFrame:
        try:
            gdf = ox.geometries_from_place(place, tags)
            gdf = gdf[gdf["geometry"].type.isin({"Polygon", "MultiPolygon"})]
            gdf = gdf[["name", "geometry"]].reset_index(drop=True)
            response = ("geometry", gdf)
        except Exception as e:
            response = ("geometry", f"Error in parsing: {(place, tags)}")
        return response

    def _arun(self, place: str):
        raise NotImplementedError
