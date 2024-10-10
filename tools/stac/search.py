from typing import List, Type

import planetary_computer as pc
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
from pystac import Item
from pystac_client import Client

PC_STAC_API = "https://planetarycomputer.microsoft.com/api/stac/v1"


STAC_API = "https://earth-search.aws.element84.com/v1"
COLLECTION = "sentinel-2-l2a"


class StacSearchInput(BaseModel):
    latitude: tuple[float, float] = Field(description="Latitude of a location")
    longitude: float = Field(description="Longitude of a location")
    start: str = Field(description="Start date")
    end: str = Field(description="End date")


@tool("stac-search-tool", args_schema=StacSearchInput, return_direct=True)
def stac_search(latitude: float, longitude: float, start: str, end: str) -> List[Item]:
    """
    Search Sentinel-2 STAC items.

    Use this tool to perform a STAC scene search for a Sentinel-2 images at a
    latitude and longitude and between a start and an end date.
    """

    catalog = pystac_client.Client.open(STAC_API)

    search = catalog.search(
        collections=[COLLECTION],
        datetime=f"{start}/{end}",
        bbox=(longitude - 1e-5, latitude - 1e-5, longitude + 1e-5, latitude + 1e-5),
        max_items=100,
    )

    items = search.get_all_items()

    return [item for item in items]
