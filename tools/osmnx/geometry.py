from typing import Type, Dict

import osmnx as ox
import geopandas as gpd
from pydantic import BaseModel, Field
from langchain.tools import BaseTool


class PlaceWithTags(BaseModel):
    "Name of a place and tags in OSM."

    place: str = Field(..., description="name of a place")
    tags: Dict[str, str] = Field(..., description="open street maps tags")


class OSMnxGeometryTool(BaseTool):
    """Custom tool to query geometries from OSM."""

    name: str = "geometry"
    args_schema: Type[BaseModel] = PlaceWithTags
    description: str = "Use this tool to get geometry of different features of a place like building footprints, parks, lakes, hospitals, schools etc. \
    Pass the name of the place & relevant tags of Open Street Map as args."
    return_direct = True

    def _run(self, place: str, tags: Dict[str, str]) -> gpd.GeoDataFrame:
        gdf = ox.geometries_from_place(place, tags)
        gdf = gdf[gdf["geometry"].type.isin({"Polygon", "MultiPolygon"})]
        gdf = gdf[["name", "geometry"]].reset_index(drop=True).head(100)
        return gdf

    def _arun(self, place: str):
        raise NotImplementedError
