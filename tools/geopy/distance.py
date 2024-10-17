from typing import Union

from geopy.distance import distance
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class GeopyDistanceInput(BaseModel):
    """Input for GeopyDistanceTool."""

    lat1: float = Field(description="Latitude of a first location")
    lon1: float = Field(description="Longitude of a first location")
    lat2: float = Field(description="Latitude of a second location")
    lon2: float = Field(description="Longitude of a second location")


@tool("distance-tool", args_schema=GeopyDistanceInput, return_direct=False)
def distance_tool(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Tool to calculate distance in kilometers between two points.
    """
    return distance((lat1, lon1), (lat2, lon2)).km
