from langchain.agents import initialize_agent


def base_agent(llm, tools):
    """Base agent to perform xyz slippy map tiles operations.

    llm: LLM object
    tools: List of tools to use by the agent
    """
    agent = initialize_agent(
        llm=llm,
        tools=tools,
        agent="zero-shot-react-description",
        max_iterations=5,
        early_stopping_method="generate",
        verbose=True,
    )

    return agent
