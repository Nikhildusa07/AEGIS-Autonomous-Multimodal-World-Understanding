from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.planning.replanning_engine import (
    replanning_engine,
)


router = APIRouter(
    prefix="/replanning",
    tags=["Replanning"],
)


class ReplanningRequest(BaseModel):
    world_state: Dict[str, Any]
    verification: Optional[Dict[str, Any]] = None


@router.post("/evaluate")
async def evaluate_replanning(
    request: ReplanningRequest,
):
    try:
        result = (
            replanning_engine
            .evaluate_replanning(
                world_state=request.world_state,
                verification=request.verification,
            )
        )

        return {
            "message": (
                "Replanning evaluation completed successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Replanning evaluation failed: {exc}"
            ),
        )


@router.post("/generate")
async def generate_new_plan(
    request: ReplanningRequest,
):
    try:
        result = (
            replanning_engine
            .generate_new_plan(
                world_state=request.world_state,
                verification=request.verification,
            )
        )

        return {
            "message": (
                "New plan generated successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Plan generation failed: {exc}"
            ),
        )


@router.post("/from-verification")
async def replan_from_verification(
    request: ReplanningRequest,
):
    if request.verification is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Verification data is required "
                "for verification-based replanning."
            ),
        )

    try:
        result = (
            replanning_engine
            .replan_from_verification(
                world_state=request.world_state,
                verification=request.verification,
            )
        )

        return {
            "message": (
                "Replanning from verification completed successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Verification-based replanning failed: {exc}"
            ),
        )


@router.get("/history")
async def get_replanning_history():
    try:
        result = (
            replanning_engine
            .get_replanning_history()
        )

        return {
            "message": (
                "Replanning history retrieved successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to retrieve replanning history: {exc}"
            ),
        )


@router.get("/result")
async def get_last_replanning_result():
    result = (
        replanning_engine
        .get_last_result()
    )

    if result is None:
        return {
            "message": (
                "No replanning result available."
            ),
            "result": None,
        }

    return {
        "message": (
            "Latest replanning result retrieved."
        ),
        "result": result,
    }