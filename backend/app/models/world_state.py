from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Position(BaseModel):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


class BoundingBox(BaseModel):
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0


class DetectedObject(BaseModel):
    object_id: str
    label: str
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    position: Optional[Position] = None
    bounding_box: Optional[BoundingBox] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)


class SensorReading(BaseModel):
    sensor_name: str
    value: float
    unit: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class DetectedEvent(BaseModel):
    event_id: str
    event_type: str
    description: str
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    severity: str = "normal"


class Observation(BaseModel):
    observation_id: str
    modality: str
    source: str
    content: Optional[str] = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PlannedAction(BaseModel):
    action_id: str
    action_type: str
    description: str
    target: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class ActionResult(BaseModel):
    action_id: str
    status: str
    message: str
    success: bool
    verification_confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WorldState(BaseModel):
    state_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    environment: str = "unknown"
    location: Optional[str] = None

    observations: List[Observation] = Field(default_factory=list)

    detected_objects: List[DetectedObject] = Field(
        default_factory=list
    )

    sensor_readings: List[SensorReading] = Field(
        default_factory=list
    )

    detected_events: List[DetectedEvent] = Field(
        default_factory=list
    )

    planned_actions: List[PlannedAction] = Field(
        default_factory=list
    )

    action_results: List[ActionResult] = Field(
        default_factory=list
    )

    world_context: Dict[str, Any] = Field(
        default_factory=dict
    )

    overall_confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0
    )

    requires_replanning: bool = False