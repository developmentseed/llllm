import os

import rasterio as rio
import folium
import streamlit as st
from streamlit_folium import folium_static

import langchain
from langchain import hub
from langchain.agents import AgentType
from langchain_ollama import ChatOllama
from langchain.tools import Tool, DuckDuckGoSearchRun
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents import AgentExecutor, create_react_agent, load_tools


from tools.mercantile_tool import mercantile_tool
from tools.geopy.geocode import geocode_tool
from tools.geopy.distance import distance_tool
from tools.osmnx.geometry import geometry_tool
from tools.osmnx.network import network_tool
from tools.stac.search import stac_search
from agents.l4m_agent import base_agent

# DEBUG
langchain.debug = True

duckduckgo_tool = Tool(
    name="DuckDuckGo",
    description="Use this tool to answer questions about current events and places. \
    Please ask targeted questions.",
    func=DuckDuckGoSearchRun().run,
)

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
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent_executor.invoke(
            {"input": prompt}, {"callbacks": [st_callback]}
        )
        st.write(response["output"])
