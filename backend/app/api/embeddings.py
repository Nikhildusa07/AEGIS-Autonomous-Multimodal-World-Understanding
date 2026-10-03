from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.reasoning.embedding_engine import (
    multimodal_embedding_engine,
)


router = APIRouter(
    prefix="/embeddings",
    tags=["Multimodal Embeddings"],
)


UPLOAD_DIR = Path("uploads/embeddings")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/bmp",
}


class TextEmbeddingRequest(BaseModel):
    text: str = Field(..., min_length=1)


@router.post("/text")
async def create_text_embedding(
    request: TextEmbeddingRequest,
):
    try:
        result = (
            multimodal_embedding_engine.create_text_embedding(
                request.text
            )
        )

        return {
            "message": "Text embedding generated successfully.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Text embedding failed: {exc}",
        )


@router.post("/image")
async def create_image_embedding(
    file: UploadFile = File(...),
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

        result = (
            multimodal_embedding_engine.create_image_embedding(
                str(file_path)
            )
        )

        return {
            "message": "Image embedding generated successfully.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Image embedding failed: {exc}",
        )

    finally:
        if file_path.exists():
            file_path.unlink()


@router.get("/result")
async def get_last_embedding_result():
    result = (
        multimodal_embedding_engine.get_last_result()
    )

    if result is None:
        return {
            "message": "No embedding result available.",
            "result": None,
        }

    return {
        "message": "Latest embedding result retrieved.",
        "result": result,
    }