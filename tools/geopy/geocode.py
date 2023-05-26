from typing import Type

from geopy.geocoders import Nominatim
from pydantic import BaseModel, Field
from langchain.tools import BaseTool


class GeopyGeocodeInput(BaseModel):
    """Input for GeopyGeocodeTool."""

    place: str = Field(..., description="name of a place")


class GeopyGeocodeTool(BaseTool):
    """Custom tool to perform geocoding."""

    name: str = "geocode"
    args_schema: Type[BaseModel] = GeopyGeocodeInput
    description: str = "Use this tool for geocoding."

    def _run(self, place: str) -> tuple:
        locator = Nominatim(user_agent="geocode")
        location = locator.geocode(place)
        return (location.latitude, location.longitude)

    def _arun(self, place: str):
        raise NotImplementedError
