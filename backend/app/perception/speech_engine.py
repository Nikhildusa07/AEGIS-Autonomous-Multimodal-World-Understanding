from pathlib import Path
from typing import Any, Dict

from faster_whisper import WhisperModel


class SpeechEngine:
    def __init__(self):
        self.model = WhisperModel(
            "tiny",
            device="cpu",
            compute_type="int8",
        )

        self.last_result: Dict[str, Any] | None = None

    def transcribe(
        self,
        audio_path: str,
    ) -> Dict[str, Any]:

        path = Path(audio_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        try:
            segments, info = self.model.transcribe(
                str(path),
                beam_size=5,
            )

            text_parts = []

            for segment in segments:
                text_parts.append(
                    segment.text.strip()
                )

            text = " ".join(
                part for part in text_parts if part
            ).strip()

            result = {
                "status": "success",
                "filename": path.name,
                "text": text,
                "language": info.language,
                "language_probability": round(
                    info.language_probability,
                    4,
                ),
                "character_count": len(text),
            }

            self.last_result = result

            return result

        except Exception as exc:
            result = {
                "status": "error",
                "filename": path.name,
                "text": "",
                "language": None,
                "language_probability": 0.0,
                "character_count": 0,
                "error": str(exc),
            }

            self.last_result = result

            return result

    def get_last_result(self):
        return self.last_result


speech_engine = SpeechEngine()