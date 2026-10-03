from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.reasoning.vision_language_engine import (
    vision_language_reasoning_engine,
)


router = APIRouter(
    prefix="/vision-language",
    tags=["Vision-Language Reasoning"],
)


class VisionLanguageRequest(BaseModel):
    visual_objects: List[Dict[str, Any]] = Field(
        default_factory=list
    )
    visual_scene: Optional[str] = None
    ocr_text: Optional[str] = None
    audio_transcript: Optional[str] = None
    text_context: Optional[str] = None
    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )


class ObservationReasoningRequest(BaseModel):
    observation: Dict[str, Any]


@router.post("/reason")
async def reason_from_multimodal_input(
    request: VisionLanguageRequest,
):
    try:
        result = (
            vision_language_reasoning_engine.reason(
                visual_objects=request.visual_objects,
                visual_scene=request.visual_scene,
                ocr_text=request.ocr_text,
                audio_transcript=request.audio_transcript,
                text_context=request.text_context,
                metadata=request.metadata,
            )
        )

        return {
            "message": (
                "Vision-language reasoning "
                "completed successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Vision-language reasoning "
                f"failed: {exc}"
            ),
        )


@router.post("/observation")
async def reason_from_observation(
    request: ObservationReasoningRequest,
):
    try:
        result = (
            vision_language_reasoning_engine
            .reason_from_observation(
                observation=request.observation
            )
        )

        return {
            "message": (
                "Observation-based vision-language "
                "reasoning completed successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Observation-based reasoning "
                f"failed: {exc}"
            ),
        )


@router.get("/history")
async def get_reasoning_history():
    try:
        result = (
            vision_language_reasoning_engine
            .get_history()
        )

        return {
            "message": (
                "Vision-language reasoning history "
                "retrieved successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to retrieve reasoning "
                f"history: {exc}"
            ),
        )


@router.get("/result")
async def get_last_reasoning_result():
    result = (
        vision_language_reasoning_engine
        .get_last_result()
    )

    if result is None:
        return {
            "message": (
                "No vision-language reasoning "
                "result available."
            ),
            "result": None,
        }

    return {
        "message": (
            "Latest vision-language reasoning "
            "result retrieved."
        ),
        "result": result,
    }