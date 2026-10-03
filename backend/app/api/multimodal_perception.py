from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.perception.object_detection_engine import (
    object_detection_engine,
)
from app.perception.ocr_engine import ocr_engine


router = APIRouter(
    prefix="/multimodal-perception",
    tags=["Multimodal Perception"],
)


UPLOAD_DIR = Path("uploads/multimodal")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/bmp",
}


@router.post("/analyze")
async def analyze_image(
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

        with open(
            file_path,
            "wb",
        ) as output_file:
            output_file.write(file_data)

        ocr_result = ocr_engine.extract_text(
            str(file_path)
        )

        detection_result = (
            object_detection_engine.detect_objects(
                str(file_path)
            )
        )

        return {
            "message": (
                "Multimodal image analysis "
                "completed."
            ),
            "result": {
                "filename": file.filename,
                "modality": "image",
                "ocr": ocr_result,
                "object_detection": detection_result,
                "summary": {
                    "text_detected": (
                        ocr_result["character_count"] > 0
                    ),
                    "objects_detected": (
                        detection_result["object_count"]
                    ),
                },
            },
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Multimodal analysis failed: {exc}"
            ),
        )

    finally:
        if file_path.exists():
            file_path.unlink()