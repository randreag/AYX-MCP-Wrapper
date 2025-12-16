import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from src.tools import AYXMCPTools
# =========================
# INIT
# =========================

app = FastAPI(title="Alteryx AI API")
tools = AYXMCPTools()

# =========================
# ACTION REGISTRY
# =========================

ACTION_REGISTRY = {

    # =========================
    # COLLECTIONS
    # =========================
    "create_collection": {
        "method": "create_collection",
        "required_params": ["name"]
    },
    "delete_collection": {
        "method": "delete_collection",
        "required_params": ["collection_id"]
    },
    "update_collection_name_or_owner": {
        "method": "update_collection_name_or_owner",
        "required_params": ["collection_id", "name", "owner_id"]
    },
    "add_workflow_to_collection": {
        "method": "add_workflow_to_collection",
        "required_params": ["collection_id", "workflow_id"]
    },
    "remove_workflow_from_collection": {
        "method": "remove_workflow_from_collection",
        "required_params": ["collection_id", "workflow_id"]
    },
    "add_schedule_to_collection": {
        "method": "add_schedule_to_collection",
        "required_params": ["collection_id", "schedule_id"]
    },
    "remove_schedule_from_collection": {
        "method": "remove_schedule_from_collection",
        "required_params": ["collection_id", "schedule_id"]
    },

    # =========================
    # WORKFLOWS
    # =========================
    "get_all_workflows": {
        "method": "get_all_workflows",
        "required_params": []
    },
    "get_workflow_by_id": {
        "method": "get_workflow_by_id",
        "required_params": ["workflow_id"]
    },
    "update_workflow_name_or_comment": {
        "method": "update_workflow_name_or_comment",
        "required_params": ["workflow_id", "name", "comment"]
    },
    "download_workflow_package_file": {
        "method": "download_workflow_package_file",
        "required_params": ["workflow_id", "output_directory"]
    },
    "get_workflow_xml": {
        "method": "get_workflow_xml",
        "required_params": ["workflow_id"]
    },
    "get_workflow_tool_list": {
        "method": "get_workflow_tool_list",
        "required_params": ["workflow_id"]
    },
    "transfer_workflow": {
        "method": "transfer_workflow",
        "required_params": ["workflow_id", "new_owner_id"]
    },
    "get_workflow_jobs": {
        "method": "get_workflow_jobs",
        "required_params": ["workflow_id"]
    },
    "start_workflow_execution": {
        "method": "start_workflow_execution",
        "required_params": ["workflow_id"]
    },
    "execute_workflow_with_monitoring": {
        "method": "execute_workflow_with_monitoring",
        "required_params": ["workflow_id"]
    },

    # =========================
    # USERS
    # =========================
    "get_all_users": {
        "method": "get_all_users",
        "required_params": []
    },
    "get_user_by_id": {
        "method": "get_user_by_id",
        "required_params": ["user_id"]
    },
    "get_user_by_email": {
        "method": "get_user_by_email",
        "required_params": ["email"]
    },
    "get_user_by_name": {
        "method": "get_user_by_name",
        "required_params": ["name"]
    },
    "get_user_by_first_name": {
        "method": "get_user_by_first_name",
        "required_params": ["first_name"]
    },
    "get_all_user_assets": {
        "method": "get_all_user_assets",
        "required_params": ["user_id"]
    },
    "get_user_assets_by_type": {
        "method": "get_user_assets_by_type",
        "required_params": ["user_id", "asset_type"]
    },
    "update_user_details": {
        "method": "update_user_details",
        "required_params": ["user_id", "first_name", "last_name", "email"]
    },
    "transfer_all_assets": {
        "method": "transfer_all_assets",
        "required_params": ["user_id", "new_owner_id"]
    },
    "deactivate_user": {
        "method": "deactivate_user",
        "required_params": ["user_id"]
    },
    "reset_user_password": {
        "method": "reset_user_password",
        "required_params": ["user_id"]
    },

    # =========================
    # JOBS
    # =========================
    "get_all_job_messages": {
        "method": "get_all_job_messages",
        "required_params": ["job_id"]
    },
    "get_job_by_id": {
        "method": "get_job_by_id",
        "required_params": ["job_id"]
    },
    "get_job_output_data": {
        "method": "get_job_output_data",
        "required_params": ["job_id"]
    },

    # =========================
    # SCHEDULES
    # =========================
    "get_all_schedules": {
        "method": "get_all_schedules",
        "required_params": []
    },
    "get_schedule_by_id": {
        "method": "get_schedule_by_id",
        "required_params": ["schedule_id"]
    },
    "deactivate_schedule": {
        "method": "deactivate_schedule",
        "required_params": ["schedule_id"]
    },
    "activate_schedule": {
        "method": "activate_schedule",
        "required_params": ["schedule_id"]
    },
    "update_schedule_name_or_comment": {
        "method": "update_schedule_name_or_comment",
        "required_params": ["schedule_id", "name", "comment"]
    },
    "change_schedule_owner": {
        "method": "change_schedule_owner",
        "required_params": ["schedule_id", "new_owner_id"]
    },

    # =========================
    # CREDENTIALS
    # =========================
    "get_all_credentials": {
        "method": "get_all_credentials",
        "required_params": []
    },
    "get_credential_by_id": {
        "method": "get_credential_by_id",
        "required_params": ["credential_id"]
    },

    # =========================
    # CONNECTIONS
    # =========================
    "lookup_connection": {
        "method": "lookup_connection",
        "required_params": ["connection_id"]
    },
    "get_connection_by_id": {
        "method": "get_connection_by_id",
        "required_params": ["connection_id"]
    }
}



# =========================
# MODELS
# =========================

class InvokeRequest(BaseModel):
    action: str
    params: Dict[str, Any] = {}


# =========================
# ROUTES
# =========================

@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/actions")
def list_actions():
    """
    Allows the LLM (and you) to see all available actions
    """
    return {
        action: {
            "required_params": data["required_params"]
        }
        for action, data in ACTION_REGISTRY.items()
    }


@app.post("/invoke")
def invoke(req: InvokeRequest):
    """
    Single endpoint to execute ANY action
    """

    if req.action not in ACTION_REGISTRY:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown action: {req.action}"
        )

    action_def = ACTION_REGISTRY[req.action]
    method_name = action_def["method"]
    required_params = action_def["required_params"]

    # validate params
    missing = [p for p in required_params if p not in req.params]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing params: {missing}"
        )

    # dynamic dispatch
    try:
        method = getattr(tools, method_name)
        return method(**req.params)
    except Exception as e:
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
