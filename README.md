# llllm

A suite of tools to perform geospatial operations using Large Language Models.

LLLLM stands for Lat-Lng-Large-Language-Model, you can call it as "el el el el emm" or "L4M".

## Setup

Create the llllm-env - `mamba env create -f environment.yaml`

## Getting Started

### Adding a new tool

Tools are ways the agent can use to interact with the outside world. You can find more information on how LLMs use tools to solve new tasks at scale in this paper: [Toolformer](https://arxiv.org/pdf/2302.04761.pdf)

Langchain comes bundled with a set of tools like Google Search, Wikipedia, Python REPL, Shell, Wolfram Alpha & several others - find the list of pre-built tools [here](https://python.langchain.com/en/latest/modules/agents/tools.html#)

Creating a new tool is simple in Langchain. You can create a custom tool by:
- using the `Tool` dataclass or
- inhering from the `BaseTool` class

Both these methods need to provide:
- name: unique & referred to by LLM while executing the chains
- description: detailed description of when & how the LLM should use this tool
- args_schema: arguments to the tool

Barebones of how to define a custom tool by inheriting from the `BaseTool` class
```python
from langchain.tools import BaseTool

class YourCustomTool(BaseTool):
    name = <name>
    description = <detailed-description>
    args_schema = <PydanticModel>

    def _run(self, query):
        # functionality of the tool
        pass

    def _arun(self, query):
        # async implementation of the tool (Optional)
        raise NotImplementedError
```
We have a few tools available in the LLLLM toolkit that you can use for reference - [MercantileTool](tools/mercantile_tool.py), [GeoPyTool](tools/geopy/), [OSMnxTool](tools/osmnx/)

Learn more about creating custom tools by reading this blog on [Building Custom Tools for LLM Agents from Pinecone](https://www.pinecone.io/learn/langchain-tools/) or [documention from Langchain](https://python.langchain.com/en/latest/modules/agents/tools/custom_tools.html).


### Creating an agent

Agents act like routers using LLMs to decide which tools to use for the task at hand. There are different types of agents available in langchain:
- [ReAct](https://python.langchain.com/en/latest/modules/agents/agents/examples/react.html) - Reason & Act agents are optimized for picking tools for best response - read more about them in this [paper](https://react-lm.github.io/)
- [Conversation Agent](https://python.langchain.com/en/latest/modules/agents/agents/examples/chat_conversation_agent.html) - they are ideal to use in a conversational setting
- [Structured Tool Chat Agent](https://python.langchain.com/en/latest/modules/agents/agents/examples/structured_chat.html) - use this agent if you have tools that expect multi-input parameters. Check the OSMnx or GeoPy tool for reference.

Usage
```python
from agents.l4m_agent import base_agent

agent = base_agent(
    llm=<LLM object>, # instance of an LLM like GPT-3.5-TURBO or GPT-4
    tools=[<tool1>, <tool1>, ...], # list of tools the agent has access to perform its tasks
    name=<name of agent>, # Agent.Type for eg: zero-shot-react-description or structure-chat-zero-shot-react-description (for multi-input tools)
)
```

### Creating notebooks to test
Import the tools & create an agent in jupyter notebook to interact with them. Please find example notebooks [here](/nbs/).


### Running the streamlit app
`streamlit run app.py`
