from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.reasoning.knowledge_engine import (
    knowledge_representation_engine,
)


router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Representation"],
)


class EntityRequest(BaseModel):
    name: str = Field(..., min_length=1)
    entity_type: str = "unknown"
    attributes: Dict[str, Any] = Field(
        default_factory=dict
    )


class RelationRequest(BaseModel):
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


class KnowledgeQueryRequest(BaseModel):
    entity_name: Optional[str] = None
    relation: Optional[str] = None


@router.post("/entity")
async def add_entity(
    request: EntityRequest,
):
    try:
        result = knowledge_representation_engine.add_entity(
            name=request.name,
            entity_type=request.entity_type,
            attributes=request.attributes,
        )

        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add entity: {exc}",
        )


@router.post("/relation")
async def add_relation(
    request: RelationRequest,
):
    try:
        result = knowledge_representation_engine.add_relation(
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
            detail=f"Failed to add relation: {exc}",
        )


@router.post("/query")
async def query_knowledge(
    request: KnowledgeQueryRequest,
):
    try:
        result = knowledge_representation_engine.query(
            entity_name=request.entity_name,
            relation=request.relation,
        )

        return {
            "message": "Knowledge query completed.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Knowledge query failed: {exc}",
        )


@router.get("/graph")
async def get_knowledge_graph():
    try:
        result = (
            knowledge_representation_engine
            .get_knowledge_graph()
        )

        return {
            "message": "Knowledge graph retrieved successfully.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve knowledge graph: {exc}",
        )


@router.get("/entity/{entity_name}")
async def get_entity_relations(
    entity_name: str,
):
    try:
        relations = (
            knowledge_representation_engine
            .get_entity_relations(entity_name)
        )

        return {
            "status": "success",
            "entity": entity_name,
            "relation_count": len(relations),
            "relations": relations,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve entity relations: {exc}",
        )


@router.get("/result")
async def get_last_knowledge_result():
    result = (
        knowledge_representation_engine
        .get_last_result()
    )

    if result is None:
        return {
            "message": "No knowledge result available.",
            "result": None,
        }

    return {
        "message": "Latest knowledge result retrieved.",
        "result": result,
    }