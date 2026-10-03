from pathlib import Path
from typing import Any, Dict, List

from PIL import Image
from sentence_transformers import SentenceTransformer


class MultimodalEmbeddingEngine:
    def __init__(self):
        self.model_name = "clip-ViT-B-32"
        self.model = SentenceTransformer(self.model_name)
        self.last_result: Dict[str, Any] | None = None

    def encode_text(self, text: str) -> List[float]:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def encode_image(self, image_path: str) -> List[float]:
        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Image file not found: {image_path}"
            )

        image = Image.open(path).convert("RGB")

        embedding = self.model.encode(
            image,
            normalize_embeddings=True,
        )

        return embedding.tolist()

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