import streamlit as st
from langchain_core.messages import HumanMessage

from graphs.l4m_graph import graph

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    config = {"configurable": {"thread_id": "1"}}
    for chunk in graph.stream(
        {"messages": [HumanMessage(content=prompt)]}, config, stream_mode="updates"
    ):
        # for chunk in graph.invoke(
        #     {"messages": [HumanMessage(content=prompt)]}, config, stream_mode="updates"
        # ):
        #     st.markdown(chunk)

        node = "assistant" if "assistant" in chunk else "tools"
        with st.chat_message(node):
            for msg in chunk[node]["messages"]:
                st.markdown(msg.content)
