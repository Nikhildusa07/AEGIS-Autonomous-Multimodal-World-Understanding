from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.reasoning.spatial_engine import (
    spatial_reasoning_engine,
)


router = APIRouter(
    prefix="/spatial",
    tags=["Spatial Reasoning"],
)


class SpatialRelationRequest(BaseModel):
    subject: str = Field(..., min_length=1)
    relation: str = Field(..., min_length=1)
    object_name: str = Field(..., min_length=1)
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )


class PointRequest(BaseModel):
    x: float
    y: float
    z: Optional[float] = None


class DistanceRequest(BaseModel):
    point_a: PointRequest
    point_b: PointRequest


class DirectionRequest(BaseModel):
    subject_position: PointRequest
    reference_position: PointRequest


class ProximityRequest(BaseModel):
    distance: float = Field(..., ge=0.0)
    near_threshold: float = Field(
        default=2.0,
        ge=0.0,
    )
    far_threshold: float = Field(
        default=10.0,
        ge=0.0,
    )


class SpatialQueryRequest(BaseModel):
    entity_name: Optional[str] = None
    relation: Optional[str] = None


@router.post("/relation")
async def add_spatial_relation(
    request: SpatialRelationRequest,
):
    try:
        result = spatial_reasoning_engine.add_relation(
            subject=request.subject,
            relation=request.relation,
            object_name=request.object_name,
            confidence=request.confidence,
            metadata=request.metadata,
        )

        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add spatial relation: {exc}",
        )


@router.post("/distance")
async def calculate_distance(
    request: DistanceRequest,
):
    try:
        point_a = request.point_a.model_dump(
            exclude_none=True
        )
        point_b = request.point_b.model_dump(
            exclude_none=True
        )

        result = (
            spatial_reasoning_engine.calculate_distance(
                point_a=point_a,
                point_b=point_b,
            )
        )

        return {
            "message": "Spatial distance calculated.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Distance calculation failed: {exc}",
        )


@router.post("/direction")
async def determine_direction(
    request: DirectionRequest,
):
    try:
        subject_position = (
            request.subject_position.model_dump(
                exclude_none=True
            )
        )

        reference_position = (
            request.reference_position.model_dump(
                exclude_none=True
            )
        )

        result = (
            spatial_reasoning_engine.determine_direction(
                subject_position=subject_position,
                reference_position=reference_position,
            )
        )

        return {
            "message": "Spatial direction determined.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Direction calculation failed: {exc}",
        )


@router.post("/proximity")
async def classify_proximity(
    request: ProximityRequest,
):
    try:
        result = (
            spatial_reasoning_engine.classify_proximity(
                distance=request.distance,
                near_threshold=request.near_threshold,
                far_threshold=request.far_threshold,
            )
        )

        return {
            "message": "Spatial proximity classified.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Proximity classification failed: {exc}",
        )


@router.post("/query")
async def query_spatial_relations(
    request: SpatialQueryRequest,
):
    try:
        result = (
            spatial_reasoning_engine.query_relations(
                entity_name=request.entity_name,
                relation=request.relation,
            )
        )

        return {
            "message": "Spatial relation query completed.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Spatial query failed: {exc}",
        )


@router.get("/relations")
async def get_all_spatial_relations():
    try:
        result = (
            spatial_reasoning_engine.get_all_relations()
        )

        return {
            "message": "Spatial relations retrieved successfully.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve spatial relations: {exc}",
        )


@router.get("/result")
async def get_last_spatial_result():
    result = (
        spatial_reasoning_engine.get_last_result()
    )

    if result is None:
        return {
            "message": "No spatial reasoning result available.",
            "result": None,
        }

    return {
        "message": "Latest spatial reasoning result retrieved.",
        "result": result,
    }