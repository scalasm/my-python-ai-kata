"""Hello World MCP Server."""

from typing import Any, Literal
from fastmcp import FastMCP


mcp: FastMCP = FastMCP(name="My First MCP Server")  # type: ignore


@mcp.tool(description="Greet a person by name provided as input")
def greet(name: str) -> str:
    """Returns a simple greeting."""
    return f"Hello, {name}!"


@mcp.tool(description="Add two integers together, in a very smart way!")
def add(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b


APP_CONFIG = {"theme": "dark", "version": "1.1", "feature_flags": ["new_dashboard"]}


@mcp.resource("data://config")
def get_config() -> dict:  # type: ignore
    """Provides the application configuration."""
    return APP_CONFIG


USER_PROFILES = {
    101: {"name": "Alice", "status": "active"},
    102: {"name": "Bob", "status": "inactive"},
}


@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: int) -> dict[str, Any]:
    """Retrieves a user's profile by their ID."""
    # The {user_id} from the URI is automatically passed as an argument
    return USER_PROFILES.get(user_id, {"error": "User not found"})


@mcp.prompt("summarize")
async def summarize_prompt(text: str) -> list[dict]:  # type: ignore
    """Generates a prompt to summarize the provided text."""
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant skilled at summarization.",
        },
        {"role": "user", "content": f"Please summarize the following text:\n\n{text}"},
    ]  # type: ignore


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Start the MCP server.")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default="stdio",
        help="Transport to use for the server (default: stdio)",
    )
    args = parser.parse_args()
    transport: Literal["stdio", "streamable-http", "sse"] = args.transport  # type: ignore
    print(f"\n--- Starting {mcp.name!r} via __main__ (transport={transport!r}) ---")
    mcp.run(transport=transport)
