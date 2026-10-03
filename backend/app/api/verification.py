from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.environment.action_verifier import (
    action_verification_engine,
)


router = APIRouter(
    prefix="/verification",
    tags=["Action Verification"],
)


class VerifyActionRequest(BaseModel):
    action_id: str = Field(..., min_length=1)
    action_type: str = Field(..., min_length=1)
    execution_status: str = Field(..., min_length=1)
    execution_success: bool
    expected_outcome: Optional[str] = None
    actual_outcome: Optional[str] = None
    verification_confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )


class VerifyExecutionRequest(BaseModel):
    execution: Dict[str, Any]
    expected_outcome: Optional[str] = None
    actual_outcome: Optional[str] = None


class ConfidenceVerificationRequest(BaseModel):
    action_id: str = Field(..., min_length=1)
    action_type: str = Field(..., min_length=1)
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )
    minimum_confidence: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
    )


@router.post("/action")
async def verify_action(
    request: VerifyActionRequest,
):
    try:
        result = (
            action_verification_engine
            .verify_action(
                action_id=request.action_id,
                action_type=request.action_type,
                execution_status=(
                    request.execution_status
                ),
                execution_success=(
                    request.execution_success
                ),
                expected_outcome=(
                    request.expected_outcome
                ),
                actual_outcome=(
                    request.actual_outcome
                ),
                verification_confidence=(
                    request.verification_confidence
                ),
                metadata=request.metadata,
            )
        )

        return {
            "message": (
                "Action verification completed successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Action verification failed: {exc}"
            ),
        )


@router.post("/execution")
async def verify_execution(
    request: VerifyExecutionRequest,
):
    try:
        result = (
            action_verification_engine
            .verify_execution(
                execution=request.execution,
                expected_outcome=(
                    request.expected_outcome
                ),
                actual_outcome=(
                    request.actual_outcome
                ),
            )
        )

        return {
            "message": (
                "Execution verification completed successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Execution verification failed: {exc}"
            ),
        )


@router.post("/confidence")
async def verify_by_confidence(
    request: ConfidenceVerificationRequest,
):
    try:
        result = (
            action_verification_engine
            .verify_by_confidence(
                action_id=request.action_id,
                action_type=request.action_type,
                confidence=request.confidence,
                minimum_confidence=(
                    request.minimum_confidence
                ),
            )
        )

        return {
            "message": (
                "Confidence-based verification completed successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Confidence verification failed: {exc}"
            ),
        )


@router.get("/history")
async def get_verification_history():
    try:
        result = (
            action_verification_engine
            .get_verification_history()
        )

        return {
            "message": (
                "Verification history retrieved successfully."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to retrieve verification history: {exc}"
            ),
        )


@router.get("/result")
async def get_last_verification_result():
    result = (
        action_verification_engine
        .get_last_result()
    )

    if result is None:
        return {
            "message": (
                "No action verification result available."
            ),
            "result": None,
        }

    return {
        "message": (
            "Latest action verification result retrieved."
        ),
        "result": result,
    }