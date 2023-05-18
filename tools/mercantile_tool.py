import mercantile
from langchain.tools import BaseTool


class MercantileTool(BaseTool):
    """Custom tool to perform mercantile operations.

    This tool is used to get the xyz tiles given a lng,lat coordinate.
    """

    name = "mercantile"
    description = "Use this tool to get the xyz tiles given a lng,lat coordinate. \
    To use this tool you need to provide lng,lat,zoom level separated by comma. \
    Eg: `-105.24, 22.50, 5` is the input to get a tile for this (lng=-105.24, lat=22.50) at zoom level 5"

    def _run(self, query):
        lng, lat, zoom = map(float, query.split(","))
        return mercantile.tile(lng, lat, zoom)

    def _arun(self, query):
        raise NotImplementedError(
            "Mercantile tool doesn't have an async implementation."
        )
