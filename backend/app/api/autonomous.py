from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.autonomous_loop import (
    autonomous_loop_engine,
)


router = APIRouter(
    prefix="/autonomous",
    tags=["Autonomous Loop"],
)


class AutonomousLoopRequest(BaseModel):
    world_state: Dict[str, Any]

    visual_objects: List[Dict[str, Any]] = Field(
        default_factory=list
    )

    visual_scene: Optional[str] = None

    ocr_text: Optional[str] = None

    audio_transcript: Optional[str] = None

    text_context: Optional[str] = None

    execute_actions: bool = True

    observation_inputs: List[
        Dict[str, Any]
    ] = Field(default_factory=list)


@router.post("/run")
async def run_autonomous_cycle(
    request: AutonomousLoopRequest,
):
    try:
        result = autonomous_loop_engine.run_cycle(
            world_state=request.world_state,
            visual_objects=request.visual_objects,
            visual_scene=request.visual_scene,
            ocr_text=request.ocr_text,
            audio_transcript=request.audio_transcript,
            text_context=request.text_context,
            execute_actions=request.execute_actions,
            observation_inputs=request.observation_inputs,
        )

        return {
            "message": (
                "Autonomous AEGIS cycle "
                "completed successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Autonomous cycle failed: "
                f"{exc}"
            ),
        )


@router.get("/history")
async def get_autonomous_history():
    try:
        result = (
            autonomous_loop_engine
            .get_history()
        )

        return {
            "message": (
                "Autonomous cycle history "
                "retrieved successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to retrieve autonomous "
                f"history: {exc}"
            ),
        )


@router.get("/result")
async def get_last_autonomous_result():
    result = (
        autonomous_loop_engine
        .get_last_result()
    )

    if result is None:
        return {
            "message": (
                "No autonomous cycle result "
                "available."
            ),
            "result": None,
        }

    return {
        "message": (
            "Latest autonomous cycle result "
            "retrieved."
        ),
        "result": result,
    }