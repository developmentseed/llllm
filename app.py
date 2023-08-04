import os
from dotenv import load_dotenv

import rasterio as rio
import folium
import streamlit as st
from streamlit_folium import folium_static

import langchain
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool, DuckDuckGoSearchRun
from langchain.callbacks import (
    StreamlitCallbackHandler,
    AimCallbackHandler,
    get_openai_callback,
)

from tools.mercantile_tool import MercantileTool
from tools.geopy.geocode import GeopyGeocodeTool

# from tools.geopy.distance import GeopyDistanceTool
from tools.osmnx.geometry import OSMnxGeometryTool
from tools.osmnx.network import OSMnxNetworkTool
from tools.stac.search import STACSearchTool
from agents.l4m_agent import base_agent, openai_function_agent

# # DEBUG
langchain.debug = True
# langchain.verbose = True

# Load environment variables
load_dotenv()


@st.cache_resource(ttl="1h")
def get_agent(openai_api_key):
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=openai_api_key,
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
    # distance_tool = GeopyDistanceTool()
    mercantile_tool = MercantileTool()
    geometry_tool = OSMnxGeometryTool()
    network_tool = OSMnxNetworkTool()
    search_tool = STACSearchTool()

    tools = [
        duckduckgo_tool,
        geocode_tool,
        # distance_tool,
        mercantile_tool,
        geometry_tool,
        network_tool,
        search_tool,
    ]

    agent = openai_function_agent(llm, tools)
    # agent = base_agent(llm, tools)
    return agent


def plot_raster(items):
    st.subheader("Preview of the first item sorted by cloud cover")
    selected_item = min(items, key=lambda item: item.properties["eo:cloud_cover"])
    href = selected_item.assets["rendered_preview"].href
    arr = rio.open(href).read()

    lon_min, lat_min, lon_max, lat_max = selected_item.bbox
    bbox = [[lat_min, lon_min], [lat_max, lon_max]]
    m = folium.Map(
        location=[(lat_min + lat_max) / 2, (lon_min + lon_max) / 2], zoom_start=8
    )
    img = folium.raster_layers.ImageOverlay(
        name="Sentinel 2",
        image=arr.transpose(1, 2, 0),
        bounds=bbox,
        opacity=0.9,
        interactive=True,
        cross_origin=False,
        zindex=1,
    )

    img.add_to(m)
    folium.LayerControl().add_to(m)

    folium_static(m)
    # st.image(href)


def plot_vector(df):
    st.subheader("Add the geometry to the Map")
    center = df.centroid.iloc[0]
    m = folium.Map(location=[center.y, center.x], zoom_start=12)
    folium.GeoJson(df).add_to(m)
    folium_static(m)


st.set_page_config(page_title="LLLLM", page_icon="🤖", layout="wide")
st.markdown("🤖 I am Geo LLM Agent!")
st.caption(
    "I have access to tools like :blue[STAC Search, OSM API, Geocode & Mercantile]. Feel free to ask me questions like - :orange[_lat,lng_ of a place, _parks/hospitals_ in a city, _walkable streets_ in a city or _satellite image_ on a particular date.]"
)


if "msgs" not in st.session_state:
    st.session_state.msgs = []

if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

if "prompt_tokens" not in st.session_state:
    st.session_state.prompt_tokens = 0

if "completion_tokens" not in st.session_state:
    st.session_state.completion_tokens = 0

if "total_cost" not in st.session_state:
    st.session_state.total_cost = 0

with st.sidebar:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        openai_api_key = st.text_input("OpenAI API Key", type="password")
        st.info(
            "You can find your API key [here](https://platform.openai.com/account/api-keys)"
        )

    st.subheader("OpenAI Usage this Session")
    total_tokens = st.empty()
    prompt_tokens = st.empty()
    completion_tokens = st.empty()
    total_cost = st.empty()

    total_tokens.write(f"Total Tokens: {st.session_state.total_tokens:,.0f}")
    prompt_tokens.write(f"Prompt Tokens: {st.session_state.prompt_tokens:,.0f}")
    completion_tokens.write(
        f"Completion Tokens: {st.session_state.completion_tokens:,.0f}"
    )
    total_cost.write(f"Total Cost (USD): ${st.session_state.total_cost:,.4f}")


for msg in st.session_state.msgs:
    with st.chat_message(name=msg["role"], avatar=msg["avatar"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask me anything about the flat world..."):
    with st.chat_message(name="user", avatar="🧑‍💻"):
        st.markdown(prompt)

    st.session_state.msgs.append({"role": "user", "avatar": "🧑‍💻", "content": prompt})

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    aim_callback = AimCallbackHandler(
        repo=os.getenv("AIM_LOGS", "."),
        experiment_name="LLLLLM: OpenAI function agent v0.3",
    )

    agent = get_agent(openai_api_key)

    with get_openai_callback() as cb:
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(
            prompt,
            callbacks=[st_callback, aim_callback],
        )

        aim_callback.flush_tracker(langchain_asset=agent, reset=False, finish=True)

        # Log OpenAI stats
        # print(f"Model name: {response.llm_output.get('model_name', '')}")
        st.session_state.total_tokens += cb.total_tokens
        st.session_state.prompt_tokens += cb.prompt_tokens
        st.session_state.completion_tokens += cb.completion_tokens
        st.session_state.total_cost += cb.total_cost

        total_tokens.write(f"Total Tokens: {st.session_state.total_tokens:,.0f}")
        prompt_tokens.write(f"Prompt Tokens: {st.session_state.prompt_tokens:,.0f}")
        completion_tokens.write(
            f"Completion Tokens: {st.session_state.completion_tokens:,.0f}"
        )
        total_cost.write(f"Total Cost (USD): ${st.session_state.total_cost:,.4f}")

    with st.chat_message(name="assistant", avatar="🤖"):
        print(type(response))
        print(response)
        if type(response) == str:
            content = response
            st.markdown(response)
        else:
            tool, result = response

            match tool:
                case "stac-search":
                    if len(result) == 0:
                        content = "No items found."
                    else:
                        content = f"Found {len(result)} items from the catalog."
                        plot_raster(result)
                    st.markdown(content)
                case "geometry":
                    if type(result) is str or len(result) == 0:
                        content = "No geometries found."
                    else:
                        content = f"Found {len(result)} geometries."
                        gdf = result
                        plot_vector(gdf)
                    st.markdown(content)
                case "network":
                    if type(result) is str or len(result) == 0:
                        content = "No network geometries found."
                    else:
                        content = f"Found {len(result)} network geometries."
                        ndf = result
                        plot_vector(ndf)
                    st.markdown(content)
                case _:
                    content = response
                    st.markdown(content)

    st.session_state.msgs.append(
        {"role": "assistant", "avatar": "🤖", "content": content}
    )
