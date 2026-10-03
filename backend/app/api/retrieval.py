from pathlib import Path
from uuid import uuid4
from typing import Any, Dict, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.reasoning.retrieval_engine import (
    cross_modal_retrieval_engine,
)


router = APIRouter(
    prefix="/retrieval",
    tags=["Cross-Modal Retrieval"],
)


UPLOAD_DIR = Path("uploads/retrieval")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/bmp",
}


class AddTextRequest(BaseModel):
    text: str = Field(..., min_length=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)


@router.post("/text")
async def add_text_to_index(
    request: AddTextRequest,
):
    try:
        result = cross_modal_retrieval_engine.add_text(
            text=request.text,
            metadata=request.metadata,
        )

        return {
            "message": "Text added to retrieval index.",
            "result": result,
            "index_size": (
                cross_modal_retrieval_engine.get_index_size()
            ),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add text: {exc}",
        )


@router.post("/image")
async def add_image_to_index(
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(default=None),
):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image format. "
                "Use JPEG, PNG, WEBP, or BMP."
            ),
        )

    extension = Path(
        file.filename or ""
    ).suffix.lower()

    if not extension:
        extension = ".png"

    file_name = f"{uuid4()}{extension}"
    file_path = UPLOAD_DIR / file_name

    try:
        file_data = await file.read()

        with open(file_path, "wb") as output_file:
            output_file.write(file_data)

        parsed_metadata: Dict[str, Any] = {}

        if metadata:
            parsed_metadata = {
                "description": metadata,
            }

        result = cross_modal_retrieval_engine.add_image(
            image_path=str(file_path),
            metadata=parsed_metadata,
        )

        return {
            "message": "Image added to retrieval index.",
            "result": result,
            "index_size": (
                cross_modal_retrieval_engine.get_index_size()
            ),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add image: {exc}",
        )

    finally:
        if file_path.exists():
            file_path.unlink()


@router.post("/search")
async def search_retrieval_index(
    request: SearchRequest,
):
    try:
        result = cross_modal_retrieval_engine.search(
            query=request.query,
            top_k=request.top_k,
        )

        return {
            "message": "Cross-modal retrieval completed.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Retrieval failed: {exc}",
        )


@router.get("/index")
async def get_index_information():
    return {
        "status": "success",
        "index_size": (
            cross_modal_retrieval_engine.get_index_size()
        ),
        "message": (
            "Cross-modal retrieval index information "
            "retrieved successfully."
        ),
    }


@router.get("/result")
async def get_last_retrieval_result():
    result = (
        cross_modal_retrieval_engine.get_last_result()
    )

    if result is None:
        return {
            "message": "No retrieval result available.",
            "result": None,
        }

    return {
        "message": "Latest retrieval result retrieved.",
        "result": result,
    }