from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.reasoning.scene_engine import (
    scene_understanding_engine,
)


router = APIRouter(
    prefix="/scene",
    tags=["Scene Understanding"],
)


class SceneRequest(BaseModel):
    objects: List[Dict[str, Any]] = Field(
        default_factory=list
    )
    ocr_text: str = ""
    audio_transcript: str = ""
    environment: str = "unknown"
    location: Optional[str] = None


@router.post("/analyze")
async def analyze_scene(
    request: SceneRequest,
):
    result = scene_understanding_engine.analyze_scene(
        objects=request.objects,
        ocr_text=request.ocr_text,
        audio_transcript=request.audio_transcript,
        environment=request.environment,
        location=request.location,
    )

    return {
        "message": "Scene understanding completed.",
        "result": result,
    }


@router.get("/result")
async def get_scene_result():
    result = scene_understanding_engine.get_last_result()

    if result is None:
        return {
            "message": "No scene analysis available.",
            "result": None,
        }

    return {
        "message": "Latest scene analysis retrieved.",
        "result": result,
    }