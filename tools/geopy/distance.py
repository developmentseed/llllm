from geopy.distance import distance
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class GeopyDistanceInput(BaseModel):
    """Input for GeopyDistanceTool."""

    point_1: tuple[float, float] = Field(description="lat,lng of a place")
    point_2: tuple[float, float] = Field(description="lat,lng of a place")


@tool("distance-tool", args_schema=GeopyDistanceInput, return_direct=False)
def distance_tool(point_1: tuple[float, float], point_2: tuple[float, float]) -> float:
    """
    Custom tool to calculate geodesic distance between two points.
    """
    return distance(point_1, point_2).km
