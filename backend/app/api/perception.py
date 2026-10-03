from fastapi import APIRouter
from pydantic import BaseModel

from app.models.world_state import Observation
from app.perception.perception_engine import perception_engine


router = APIRouter(
    prefix="/perception",
    tags=["Perception"],
)


class PerceptionRequest(BaseModel):
    observation: Observation


@router.post("/process")
async def process_observation(
    request: PerceptionRequest,
):
    result = perception_engine.process_observation(
        request.observation
    )

    return {
        "message": "Observation processed successfully.",
        "result": result,
    }


@router.get("/result/{observation_id}")
async def get_perception_result(
    observation_id: str,
):
    result = perception_engine.get_last_result(
        observation_id
    )

    if result is None:
        return {
            "message": "No perception result found.",
            "result": None,
        }

    return {
        "message": "Perception result retrieved successfully.",
        "result": result,
    }