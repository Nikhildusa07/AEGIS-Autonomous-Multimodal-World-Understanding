from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.reasoning.event_engine import (
    event_detection_engine,
)


router = APIRouter(
    prefix="/events",
    tags=["Event Detection"],
)


class ObjectEventRequest(BaseModel):
    objects: List[Dict[str, Any]] = Field(
        default_factory=list
    )


class PresenceEventRequest(BaseModel):
    entity: str = Field(..., min_length=1)
    present: bool
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )


class ThresholdEventRequest(BaseModel):
    sensor_name: str = Field(..., min_length=1)
    value: float
    threshold: float
    operator: str = "greater_than"
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )


class CustomEventRequest(BaseModel):
    event_type: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )
    severity: str = "normal"
    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )


@router.post("/objects")
async def detect_object_events(
    request: ObjectEventRequest,
):
    try:
        result = (
            event_detection_engine
            .detect_object_events(
                current_objects=request.objects,
            )
        )

        return {
            "message": "Object events detected successfully.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Object event detection failed: {exc}",
        )


@router.post("/presence")
async def detect_presence_event(
    request: PresenceEventRequest,
):
    try:
        result = (
            event_detection_engine
            .detect_presence_event(
                entity=request.entity,
                present=request.present,
                confidence=request.confidence,
            )
        )

        return {
            "message": "Presence event detected successfully.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Presence event detection failed: {exc}",
        )


@router.post("/threshold")
async def detect_threshold_event(
    request: ThresholdEventRequest,
):
    try:
        result = (
            event_detection_engine
            .detect_threshold_event(
                sensor_name=request.sensor_name,
                value=request.value,
                threshold=request.threshold,
                operator=request.operator,
                confidence=request.confidence,
            )
        )

        return {
            "message": "Threshold event detection completed.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Threshold event detection failed: {exc}",
        )


@router.post("/custom")
async def add_custom_event(
    request: CustomEventRequest,
):
    try:
        result = (
            event_detection_engine
            .add_custom_event(
                event_type=request.event_type,
                description=request.description,
                confidence=request.confidence,
                severity=request.severity,
                metadata=request.metadata,
            )
        )

        return {
            "message": "Custom event added successfully.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Custom event creation failed: {exc}",
        )


@router.get("/")
async def get_all_events():
    try:
        result = (
            event_detection_engine
            .get_all_events()
        )

        return {
            "message": "All detected events retrieved successfully.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve events: {exc}",
        )


@router.get("/result")
async def get_last_event_result():
    result = (
        event_detection_engine
        .get_last_result()
    )

    if result is None:
        return {
            "message": "No event detection result available.",
            "result": None,
        }

    return {
        "message": "Latest event detection result retrieved.",
        "result": result,
    }