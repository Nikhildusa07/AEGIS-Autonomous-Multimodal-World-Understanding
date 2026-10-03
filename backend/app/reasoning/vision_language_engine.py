from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4


class VisionLanguageReasoningEngine:
    """
    Combines visual observations and language context
    to produce a grounded interpretation of the environment.
    """

    def __init__(self):
        self.reasoning_history: List[Dict[str, Any]] = []
        self.last_result: Optional[Dict[str, Any]] = None

    def reason(
        self,
        visual_objects: Optional[List[Dict[str, Any]]] = None,
        visual_scene: Optional[str] = None,
        ocr_text: Optional[str] = None,
        audio_transcript: Optional[str] = None,
        text_context: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        visual_objects = visual_objects or []

        visual_labels = []

        for obj in visual_objects:
            if not isinstance(obj, dict):
                continue

            label = obj.get("label")

            if label:
                visual_labels.append(
                    str(label).strip()
                )

        visual_labels = list(
            dict.fromkeys(visual_labels)
        )

        language_sources = []

        if ocr_text and ocr_text.strip():
            language_sources.append(
                {
                    "source": "ocr",
                    "content": ocr_text.strip(),
                }
            )

        if audio_transcript and audio_transcript.strip():
            language_sources.append(
                {
                    "source": "audio",
                    "content": audio_transcript.strip(),
                }
            )

        if text_context and text_context.strip():
            language_sources.append(
                {
                    "source": "text",
                    "content": text_context.strip(),
                }
            )

        evidence = []

        if visual_labels:
            evidence.append(
                {
                    "type": "visual",
                    "content": visual_labels,
                }
            )

        if visual_scene and visual_scene.strip():
            evidence.append(
                {
                    "type": "scene",
                    "content": visual_scene.strip(),
                }
            )

        evidence.extend(language_sources)

        grounded_matches = []

        combined_language = " ".join(
            item["content"].lower()
            for item in language_sources
        )

        for label in visual_labels:
            normalized_label = label.lower()

            if normalized_label in combined_language:
                grounded_matches.append(
                    {
                        "visual_object": label,
                        "supporting_language": True,
                        "reason": (
                            "Visual object is explicitly "
                            "supported by language context."
                        ),
                    }
                )

        if visual_scene:
            scene_words = set(
                visual_scene.lower().split()
            )

            for label in visual_labels:
                if label.lower() in scene_words:
                    grounded_matches.append(
                        {
                            "visual_object": label,
                            "supporting_scene": True,
                            "reason": (
                                "Visual object is supported "
                                "by the scene description."
                            ),
                        }
                    )

        unique_matches = []
        seen = set()

        for match in grounded_matches:
            key = match["visual_object"].lower()

            if key not in seen:
                seen.add(key)
                unique_matches.append(match)

        if visual_labels and language_sources:
            modality_alignment = min(
                1.0,
                0.5
                + (
                    len(unique_matches)
                    / max(len(visual_labels), 1)
                )
                * 0.5,
            )
        elif visual_labels or language_sources:
            modality_alignment = 0.5
        else:
            modality_alignment = 0.0

        evidence_count = len(evidence)

        if evidence_count >= 4:
            grounding_confidence = 0.95
        elif evidence_count == 3:
            grounding_confidence = 0.90
        elif evidence_count == 2:
            grounding_confidence = 0.80
        elif evidence_count == 1:
            grounding_confidence = 0.65
        else:
            grounding_confidence = 0.20

        overall_confidence = (
            grounding_confidence
            * 0.6
            + modality_alignment
            * 0.4
        )

        overall_confidence = round(
            max(
                0.0,
                min(
                    1.0,
                    overall_confidence,
                ),
            ),
            4,
        )

        if visual_labels and language_sources:
            interpretation = (
                "The environment contains "
                f"{', '.join(visual_labels)}. "
                "Language context was combined with "
                "visual evidence to ground the "
                "interpretation."
            )
        elif visual_labels:
            interpretation = (
                "The visual system detected "
                f"{', '.join(visual_labels)}, "
                "but no language context was available."
            )
        elif language_sources:
            interpretation = (
                "Language information was available, "
                "but no visual objects were detected."
            )
        else:
            interpretation = (
                "Insufficient multimodal evidence "
                "for a grounded interpretation."
            )

        reasoning = {
            "reasoning_id": str(uuid4()),
            "interpretation": interpretation,
            "visual_objects": visual_labels,
            "language_sources": language_sources,
            "grounded_matches": unique_matches,
            "evidence_count": evidence_count,
            "modality_alignment": round(
                modality_alignment,
                4,
            ),
            "grounding_confidence": round(
                grounding_confidence,
                4,
            ),
            "overall_confidence": overall_confidence,
            "timestamp": datetime.utcnow(),
            "metadata": metadata or {},
        }

        self.reasoning_history.append(
            reasoning
        )

        self.last_result = reasoning

        return {
            "status": "success",
            "reasoning": reasoning,
            "message": (
                "Vision-language reasoning "
                "completed."
            ),
        }

    def reason_from_observation(
        self,
        observation: Dict[str, Any],
    ) -> Dict[str, Any]:

        if not isinstance(observation, dict):
            raise ValueError(
                "Observation must be a dictionary."
            )

        return self.reason(
            visual_objects=observation.get(
                "detected_objects",
                [],
            ),
            visual_scene=observation.get(
                "scene_description"
            ),
            ocr_text=observation.get(
                "ocr_text"
            ),
            audio_transcript=observation.get(
                "audio_transcript"
            ),
            text_context=observation.get(
                "text_context"
            ),
            metadata={
                "source": "observation",
                "observation_id": observation.get(
                    "observation_id"
                ),
            },
        )

    def get_history(self) -> Dict[str, Any]:

        result = {
            "status": "success",
            "reasoning_count": len(
                self.reasoning_history
            ),
            "reasoning_history": (
                self.reasoning_history
            ),
        }

        self.last_result = result

        return result

    def get_last_result(self):

        return self.last_result


vision_language_reasoning_engine = (
    VisionLanguageReasoningEngine()
)