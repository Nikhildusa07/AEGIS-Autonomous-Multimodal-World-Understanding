from typing import Any, Dict, List
from uuid import uuid4

import numpy as np

from app.reasoning.embedding_engine import (
    multimodal_embedding_engine,
)


class CrossModalRetrievalEngine:
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.last_result: Dict[str, Any] | None = None

    def add_text(
        self,
        text: str,
        metadata: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        embedding = (
            multimodal_embedding_engine.encode_text(text)
        )

        item = {
            "id": str(uuid4()),
            "modality": "text",
            "content": text,
            "embedding": embedding,
            "metadata": metadata or {},
        }

        self.documents.append(item)

        return {
            "status": "success",
            "id": item["id"],
            "modality": "text",
            "message": "Text added to retrieval index.",
        }

    def add_image(
        self,
        image_path: str,
        metadata: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:

        embedding = (
            multimodal_embedding_engine.encode_image(
                image_path
            )
        )

        item = {
            "id": str(uuid4()),
            "modality": "image",
            "content": image_path,
            "embedding": embedding,
            "metadata": metadata or {},
        }

        self.documents.append(item)

        return {
            "status": "success",
            "id": item["id"],
            "modality": "image",
            "message": "Image added to retrieval index.",
        }

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        if not self.documents:
            return {
                "status": "success",
                "query": query,
                "result_count": 0,
                "results": [],
            }

        query_embedding = np.array(
            multimodal_embedding_engine.encode_text(query),
            dtype=np.float32,
        )

        results = []

        for document in self.documents:
            document_embedding = np.array(
                document["embedding"],
                dtype=np.float32,
            )

            similarity = float(
                np.dot(
                    query_embedding,
                    document_embedding,
                )
            )

            results.append(
                {
                    "id": document["id"],
                    "modality": document["modality"],
                    "content": document["content"],
                    "similarity": round(similarity, 4),
                    "metadata": document["metadata"],
                }
            )

        results.sort(
            key=lambda item: item["similarity"],
            reverse=True,
        )

        results = results[:max(1, top_k)]

        result = {
            "status": "success",
            "query": query,
            "result_count": len(results),
            "results": results,
        }

        self.last_result = result

        return result

    def get_index_size(self) -> int:
        return len(self.documents)

    def get_last_result(self):
        return self.last_result


cross_modal_retrieval_engine = CrossModalRetrievalEngine()