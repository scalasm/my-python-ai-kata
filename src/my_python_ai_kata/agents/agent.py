"""Simple Agent using Strands Agentic framework with OpenAI."""

from os import environ
from strands import Agent
from strands.types.tools import AgentTool
from strands.tools.mcp import MCPClient
from strands_tools import http_request  # pyright: ignore[reportMissingTypeStubs]
from strands.models.openai import OpenAIModel
from mcp import stdio_client, StdioServerParameters

# Define a naming-focused system prompt
NAMING_SYSTEM_PROMPT = """
You are an assistant that helps to name open source projects.

When providing open source project name suggestions, always provide
one or more available domain names and one or more available GitHub
organization names that could be used for the project.

Before providing your suggestions, use your tools to validate
that the domain names are not already registered and that the GitHub
organization names are not already used.
"""

# Load an MCP server that can determine if a domain name is available
domain_name_tools = MCPClient(lambda: stdio_client(
    StdioServerParameters(command="uvx", args=["fastdomaincheck-mcp-server"])
))

# Use a pre-built Strands Agents tool that can make requests to GitHub
# to determine if a GitHub organization name is available
github_tools = [http_request]

model = OpenAIModel(
    client_args={
        "api_key": environ.get("OPENAI_API_KEY"),
    },
    # **model_config
    model_id="gpt-4o",
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)

with domain_name_tools:
    # Define the naming agent with tools and a system prompt
    tools: list[AgentTool] = domain_name_tools.list_tools_sync() + github_tools  # type: ignore
    naming_agent = Agent(
        system_prompt=NAMING_SYSTEM_PROMPT,
        model=model,
        tools=tools
    )

    # Run the naming agent with the end user's prompt
    result = naming_agent("I need to name an open source project for building AI agents.")

    print(f"\nTotal tokens: {result.metrics.accumulated_usage['totalTokens']}")
    print(f"Execution time: {sum(result.metrics.cycle_durations):.2f} seconds")
    print(f"Tools used: {list(result.metrics.tool_metrics.keys())}")
