from typing import Any, Dict, List


class SceneUnderstandingEngine:
    def __init__(self):
        self.last_result: Dict[str, Any] | None = None

    def analyze_scene(
        self,
        objects: List[Dict[str, Any]] | None = None,
        ocr_text: str = "",
        audio_transcript: str = "",
        environment: str = "unknown",
        location: str | None = None,
    ) -> Dict[str, Any]:

        objects = objects or []

        object_labels = [
            obj.get("label", "unknown")
            for obj in objects
            if isinstance(obj, dict)
        ]

        unique_objects = sorted(
            set(object_labels)
        )

        scene_description_parts = []

        if environment != "unknown":
            scene_description_parts.append(
                f"The environment is {environment}."
            )

        if location:
            scene_description_parts.append(
                f"The current location is {location}."
            )

        if unique_objects:
            scene_description_parts.append(
                "Detected objects include: "
                + ", ".join(unique_objects)
                + "."
            )

        if ocr_text.strip():
            scene_description_parts.append(
                "Text was detected in the scene."
            )

        if audio_transcript.strip():
            scene_description_parts.append(
                "Audio information is available."
            )

        if not scene_description_parts:
            scene_description_parts.append(
                "Insufficient information to describe the scene."
            )

        result = {
            "status": "success",
            "environment": environment,
            "location": location,
            "object_count": len(objects),
            "unique_objects": unique_objects,
            "ocr_available": bool(
                ocr_text.strip()
            ),
            "audio_available": bool(
                audio_transcript.strip()
            ),
            "scene_description": " ".join(
                scene_description_parts
            ),
        }

        self.last_result = result

        return result

    def get_last_result(self):
        return self.last_result


scene_understanding_engine = SceneUnderstandingEngine()