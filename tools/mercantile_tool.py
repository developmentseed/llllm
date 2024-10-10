from typing import List

import mercantile
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class MercantileToolInput(BaseModel):
    latitude: float = Field(description="Latitude of a location")
    longitude: float = Field(description="Longitude of a location")
    zoom: str = Field(description="Zoom level for mercantile")


@tool("mercantile-tool", args_schema=MercantileToolInput, return_direct=True)
def mercantile_tool(latitude: float, longitude: float, zoom: int) -> mercantile.Tile:
    """
    Tool to perform mercantile operations.
    Use this tool to get the xyz tiles for a place. To use this tool you need to provide
    lng,lat,zoom level of the place separated by comma.
    """
    lng, lat, zoom = map(float, query.split(","))
    return mercantile.tile(lng, lat, zoom)
