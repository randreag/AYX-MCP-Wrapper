import time
from mcp.server.fastmcp import FastMCP
from src.tools import AYXMCPTools

mcp_app = FastMCP(name="mcp-alteryx-server")
tools = AYXMCPTools()

@mcp_app.tool()
def get_all_collections():
    """Get all collections from the Alteryx server"""
    return tools.get_all_collections()

if __name__ == "__main__":
    mcp_app.run()

    # ⬇️ Mantiene vivo el proceso (CLAVE para Render)
    while True:
        time.sleep(3600)
