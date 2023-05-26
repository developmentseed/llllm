from typing import Type

from geopy.distance import distance
from pydantic import BaseModel, Field
from langchain.tools import BaseTool


class GeopyDistanceInput(BaseModel):
    """Input for GeopyDistanceTool."""

    point_1: tuple[float, float] = Field(..., description="lat,lng of a place")
    point_2: tuple[float, float] = Field(..., description="lat,lng of a place")


class GeopyDistanceTool(BaseTool):
    """Custom tool to calculate geodesic distance between two points."""

    name: str = "distance"
    args_schema: Type[BaseModel] = GeopyDistanceInput
    description: str = "Use this tool to compute distance between two points available in lat,lng format."

    def _run(self, point_1: tuple[int, int], point_2: tuple[int, int]) -> float:
        return distance(point_1, point_2).km

    def _arun(self, place: str):
        raise NotImplementedError
