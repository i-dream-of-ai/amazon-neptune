FROM python:3.12-slim

WORKDIR /app

# Copy the original server code
COPY . .

# Install dependencies for the server
RUN pip install -e .

# Set environment for HTTP transport
ENV MCP_TRANSPORT=streamable-http
ENV PORT=8080

# Expose port
EXPOSE 8080

# Install FastMCP for proxy functionality
RUN pip install fastmcp

# Run the FastMCP proxy
CMD ["python", "/app/fastmcp-wrapper/proxy_server.py"]