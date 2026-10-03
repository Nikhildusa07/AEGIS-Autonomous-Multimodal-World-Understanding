from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.reasoning.uncertainty_engine import (
    uncertainty_estimation_engine,
)


router = APIRouter(
    prefix="/uncertainty",
    tags=["Uncertainty Estimation"],
)


class UncertaintyRequest(BaseModel):
    perception_confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )
    sensor_confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )
    event_confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )
    action_confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )
    verification_confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )
    world_state_confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
    )


class WorldStateRequest(BaseModel):
    world_state: Dict[str, Any]


@router.post("/estimate")
async def estimate_uncertainty(
    request: UncertaintyRequest,
):
    try:
        result = uncertainty_estimation_engine.estimate(
            perception_confidence=(
                request.perception_confidence
            ),
            sensor_confidence=(
                request.sensor_confidence
            ),
            event_confidence=(
                request.event_confidence
            ),
            action_confidence=(
                request.action_confidence
            ),
            verification_confidence=(
                request.verification_confidence
            ),
            world_state_confidence=(
                request.world_state_confidence
            ),
            metadata=request.metadata,
        )

        return {
            "message": (
                "Uncertainty estimation "
                "completed successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Uncertainty estimation failed: "
                f"{exc}"
            ),
        )


@router.post("/world-state")
async def estimate_from_world_state(
    request: WorldStateRequest,
):
    try:
        result = (
            uncertainty_estimation_engine
            .estimate_from_world_state(
                world_state=request.world_state,
            )
        )

        return {
            "message": (
                "World state uncertainty "
                "estimation completed successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "World state uncertainty "
                f"estimation failed: {exc}"
            ),
        )


@router.get("/history")
async def get_uncertainty_history():
    try:
        result = (
            uncertainty_estimation_engine
            .get_history()
        )

        return {
            "message": (
                "Uncertainty estimation history "
                "retrieved successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to retrieve uncertainty "
                f"history: {exc}"
            ),
        )


@router.get("/result")
async def get_last_uncertainty_result():
    result = (
        uncertainty_estimation_engine
        .get_last_result()
    )

    if result is None:
        return {
            "message": (
                "No uncertainty estimation "
                "result available."
            ),
            "result": None,
        }

    return {
        "message": (
            "Latest uncertainty estimation "
            "result retrieved."
        ),
        "result": result,
    }
