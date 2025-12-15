
import os
from fastapi import FastAPI
from src.tools import AYXMCPTools

app = FastAPI(title="Alteryx Tools API")

tools = AYXMCPTools()

@app.get("/collections")
def get_all_collections():
    """
    Returns all available collections from the Alteryx Server.
    """
    return tools.get_all_collections()

@app.get("/collections/{collection_id}")
def get_collection_by_id(collection_id: str):
    """
    Returns a specific collection by ID.
    """
    return tools.get_collection_by_id(collection_id)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
