from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.environment.observation_loop import (
    continuous_observation_engine,
)


router = APIRouter(
    prefix="/observation-loop",
    tags=["Continuous Observation"],
)


class StartObservationRequest(BaseModel):
    environment: str = "simulated_environment"
    location: Optional[str] = None


class AddObservationRequest(BaseModel):
    modality: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1)
    content: Optional[str] = None
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )
    environment: str = "simulated_environment"
    location: Optional[str] = None


@router.post("/start")
async def start_observation(
    request: StartObservationRequest,
):
    try:
        result = (
            continuous_observation_engine
            .start_observation(
                environment=request.environment,
                location=request.location,
            )
        )

        return {
            "message": (
                "Continuous observation started successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to start observation: {exc}"
            ),
        )


@router.post("/stop")
async def stop_observation():
    try:
        result = (
            continuous_observation_engine
            .stop_observation()
        )

        return {
            "message": (
                "Continuous observation stopped successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to stop observation: {exc}"
            ),
        )


@router.post("/observe")
async def add_observation(
    request: AddObservationRequest,
):
    try:
        result = (
            continuous_observation_engine
            .add_observation(
                modality=request.modality,
                source=request.source,
                content=request.content,
                confidence=request.confidence,
                metadata=request.metadata,
                environment=request.environment,
                location=request.location,
            )
        )

        return {
            "message": (
                "Continuous observation processed successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Continuous observation failed: {exc}"
            ),
        )


@router.get("/status")
async def get_observation_status():
    try:
        result = (
            continuous_observation_engine
            .get_status()
        )

        return {
            "message": (
                "Observation status retrieved successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to retrieve observation status: {exc}"
            ),
        )


@router.get("/latest")
async def get_latest_observation():
    try:
        result = (
            continuous_observation_engine
            .get_latest_observation()
        )

        return {
            "message": (
                "Latest observation retrieved successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to retrieve latest observation: {exc}"
            ),
        )


@router.get("/world-state")
async def get_latest_world_state():
    try:
        result = (
            continuous_observation_engine
            .get_latest_world_state()
        )

        return {
            "message": (
                "Latest world state retrieved successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to retrieve world state: {exc}"
            ),
        )


@router.get("/history")
async def get_observation_history():
    try:
        result = (
            continuous_observation_engine
            .get_observation_history()
        )

        return {
            "message": (
                "Observation history retrieved successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to retrieve observation history: {exc}"
            ),
        )


@router.get("/result")
async def get_last_observation_result():
    result = (
        continuous_observation_engine
        .get_last_result()
    )

    if result is None:
        return {
            "message": (
                "No continuous observation result available."
            ),
            "result": None,
        }

    return {
        "message": (
            "Latest continuous observation result retrieved."
        ),
        "result": result,
    }