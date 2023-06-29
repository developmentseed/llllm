from typing import Type, Dict

import osmnx as ox
from osmnx import utils_graph
import geopandas as gpd
from pydantic import BaseModel, Field
from langchain.tools import BaseTool


class PlaceWithNetworktype(BaseModel):
    "Name of a place on the map"
    place: str = Field(..., description="name of a place on the map")
    network_type: str = Field(
        ..., description="network type: one of walk, bike, drive or all"
    )


class OSMnxNetworkTool(BaseTool):
    """Custom tool to query road networks from OSM."""

    name: str = "network"
    args_schema: Type[BaseModel] = PlaceWithNetworktype
    description: str = "Use this tool to get road network of a place. \
    Pass the name of the place & type of road network i.e walk, bike, drive or all."
    return_direct = True

    def _run(self, place: str, network_type: str) -> gpd.GeoDataFrame:
        G = ox.graph_from_place(place, network_type=network_type, simplify=True)
        network = utils_graph.graph_to_gdfs(G, nodes=False)
        network = network[["name", "geometry"]].reset_index(drop=True).head(100)
        return ("network", network)

    def _arun(self, place: str):
        raise NotImplementedError
