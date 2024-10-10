from typing import Tuple

from geopy.geocoders import Nominatim
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool


class GeopyGeocodeInput(BaseModel):
    """Input for GeopyGeocodeTool."""

    place: str = Field(description="name of a place")


@tool("geocode-tool", args_schema=GeopyGeocodeInput, return_direct=True)
def geocode_tool(place: str) -> Tuple[float, float]:
    """
    Custom tool to perform geocoding.

    Use this tool for geocoding an address of a place.
    """
    locator = Nominatim(user_agent="geocode")
    location = locator.geocode(place)
    if location is None:
        return ("geocode", "Not a recognised address in Nomatim.")
    return location.latitude, location.longitude
