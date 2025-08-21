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

# Run the server directly with streamable-http transport
CMD ["python", "-m", "mcp_server.main", "streamable-http"]