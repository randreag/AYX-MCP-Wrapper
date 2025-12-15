import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from src.tools import AYXMCPTools

# -------------------------------------------------
# App init
# -------------------------------------------------

app = FastAPI(
    title="Alteryx Tool Dispatcher API",
    version="1.0.0"
)

tools = AYXMCPTools()

# -------------------------------------------------
# Models
# -------------------------------------------------

class ToolRequest(BaseModel):
    action: str
    params: Dict[str, Any] = {}

# -------------------------------------------------
# Health check (Render needs this)
# -------------------------------------------------

@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "alteryx-tool-dispatcher"
    }

# -------------------------------------------------
# Tool dispatcher (USED BY n8n / LLM)
# -------------------------------------------------

@app.post("/tool")
def tool_dispatcher(req: ToolRequest):

    action = req.action
    params = req.params or {}

    try:
        # ----------------------------
        # COLLECTIONS
        # ----------------------------

        if action == "get_all_collections":
            return tools.get_all_collections()

        if action == "get_collection_by_id":
            collection_id = params.get("collection_id")
            if not collection_id:
                raise HTTPException(
                    status_code=400,
                    detail="Missing required param: collection_id"
                )
            return tools.get_collection_by_id(collection_id)

        # ----------------------------
        # UNKNOWN ACTION
        # ----------------------------

        raise HTTPException(
            status_code=400,
            detail=f"Unknown action: {action}"
        )

    except HTTPException:
        raise

    except Exception as e:
        # Protect LLM from raw crashes
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# -------------------------------------------------
# Run server (Render)
# -------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
