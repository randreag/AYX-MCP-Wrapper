import os
import threading
import uvicorn
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from tools import AYXMCPTools

# ---------------------------
#  MCP SERVER (WEBSOCKET)
# ---------------------------

mcp_app = FastMCP(name="mcp-alteryx-server")
tools = AYXMCPTools()

@mcp_app.tool()
def get_all_collections():
    return tools.get_all_collections()

def run_mcp():
    mcp_app.run()   # esta es la forma correcta para tu versión

threading.Thread(target=run_mcp, daemon=True).start()


# ---------------------------
#  HTTP API (REST)
# ---------------------------

api = FastAPI()

@api.get("/")
def health():
    return {"status": "ok", "service": "mcp-alteryx-server"}

@api.get("/collections")
def http_get_collections():
    return tools.get_all_collections()


# ---------------------------
#  RUN FASTAPI SERVER
# ---------------------------

port = int(os.getenv("PORT", 10000))
uvicorn.run(api, host="0.0.0.0", port=port)
