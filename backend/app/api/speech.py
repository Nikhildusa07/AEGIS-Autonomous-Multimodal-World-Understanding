from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.perception.speech_engine import speech_engine


router = APIRouter(
    prefix="/speech",
    tags=["Speech Understanding"],
)


UPLOAD_DIR = Path("uploads/speech")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


ALLOWED_AUDIO_TYPES = {
    "audio/mpeg",
    "audio/wav",
    "audio/x-wav",
    "audio/mp4",
    "audio/x-m4a",
    "audio/ogg",
    "audio/webm",
}


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
):
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported audio format. "
                "Use MP3, WAV, M4A, OGG, or WEBM."
            ),
        )

    extension = Path(
        file.filename or ""
    ).suffix.lower()

    if not extension:
        extension = ".wav"

    file_name = f"{uuid4()}{extension}"
    file_path = UPLOAD_DIR / file_name

    try:
        file_data = await file.read()

        with open(
            file_path,
            "wb",
        ) as output_file:
            output_file.write(file_data)

        result = speech_engine.transcribe(
            str(file_path)
        )

        return {
            "message": (
                "Speech transcription completed."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Speech transcription failed: {exc}"
            ),
        )

    finally:
        if file_path.exists():
            file_path.unlink()