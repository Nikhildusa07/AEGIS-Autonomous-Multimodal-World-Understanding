from typing import Any, Dict, List
from uuid import uuid4

from app.models.world_state import (
    BoundingBox,
    DetectedObject,
    Observation,
)


class PerceptionEngine:
    """
    AEGIS perception layer.

    Converts raw multimodal observations into
    structured perception results.
    """

    def __init__(self):
        self.last_results: Dict[str, Any] = {}

    def process_observation(
        self,
        observation: Observation,
    ) -> Dict[str, Any]:
        """
        Process one observation according to its modality.
        """

        modality = observation.modality.lower()

        if modality == "image":
            result = self.process_image(observation)

        elif modality == "video":
            result = self.process_video(observation)

        elif modality == "audio":
            result = self.process_audio(observation)

        elif modality == "document":
            result = self.process_document(observation)

        elif modality == "text":
            result = self.process_text(observation)

        elif modality == "sensor":
            result = self.process_sensor(observation)

        else:
            result = {
                "status": "unsupported",
                "modality": modality,
            }

        self.last_results[observation.observation_id] = result

        return result

    def process_image(
        self,
        observation: Observation,
    ) -> Dict[str, Any]:
        """
        Process image observations.

        Object detection and OCR model integration
        will be added in later steps.
        """

        metadata = observation.metadata

        detected_objects = self._extract_objects(
            metadata.get("objects", [])
        )

        extracted_text = metadata.get(
            "ocr_text",
            "",
        )

        scene = metadata.get(
            "scene",
            "unknown",
        )

        return {
            "observation_id": observation.observation_id,
            "modality": "image",
            "scene": scene,
            "objects": detected_objects,
            "ocr_text": extracted_text,
            "confidence": observation.confidence,
            "status": "processed",
        }

    def process_video(
        self,
        observation: Observation,
    ) -> Dict[str, Any]:
        """
        Process video observations.

        Temporal reasoning and actual video models
        will be added later.
        """

        metadata = observation.metadata

        events = metadata.get(
            "events",
            [],
        )

        return {
            "observation_id": observation.observation_id,
            "modality": "video",
            "events": events,
            "frame_count": metadata.get(
                "frame_count",
                0,
            ),
            "duration_seconds": metadata.get(
                "duration_seconds",
                0,
            ),
            "confidence": observation.confidence,
            "status": "processed",
        }

    def process_audio(
        self,
        observation: Observation,
    ) -> Dict[str, Any]:
        """
        Process audio observations.

        Speech recognition will be connected later.
        """

        transcript = observation.metadata.get(
            "transcript",
            "",
        )

        return {
            "observation_id": observation.observation_id,
            "modality": "audio",
            "transcript": transcript,
            "confidence": observation.confidence,
            "status": "processed",
        }

    def process_document(
        self,
        observation: Observation,
    ) -> Dict[str, Any]:
        """
        Process document observations.

        Document extraction and advanced OCR will
        be connected later.
        """

        text = observation.metadata.get(
            "text",
            "",
        )

        return {
            "observation_id": observation.observation_id,
            "modality": "document",
            "text": text,
            "confidence": observation.confidence,
            "status": "processed",
        }

    def process_text(
        self,
        observation: Observation,
    ) -> Dict[str, Any]:
        """
        Process text observations.
        """

        text = observation.content or observation.metadata.get(
            "text",
            "",
        )

        return {
            "observation_id": observation.observation_id,
            "modality": "text",
            "text": text,
            "confidence": observation.confidence,
            "status": "processed",
        }

    def process_sensor(
        self,
        observation: Observation,
    ) -> Dict[str, Any]:
        """
        Process sensor observations.
        """

        return {
            "observation_id": observation.observation_id,
            "modality": "sensor",
            "sensor_name": observation.metadata.get(
                "sensor_name",
                "unknown",
            ),
            "value": observation.metadata.get(
                "value"
            ),
            "unit": observation.metadata.get(
                "unit",
                "",
            ),
            "confidence": observation.confidence,
            "status": "processed",
        }

    def _extract_objects(
        self,
        objects: List[Any],
    ) -> List[Dict[str, Any]]:
        """
        Convert raw detected-object data into a
        standardized structure.
        """

        results = []

        for item in objects:

            if isinstance(item, str):
                results.append(
                    {
                        "object_id": str(uuid4()),
                        "label": item,
                        "confidence": 0.0,
                    }
                )
                continue

            if not isinstance(item, dict):
                continue

            bounding_box_data = item.get(
                "bounding_box"
            )

            bounding_box = None

            if bounding_box_data:
                bounding_box = BoundingBox(
                    x=float(
                        bounding_box_data.get(
                            "x",
                            0,
                        )
                    ),
                    y=float(
                        bounding_box_data.get(
                            "y",
                            0,
                        )
                    ),
                    width=float(
                        bounding_box_data.get(
                            "width",
                            0,
                        )
                    ),
                    height=float(
                        bounding_box_data.get(
                            "height",
                            0,
                        )
                    ),
                )

            detected_object = DetectedObject(
                object_id=str(uuid4()),
                label=item.get(
                    "label",
                    "unknown",
                ),
                confidence=float(
                    item.get(
                        "confidence",
                        0.0,
                    )
                ),
                bounding_box=bounding_box,
                attributes=item.get(
                    "attributes",
                    {},
                ),
            )

            results.append(
                detected_object.model_dump()
            )

        return results

    def get_last_result(
        self,
        observation_id: str,
    ) -> Dict[str, Any] | None:
        """
        Return the most recent perception result
        for an observation.
        """

        return self.last_results.get(
            observation_id
        )


perception_engine = PerceptionEngine()