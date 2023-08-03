from typing import Type

from pystac_client import Client
import planetary_computer as pc
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

PC_STAC_API = "https://planetarycomputer.microsoft.com/api/stac/v1"


class PlaceWithDatetimeAndBBox(BaseModel):
    "Name of a place and date."

    bbox: str = Field(..., description="bbox of the place")
    datetime: str = Field(..., description="only date for the stac catalog search")


class STACSearchTool(BaseTool):
    """Tool to search for STAC items in a catalog."""

    name: str = "stac-search"
    args_schema: Type[BaseModel] = PlaceWithDatetimeAndBBox
    description: str = "Use this tool to search for STAC items in a catalog. \
    Pass the bbox of the place & date as args."
    return_direct = True

    def _run(self, bbox: str, datetime: str):
        catalog = Client.open(PC_STAC_API, modifier=pc.sign_inplace)

        search = catalog.search(
            collections=["sentinel-2-l2a"],
            bbox=bbox,
            datetime=datetime,
            max_items=10,
        )
        items = search.get_all_items()

        return ("stac-search", items)

    def _arun(self, bbox: str, datetime: str):
        raise NotImplementedError
