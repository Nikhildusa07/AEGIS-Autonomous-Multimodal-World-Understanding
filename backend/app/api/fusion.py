from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.models.world_state import Observation
from app.services.sensor_fusion import sensor_fusion_engine


router = APIRouter(
    prefix="/fusion",
    tags=["Sensor Fusion"],
)


class FusionRequest(BaseModel):
    environment: str = "simulated_environment"
    location: str | None = None
    observations: List[Observation] = Field(
        default_factory=list
    )


@router.post("/world-state")
async def create_world_state(
    request: FusionRequest,
):
    world_state = sensor_fusion_engine.fuse_observations(
        observations=request.observations,
        environment=request.environment,
        location=request.location,
    )

    return {
        "message": "Multimodal observations fused successfully.",
        "world_state": world_state,
    }


@router.get("/world-state")
async def get_current_world_state():
    world_state = sensor_fusion_engine.get_current_state()

    if world_state is None:
        return {
            "message": "No world state has been created yet.",
            "world_state": None,
        }

    return {
        "message": "Current world state retrieved successfully.",
        "world_state": world_state,
    }