from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory


def base_agent(
    llm, tools, agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
):
    """Base agent to perform xyz slippy map tiles operations.

    llm: LLM object
    tools: List of tools to use by the agent
    """
    # chat_history = MessagesPlaceholder(variable_name="chat_history")
    # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = initialize_agent(
        llm=llm,
        tools=tools,
        agent=agent_type,
        max_iterations=5,
        early_stopping_method="generate",
        verbose=True,
        # memory=memory,
        # agent_kwargs={
        #     "memory_prompts": [chat_history],
        #     "input_variables": ["input", "agent_scratchpad", "chat_history"],
        # },
    )
    print("agent initialized")
    return agent


def openai_function_agent(llm, tools, agent_type=AgentType.OPENAI_FUNCTIONS):
    """OpenAI function agent that is fine-tuned to call functions with valid arguments.

    llm: LLM object
    tools: List of tools to use by the agent
    """
    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    }
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True)
    agent = initialize_agent(
        llm=llm,
        tools=tools,
        agent=agent_type,
        max_iterations=5,
        early_stopping_method="generate",
        verbose=True,
        agent_kwargs=agent_kwargs,
        memory=memory,
        # memory=memory,
        # agent_kwargs={
        #     "memory_prompts": [chat_history],
        #     "input_variables": ["input", "agent_scratchpad", "chat_history"],
        # },
    )
    print("OpenAI function agent initialized")
    return agent
