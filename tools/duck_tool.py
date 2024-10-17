from langchain.tools import DuckDuckGoSearchRun, Tool

duckduckgo_tool = Tool(
    name="DuckDuckGo",
    description="Use this tool to answer questions about current events and places. \
    Please ask targeted questions.",
    func=DuckDuckGoSearchRun().run,
)
