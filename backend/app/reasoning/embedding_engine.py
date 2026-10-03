from pathlib import Path
from typing import Any, Dict, List
import hashlib


class MultimodalEmbeddingEngine:
    def __init__(self):
        self.model_name = "AEGIS-Lightweight-Embedding"
        self.embedding_dimension = 128
        self.model = None
        self.last_result: Dict[str, Any] | None = None

    def _generate_embedding(self, value: str) -> List[float]:
        """
        Generate a deterministic lightweight embedding without
        requiring sentence-transformers or large ML models.
        """

        if not value or not value.strip():
            raise ValueError("Input cannot be empty.")

        embedding: List[float] = []

        for index in range(self.embedding_dimension):
            digest = hashlib.sha256(
                f"{index}:{value}".encode("utf-8")
            ).digest()

            number = int.from_bytes(
                digest[:4],
                byteorder="big",
                signed=False,
            )

            normalized = (number / 4294967295.0) * 2.0 - 1.0
            embedding.append(round(normalized, 6))

        magnitude = sum(
            value * value for value in embedding
        ) ** 0.5

        if magnitude > 0:
            embedding = [
                round(value / magnitude, 6)
                for value in embedding
            ]

        return embedding

    def encode_text(self, text: str) -> List[float]:
        return self._generate_embedding(text)

    def encode_image(self, image_path: str) -> List[float]:
        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Image file not found: {image_path}"
            )

        try:
            from PIL import Image

            image = Image.open(path).convert("RGB")

            image_data = image.resize(
                (32, 32)
            ).tobytes()

            image_hash = hashlib.sha256(
                image_data
            ).hexdigest()

            return self._generate_embedding(image_hash)

        except Exception as exc:
            raise RuntimeError(
                f"Unable to process image: {exc}"
            ) from exc

    def create_text_embedding(
        self,
        text: str,
    ) -> Dict[str, Any]:

        embedding = self.encode_text(text)

        result = {
            "status": "success",
            "modality": "text",
            "model": self.model_name,
            "dimension": len(embedding),
            "embedding": embedding,
        }

        self.last_result = result

        return result

    def create_image_embedding(
        self,
        image_path: str,
    ) -> Dict[str, Any]:

        embedding = self.encode_image(image_path)

        result = {
            "status": "success",
            "modality": "image",
            "filename": Path(image_path).name,
            "model": self.model_name,
            "dimension": len(embedding),
            "embedding": embedding,
        }

        self.last_result = result

        return result

    def get_last_result(self):
        return self.last_result


multimodal_embedding_engine = MultimodalEmbeddingEngine()