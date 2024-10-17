from typing import Tuple

from geopy.geocoders import Nominatim
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class GeopyGeocodeInput(BaseModel):
    """Input for GeopyGeocodeTool."""

    place: str = Field(description="name of a place")


@tool("geocode-tool", args_schema=GeopyGeocodeInput, return_direct=True)
def geocode_tool(place: str) -> Tuple[float, float]:
    """
    Custom tool to perform geocoding.

    Use this tool for geocoding an address of a place.
    """
    return 30.1, 40.1
    locator = Nominatim(user_agent="geocode")
    location = locator.geocode(place)
    return location.latitude, location.longitude
