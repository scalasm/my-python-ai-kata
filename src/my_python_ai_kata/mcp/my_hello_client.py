"""Client for interacting with a FastMCP server."""


from fastmcp import Client
import asyncio


async def interact_with_server():
    print("--- Creating Client ---")

    # Option 1: Connect to a server run via `python my_server.py` (uses stdio)
    # client = Client("my_hello_server.py")

    # Option 2: Connect to a server run via `fastmcp run ... --transport sse --port 8080`
    client = Client("http://localhost:8888") # Use the correct URL/port

    print(f"Client configured to connect to: {client}")

    try:
        async with client:
            print("--- Client Connected ---")
            # Call the 'greet' tool
            greet_result = await client.call_tool_mcp("greet", {"name": "Remote Client"})
            print(f"greet result: {greet_result}")

            # Read the 'config' resource
            config_data = await client.read_resource("data://config")
            print(f"config resource: {config_data}")

            # Read user profile 102
            profile_102 = await client.read_resource("users://102/profile")
            print(f"User 102 profile: {profile_102}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("--- Client Interaction Finished ---")

if __name__ == "__main__":
    asyncio.run(interact_with_server())
