#!/usr/bin/env python3
"""
FastMCP v2 Proxy Wrapper for Amazon Neptune MCP Server
Uses FastMCP's built-in proxy capabilities to wrap the AG2 server
"""

import os
import sys
from fastmcp import FastMCP
from fastmcp.server.proxy import ProxyClient

# Create a wrapper script that will run the AG2 server with streamable-http
wrapper_script = "/app/run_server.py"
with open(wrapper_script, "w") as f:
    f.write("""#!/usr/bin/env python3
import subprocess
import sys

# Run the AG2 server with streamable-http transport
subprocess.run([
    sys.executable,
    "-m", "mcp_server.main",
    "streamable-http"
], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
""")
os.chmod(wrapper_script, 0o755)

# Create FastMCP proxy that wraps the AG2 server
proxy = FastMCP.as_proxy(
    ProxyClient(wrapper_script),
    name="amazon-neptune-proxy"
)

# Add API key authentication middleware
@proxy.middleware
async def api_key_auth(request, call_next):
    """API key authentication middleware"""
    expected_key = os.environ.get('CLOUD_RUN_API_KEY')
    if expected_key:
        provided_key = request.headers.get('X-API-Key', '')
        if provided_key != expected_key:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32001,
                    'message': 'Unauthorized - Invalid API key'
                },
                'id': request.get('id') if isinstance(request, dict) else None
            }
    return await call_next(request)

if __name__ == "__main__":
    # Use FastMCP's built-in HTTP transport
    port = int(os.environ.get('PORT', 8080))
    proxy.run(transport="http", host="0.0.0.0", port=port, path="/")