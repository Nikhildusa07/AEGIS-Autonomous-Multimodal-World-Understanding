from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4


class UncertaintyEstimationEngine:
    def __init__(self):
        self.estimation_history: List[Dict[str, Any]] = []
        self.last_result: Optional[Dict[str, Any]] = None

    def estimate(
        self,
        perception_confidence: float = 1.0,
        sensor_confidence: float = 1.0,
        event_confidence: float = 1.0,
        action_confidence: float = 1.0,
        verification_confidence: float = 1.0,
        world_state_confidence: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        confidences = {
            "perception": self._clamp(perception_confidence),
            "sensor": self._clamp(sensor_confidence),
            "event": self._clamp(event_confidence),
            "action": self._clamp(action_confidence),
            "verification": self._clamp(
                verification_confidence
            ),
        }

        if world_state_confidence is not None:
            confidences["world_state"] = self._clamp(
                world_state_confidence
            )

        overall_confidence = (
            sum(confidences.values())
            / len(confidences)
        )

        uncertainty = 1.0 - overall_confidence

        if uncertainty < 0.20:
            uncertainty_level = "low"
        elif uncertainty < 0.50:
            uncertainty_level = "medium"
        elif uncertainty < 0.75:
            uncertainty_level = "high"
        else:
            uncertainty_level = "critical"

        requires_attention = uncertainty >= 0.50

        weakest_source = min(
            confidences,
            key=confidences.get,
        )

        result = {
            "uncertainty_id": str(uuid4()),
            "overall_confidence": round(
                overall_confidence,
                4,
            ),
            "uncertainty_score": round(
                uncertainty,
                4,
            ),
            "uncertainty_level": uncertainty_level,
            "requires_attention": requires_attention,
            "confidence_sources": confidences,
            "weakest_source": weakest_source,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow(),
        }

        self.estimation_history.append(result)
        self.last_result = result

        return {
            "status": "success",
            "estimation": result,
            "message": (
                "Uncertainty estimation completed."
            ),
        }

    def estimate_from_world_state(
        self,
        world_state: Dict[str, Any],
    ) -> Dict[str, Any]:

        if not isinstance(world_state, dict):
            raise ValueError(
                "World state must be a dictionary."
            )

        perception_confidences = []
        sensor_confidences = []
        event_confidences = []
        action_confidences = []
        verification_confidences = []

        for obj in world_state.get(
            "detected_objects",
            [],
        ):
            if isinstance(obj, dict):
                perception_confidences.append(
                    self._clamp(
                        obj.get(
                            "confidence",
                            0.0,
                        )
                    )
                )

        for sensor in world_state.get(
            "sensor_readings",
            [],
        ):
            if isinstance(sensor, dict):
                sensor_confidences.append(
                    self._clamp(
                        sensor.get(
                            "confidence",
                            0.0,
                        )
                    )
                )

        for event in world_state.get(
            "detected_events",
            [],
        ):
            if isinstance(event, dict):
                event_confidences.append(
                    self._clamp(
                        event.get(
                            "confidence",
                            0.0,
                        )
                    )
                )

        for action in world_state.get(
            "planned_actions",
            [],
        ):
            if isinstance(action, dict):
                action_confidences.append(
                    self._clamp(
                        action.get(
                            "confidence",
                            0.0,
                        )
                    )
                )

        for result in world_state.get(
            "action_results",
            [],
        ):
            if isinstance(result, dict):
                verification_confidences.append(
                    self._clamp(
                        result.get(
                            "verification_confidence",
                            0.0,
                        )
                    )
                )

        perception_confidence = self._average_or_default(
            perception_confidences
        )

        sensor_confidence = self._average_or_default(
            sensor_confidences
        )

        event_confidence = self._average_or_default(
            event_confidences
        )

        action_confidence = self._average_or_default(
            action_confidences
        )

        verification_confidence = (
            self._average_or_default(
                verification_confidences
            )
        )

        return self.estimate(
            perception_confidence=perception_confidence,
            sensor_confidence=sensor_confidence,
            event_confidence=event_confidence,
            action_confidence=action_confidence,
            verification_confidence=(
                verification_confidence
            ),
            world_state_confidence=(
                world_state.get(
                    "overall_confidence"
                )
            ),
            metadata={
                "source": "world_state",
                "state_id": world_state.get(
                    "state_id"
                ),
                "environment": world_state.get(
                    "environment"
                ),
                "location": world_state.get(
                    "location"
                ),
            },
        )

    def get_history(self) -> Dict[str, Any]:
        result = {
            "status": "success",
            "estimation_count": len(
                self.estimation_history
            ),
            "estimations": self.estimation_history,
        }

        self.last_result = result

        return result

    def get_last_result(self):
        return self.last_result

    @staticmethod
    def _clamp(value: Any) -> float:
        try:
            value = float(value)
        except (TypeError, ValueError):
            value = 0.0

        return max(
            0.0,
            min(1.0, value),
        )

    @staticmethod
    def _average_or_default(
        values: List[float],
        default: float = 1.0,
    ) -> float:

        if not values:
            return default

        return sum(values) / len(values)


uncertainty_estimation_engine = (
    UncertaintyEstimationEngine()
)