import os
from fastapi import FastAPI
from src.tools import AYXMCPTools

app = FastAPI(title="Alteryx Tools API")

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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

