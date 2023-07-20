import os

import rasterio as rio
import folium
import streamlit as st
from streamlit_folium import folium_static

from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool, DuckDuckGoSearchRun
from langchain.callbacks import (
    StreamlitCallbackHandler,
    get_openai_callback,
)

from tools.mercantile_tool import MercantileTool
from tools.geopy.geocode import GeopyGeocodeTool
from tools.geopy.distance import GeopyDistanceTool
from tools.osmnx.geometry import OSMnxGeometryTool
from tools.osmnx.network import OSMnxNetworkTool
from tools.stac.search import STACSearchTool
from agents.l4m_agent import base_agent


@st.cache_resource(ttl="1h")
def get_agent(agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION):
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model_name="gpt-3.5-turbo-0613",
    )
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
    search_tool = STACSearchTool()

    tools = [
        duckduckgo_tool,
        geocode_tool,
        distance_tool,
        mercantile_tool,
        geometry_tool,
        network_tool,
        search_tool,
    ]

    agent = base_agent(llm, tools, agent_type=agent_type)
    return agent


def run_query(agent, query):
    st_callback = StreamlitCallbackHandler(st.container())
    response = agent.run(query, callbacks=[st_callback])
    return response


def plot_raster(items):
    st.subheader("Preview of the first item sorted by cloud cover")
    selected_item = min(items, key=lambda item: item.properties["eo:cloud_cover"])
    href = selected_item.assets["rendered_preview"].href
    # arr = rio.open(href).read()

    # m = folium.Map(location=[28.6, 77.7], zoom_start=6)

    # img = folium.raster_layers.ImageOverlay(
    #     name="Sentinel 2",
    #     image=arr.transpose(1, 2, 0),
    #     bounds=selected_item.bbox,
    #     opacity=0.9,
    #     interactive=True,
    #     cross_origin=False,
    #     zindex=1,
    # )

    # img.add_to(m)
    # folium.LayerControl().add_to(m)

    # folium_static(m)
    st.image(href)


def plot_vector(df):
    st.subheader("Add the geometry to the Map")
    center = df.centroid.iloc[0]
    m = folium.Map(location=[center.y, center.x], zoom_start=12)
    folium.GeoJson(df).add_to(m)
    folium_static(m)


st.subheader("🤖 I am Geo LLM Agent!")

agent = get_agent()

if "msgs" not in st.session_state:
    st.session_state.msgs = []

for msg in st.session_state.msgs:
    with st.chat_message(name=msg["role"], avatar=msg["avatar"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask me anything about the flat world..."):
    with st.chat_message(name="user", avatar="🧑‍💻"):
        st.markdown(prompt)

    st.session_state.msgs.append({"role": "user", "avatar": "🧑‍💻", "content": prompt})

    with get_openai_callback() as cb:
        response = run_query(agent, prompt)

        # Log OpenAI stats
        # print(f"Model name: {response.llm_output.get('model_name', '')}")
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")

    with st.chat_message(name="assistant", avatar="🤖"):
        if type(response) == str:
            content = response
            st.markdown(response)
        else:
            tool, result = response

            match tool:
                case "stac-search":
                    content = f"Found {len(result)} items from the catalog."
                    st.markdown(content)
                    if len(result) > 0:
                        plot_raster(result)
                case "geometry":
                    content = f"Found {len(result)} geometries."
                    gdf = result
                    st.markdown(content)
                    plot_vector(gdf)
                case "network":
                    content = f"Found {len(result)} network geometries."
                    ndf = result
                    st.markdown(content)
                    plot_vector(ndf)
                case _:
                    content = response
                    st.markdown(content)

    st.session_state.msgs.append(
        {"role": "assistant", "avatar": "🤖", "content": content}
    )
