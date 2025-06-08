#!/Users/rlm/Desktop/Code/vibe-code-benchmark/.venv/bin/python
"""Query tool for Langraph using the example vector store."""

import os
from mcp.server.fastmcp import FastMCP

from my_python_ai_kata.mcp.vector_store_helpers import VectorStoreQueryHelper

# Define common path to the repo locally
work_dir = "/workspaces/my-python-ai-kata/vector_store_data"  # os.path.join(os.getcwd(), "vector_store_data")
parquet_path = os.path.join(work_dir, "sklearn_vectorstore.parquet")

print(f"Using vector store at {parquet_path!r} for LangGraph documentation queries.")
query_helper = VectorStoreQueryHelper(parquet_path=parquet_path)

# Create an MCP server
mcp = FastMCP("LangGraph-Docs-MCP-Server")


# Add a tool to query the LangGraph documentation
@mcp.tool(description="Query the LangGraph documentation.")
def langgraph_query_tool(query: str) -> str:
    """Query the LangGraph documentation using a retriever.

    Args:
        query (str): The query to search the documentation with

    Returns:
        str: A str of the retrieved documents
    """
    relevant_docs = query_helper.query(query)

    formatted_context = "\n\n".join([f"==DOCUMENT {i + 1}==\n{doc.page_content}" for i, doc in enumerate(relevant_docs)])
    return formatted_context


# The @mcp.resource() decorator is meant to map a URI pattern to a function that provides the resource content
@mcp.resource(uri="docs://langgraph/full", description="Get all LangGraph documentation in one single shot.")
def get_all_langgraph_docs() -> str:
    """Get all the LangGraph documentation.

    Returns the contents of the file llms_full.txt,
    which contains a curated set of LangGraph documentation (~300k tokens). This is useful
    for a comprehensive response to questions about LangGraph.

    Returns:
        str: The contents of the LangGraph documentation
    """
    # Local path to the LangGraph documentation
    return query_helper.get_llms_full()


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
