from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.perception.video_engine import video_engine


router = APIRouter(
    prefix="/video",
    tags=["Video Understanding"],
)


UPLOAD_DIR = Path("uploads/video")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


ALLOWED_VIDEO_TYPES = {
    "video/mp4",
    "video/avi",
    "video/x-msvideo",
    "video/mov",
    "video/quicktime",
    "video/webm",
    "video/mkv",
    "video/x-matroska",
}


@router.post("/analyze")
async def analyze_video(
    file: UploadFile = File(...),
):
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported video format. "
                "Use MP4, AVI, MOV, WEBM, or MKV."
            ),
        )

    extension = Path(
        file.filename or ""
    ).suffix.lower()

    if not extension:
        extension = ".mp4"

    file_name = f"{uuid4()}{extension}"
    file_path = UPLOAD_DIR / file_name

    try:
        file_data = await file.read()

        with open(
            file_path,
            "wb",
        ) as output_file:
            output_file.write(file_data)

        result = video_engine.analyze_video(
            str(file_path)
        )

        return {
            "message": (
                "Video understanding completed."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Video analysis failed: {exc}"
            ),
        )

    finally:
        if file_path.exists():
            file_path.unlink()