from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.tools import AIPluginTool

llm = ChatOpenAI(temperature=0)

tool = AIPluginTool.from_plugin_url("https://goadmin-stage.ifrc.org/.well-known/ai-plugin.json")

tools = [tool]

agent_chain = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

agent_chain.run("Can you tell me a bit about major emergencies in Nepal in the last decade?")