import mercantile
from langchain.tools import BaseTool


class MercantileTool(BaseTool):
    """Tool to perform mercantile operations."""

    name = "mercantile"
    description = "use this tool to get the xyz tiles for a place. \
    To use this tool you need to provide lng,lat,zoom level of the place separated by comma."

    def _run(self, query):
        lng, lat, zoom = map(float, query.split(","))
        return ("mercantile", mercantile.tile(lng, lat, zoom))

    def _arun(self, query):
        raise NotImplementedError(
            "Mercantile tool doesn't have an async implementation."
        )
