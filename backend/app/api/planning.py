from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.planning.action_engine import (
    action_planning_engine,
)


router = APIRouter(
    prefix="/planning",
    tags=["Action Planning"],
)


class ActionRequest(BaseModel):
    action_type: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    target: Optional[str] = None
    parameters: Dict[str, Any] = Field(
        default_factory=dict
    )
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )
    priority: str = "normal"


class EventPlanningRequest(BaseModel):
    event_type: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    severity: str = "normal"
    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )


class MultipleEventsPlanningRequest(BaseModel):
    events: List[Dict[str, Any]] = Field(
        default_factory=list
    )


class ActionStatusRequest(BaseModel):
    action_id: str = Field(..., min_length=1)
    status: str = Field(..., min_length=1)


@router.post("/action")
async def create_action(
    request: ActionRequest,
):
    try:
        result = action_planning_engine.create_action(
            action_type=request.action_type,
            description=request.description,
            target=request.target,
            parameters=request.parameters,
            confidence=request.confidence,
            priority=request.priority,
        )

        return {
            "message": "Action planned successfully.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Action planning failed: {exc}",
        )


@router.post("/event")
async def plan_from_event(
    request: EventPlanningRequest,
):
    try:
        result = action_planning_engine.plan_from_event(
            event_type=request.event_type,
            description=request.description,
            severity=request.severity,
            metadata=request.metadata,
        )

        return {
            "message": (
                "Action planned from event successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Event-based action planning failed: {exc}"
            ),
        )


@router.post("/events")
async def plan_from_events(
    request: MultipleEventsPlanningRequest,
):
    try:
        result = action_planning_engine.plan_from_events(
            events=request.events,
        )

        return {
            "message": (
                "Actions planned from events successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Multiple-event planning failed: {exc}"
            ),
        )


@router.patch("/status")
async def update_action_status(
    request: ActionStatusRequest,
):
    try:
        result = (
            action_planning_engine
            .update_action_status(
                action_id=request.action_id,
                status=request.status,
            )
        )

        return {
            "message": (
                "Action status updated successfully."
            ),
            "result": result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Action status update failed: {exc}"
            ),
        )


@router.get("/actions")
async def get_all_actions():
    try:
        result = (
            action_planning_engine
            .get_all_actions()
        )

        return {
            "message": (
                "All planned actions retrieved successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to retrieve planned actions: {exc}"
            ),
        )


@router.get("/result")
async def get_last_planning_result():
    result = (
        action_planning_engine
        .get_last_result()
    )

    if result is None:
        return {
            "message": (
                "No action planning result available."
            ),
            "result": None,
        }

    return {
        "message": (
            "Latest action planning result retrieved."
        ),
        "result": result,
    }