from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/observations",
    tags=["Multimodal Observations"],
)


ALLOWED_MODALITIES = {
    "text",
    "image",
    "video",
    "audio",
    "document",
    "sensor",
}


class TextObservationRequest(BaseModel):
    text: str = Field(..., min_length=1)
    source: str = "user"


class SensorObservationRequest(BaseModel):
    sensor_name: str
    value: float
    unit: str
    source: str = "sensor"


class ObservationResponse(BaseModel):
    observation_id: str
    modality: str
    source: str
    message: str
    timestamp: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)


def create_observation_response(
    modality: str,
    source: str,
    message: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> ObservationResponse:
    return ObservationResponse(
        observation_id=str(uuid4()),
        modality=modality,
        source=source,
        message=message,
        timestamp=datetime.utcnow(),
        metadata=metadata or {},
    )


@router.post("/text", response_model=ObservationResponse)
async def receive_text_observation(
    request: TextObservationRequest,
):
    return create_observation_response(
        modality="text",
        source=request.source,
        message="Text observation received successfully.",
        metadata={
            "text": request.text,
        },
    )


@router.post("/sensor", response_model=ObservationResponse)
async def receive_sensor_observation(
    request: SensorObservationRequest,
):
    return create_observation_response(
        modality="sensor",
        source=request.source,
        message="Sensor observation received successfully.",
        metadata={
            "sensor_name": request.sensor_name,
            "value": request.value,
            "unit": request.unit,
        },
    )


@router.post("/file", response_model=ObservationResponse)
async def receive_file_observation(
    modality: str = Form(...),
    file: UploadFile = File(...),
):
    modality = modality.lower().strip()

    if modality not in {
        "image",
        "video",
        "audio",
        "document",
    }:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid file modality. Use one of: "
                "image, video, audio, document."
            ),
        )

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    return create_observation_response(
        modality=modality,
        source="file_upload",
        message="File observation received successfully.",
        metadata={
            "filename": file.filename,
            "content_type": file.content_type,
        },
    )


@router.get("/modalities")
async def get_supported_modalities():
    return {
        "supported_modalities": sorted(ALLOWED_MODALITIES),
        "count": len(ALLOWED_MODALITIES),
    }