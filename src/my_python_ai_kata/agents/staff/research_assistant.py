"""Research assistant agent using OpenAI and HTTP requests to provide factual, well-sourced answers to research questions."""

from strands import Agent, tool  # type: ignore
from strands_tools import retrieve, http_request  # type: ignore

from my_python_ai_kata.agents.app_config import ModelConfig, get_or_create_ai_model

# Define a specialized system prompt
RESEARCH_ASSISTANT_PROMPT = """
You are a specialized research assistant. Focus only on providing
factual, well-sourced information in response to research questions.
Always cite your sources when possible.
"""

@tool
def research_assistant(query: str) -> str:
    """
    Process and respond to research-related queries.

    Args:
        query: A research question requiring factual information

    Returns:
        A detailed research answer with citations
    """
    try:
        # Strands Agents SDK makes it easy to create a specialized agent
        research_agent = get_research_assistant()

        # Call the agent and return its response
        response = research_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in research assistant: {str(e)}"


def get_research_assistant() -> Agent:
    """
    Create and return a research assistant agent.

    Returns:
        A configured Strands Agent for research assistance
    """
    model = get_or_create_ai_model(ModelConfig.from_config())
    research_agent = Agent(
        name="Research Assistant",
        description="A specialized assistant for research inquiries and information retrieval.",
        system_prompt=RESEARCH_ASSISTANT_PROMPT,
        tools=[retrieve, http_request],
        model=model
    )
    return research_agent

