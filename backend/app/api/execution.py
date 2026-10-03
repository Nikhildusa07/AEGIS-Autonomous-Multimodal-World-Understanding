from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.environment.action_executor import (
    action_execution_engine,
)


router = APIRouter(
    prefix="/execution",
    tags=["Action Execution"],
)


class ExecuteActionRequest(BaseModel):
    action_type: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    target: Optional[str] = None
    parameters: Dict[str, Any] = Field(
        default_factory=dict
    )


@router.post("/execute")
async def execute_action(
    request: ExecuteActionRequest,
):
    try:
        result = action_execution_engine.execute_action(
            action_type=request.action_type,
            description=request.description,
            target=request.target,
            parameters=request.parameters,
        )

        return {
            "message": "Action executed successfully.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Action execution failed: {exc}",
        )


@router.get("/history")
async def get_execution_history():
    try:
        result = (
            action_execution_engine
            .get_execution_history()
        )

        return {
            "message": (
                "Action execution history retrieved successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to retrieve execution history: {exc}"
            ),
        )


@router.get("/result")
async def get_last_execution_result():
    result = (
        action_execution_engine
        .get_last_result()
    )

    if result is None:
        return {
            "message": (
                "No action execution result available."
            ),
            "result": None,
        }

    return {
        "message": (
            "Latest action execution result retrieved."
        ),
        "result": result,
    }