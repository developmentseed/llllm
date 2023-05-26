from langchain.agents import initialize_agent


def base_agent(llm, tools, name="zero-shot-react-description"):
    """Base agent to perform xyz slippy map tiles operations.

    llm: LLM object
    tools: List of tools to use by the agent
    """
    agent = initialize_agent(
        llm=llm,
        tools=tools,
        agent=name,
        max_iterations=3,
        early_stopping_method="generate",
        verbose=True,
    )

    return agent
