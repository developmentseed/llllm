import geopandas as gpd
import osmnx as ox
from geopandas import GeoDataFrame
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
from osmnx import utils_graph


class PlaceWithNetworktype(BaseModel):
    "Name of a place on the map"
    place: str = Field(description="name of a place on the map")
    network_type: str = Field(
        description="network type: one of walk, bike, drive or all"
    )


@tool("network-tool", args_schema=PlaceWithNetworktype, return_direct=True)
def network_tool(place: str, network_type: str) -> GeoDataFrame:
    """
    Custom tool to query road networks from OSM.
    Use this tool to get road network of a place.
    Pass the name of the place & type of road network i.e walk, bike, drive or all
    """
    G = ox.graph_from_place(place, network_type=network_type, simplify=True)
    network = utils_graph.graph_to_gdfs(G, nodes=False)
    return network[["name", "geometry"]].reset_index(drop=True)
