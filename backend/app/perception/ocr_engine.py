from pathlib import Path
from typing import Any, Dict

import pytesseract
from PIL import Image


class OCREngine:
    def __init__(self):
        self.last_result: Dict[str, Any] | None = None

        # Windows Tesseract installation path
        tesseract_path = Path(
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        if tesseract_path.exists():
            pytesseract.pytesseract.tesseract_cmd = str(tesseract_path)

    def extract_text(self, image_path: str) -> Dict[str, Any]:
        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Image file not found: {image_path}"
            )

        try:
            image = Image.open(path)

            text = pytesseract.image_to_string(image).strip()

            result = {
                "status": "success",
                "filename": path.name,
                "text": text,
                "character_count": len(text),
            }

            self.last_result = result
            return result

        except Exception as exc:
            result = {
                "status": "error",
                "filename": path.name,
                "text": "",
                "character_count": 0,
                "error": str(exc),
            }

            self.last_result = result
            return result

    def get_last_result(self):
        return self.last_result


ocr_engine = OCREngine()