from langchain.agents import initialize_agent
from langchain.agents import AgentType


def base_agent(llm, tools, agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION):
    """Base agent to perform xyz slippy map tiles operations.

    llm: LLM object
    tools: List of tools to use by the agent
    """
    agent = initialize_agent(
        llm=llm,
        tools=tools,
        agent=agent_type,
        max_iterations=3,
        early_stopping_method="generate",
        verbose=True,
    )

    return agent
