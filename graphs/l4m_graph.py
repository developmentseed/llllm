import langchain
from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from tools.geopy.distance import distance_tool
from tools.geopy.geocode import geocode_tool
from tools.mercantile_tool import mercantile_tool
from tools.osmnx.geometry import geometry_tool
from tools.osmnx.network import network_tool
from tools.stac.search import stac_search

# from tools.duck_tool import duckduckgo_tool

# DEBUG
langchain.debug = True

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)

tools = [
    # duckduckgo_tool,
    geocode_tool,
    distance_tool,
    mercantile_tool,
    geometry_tool,
    network_tool,
    stac_search,
]

# For this ipynb we set parallel tool calling to false as math generally is done sequentially, and this time we have 3 tools that can do math
# the OpenAI model specifically defaults to parallel tool calling for efficiency, see https://python.langchain.com/docs/how_to/tool_calling_parallel/
# play around with it and see how the model behaves with math equations!
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)


# System message
sys_msg = SystemMessage(
    content="You are a helpful assistant tasked with answering questions on a set of geographic inputs."
    # "You are a helpful assistant tasked with performing arithmetic on a set of inputs. "
    "do not use tools unless the message does not contain geographic inputs"
    # "do NOT use tools unless strictly necessary to answer the question"
    # " Do NOT answer the question, just reformulate it if needed and otherwise return it as is.."
)


# Node
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


# Graph
builder = StateGraph(MessagesState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")

graph = builder.compile()
