from fastapi import FastAPI
from pydantic import BaseModel
from src.tools import AYXMCPTools

app = FastAPI()
tools = AYXMCPTools()

class ToolRequest(BaseModel):
    action: str
    params: dict = {}

@app.post("/tool")
def tool_dispatcher(req: ToolRequest):

    if req.action == "get_all_collections":
        return tools.get_all_collections()

    if req.action == "get_collection_by_id":
        return tools.get_collection_by_id(
            req.params.get("collection_id")
        )

    return {
        "error": f"Unknown action: {req.action}"
    }

