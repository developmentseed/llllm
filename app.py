import os

import folium
import streamlit as st
from streamlit_folium import folium_static

from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool, DuckDuckGoSearchRun

from tools.mercantile_tool import MercantileTool
from tools.geopy.geocode import GeopyGeocodeTool
from tools.geopy.distance import GeopyDistanceTool
from tools.osmnx.geometry import OSMnxGeometryTool
from tools.osmnx.network import OSMnxNetworkTool
from agents.l4m_agent import base_agent


def get_llm():
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model_name="gpt-3.5-turbo",
    )
    return llm


def get_agent(llm, agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION):
    # define a set of tools the agent has access to for queries
    duckduckgo_tool = Tool(
        name="DuckDuckGo",
        description="Use this tool to answer questions about current events and places. \
        Please ask targeted questions.",
        func=DuckDuckGoSearchRun().run,
    )
    geocode_tool = GeopyGeocodeTool()
    distance_tool = GeopyDistanceTool()
    mercantile_tool = MercantileTool()
    geometry_tool = OSMnxGeometryTool()
    network_tool = OSMnxNetworkTool()

    tools = [
        duckduckgo_tool,
        geocode_tool,
        distance_tool,
        mercantile_tool,
        geometry_tool,
        network_tool,
    ]

    agent = base_agent(llm, tools, agent_type=agent_type)
    return agent


def run_query(agent, query):
    response = agent(query)
    return response


def show_on_map(response):
    gdf = response["output"]
    center = gdf.centroid.iloc[0]
    folium_map = folium.Map(location=[center.y, center.x], zoom_start=12)
    folium.GeoJson(gdf).add_to(folium_map)
    folium_static(folium_map)


st.title("LLLLM")

query = st.text_input(
    "Ask me stuff about the flat world: ",
    placeholder="Find all the hospitals in Bangalore",
)

if st.button("Submit", key="submit", type="primary"):
    llm = get_llm()
    agent = get_agent(llm)
    response = run_query(agent, query)
    show_on_map(response)
    st.success("Great, you have the results plotted on the map.")
