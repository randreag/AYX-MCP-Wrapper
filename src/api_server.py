import os
import uvicorn
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from src.tools import AYXMCPTools
import mcp
print("MCP VERSION:", mcp.__version__)
# FastAPI app (lo que Render expone)
app = FastAPI()

# MCP app
mcp = FastMCP(name="mcp-alteryx-server")
tools = AYXMCPTools()

@mcp.tool()
def get_all_collections():
    """Get all collections from the Alteryx server"""
    return tools.get_all_collections()

# 🔗 Montar MCP dentro de FastAPI
app.mount("/", mcp.app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
