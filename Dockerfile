# Build the MCP Server Python Docker image
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/

CMD ["fastmcp", "run", "my_python_ai_kata/mcp/my_hello_server.py"]
