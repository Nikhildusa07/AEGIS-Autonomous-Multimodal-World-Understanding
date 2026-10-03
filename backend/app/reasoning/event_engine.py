from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4


class EventDetectionEngine:
    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        self.previous_objects: set[str] = set()
        self.last_result: Optional[Dict[str, Any]] = None

    def detect_object_events(
        self,
        current_objects: List[Dict[str, Any]],
        timestamp: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        timestamp = timestamp or datetime.utcnow()

        current_labels = {
            str(
                obj.get("label", "unknown")
            ).strip().lower()
            for obj in current_objects
            if isinstance(obj, dict)
        }

        appeared = sorted(
            current_labels - self.previous_objects
        )

        disappeared = sorted(
            self.previous_objects - current_labels
        )

        detected_events = []

        for label in appeared:
            detected_events.append(
                self._create_event(
                    event_type="object_appeared",
                    description=(
                        f"Object '{label}' appeared "
                        "in the observed environment."
                    ),
                    confidence=0.9,
                    timestamp=timestamp,
                    metadata={
                        "object": label,
                    },
                )
            )

        for label in disappeared:
            detected_events.append(
                self._create_event(
                    event_type="object_disappeared",
                    description=(
                        f"Object '{label}' disappeared "
                        "from the observed environment."
                    ),
                    confidence=0.9,
                    timestamp=timestamp,
                    metadata={
                        "object": label,
                    },
                )
            )

        self.previous_objects = current_labels

        result = {
            "status": "success",
            "timestamp": timestamp,
            "appeared": appeared,
            "disappeared": disappeared,
            "event_count": len(detected_events),
            "events": detected_events,
        }

        self.last_result = result

        return result

    def detect_presence_event(
        self,
        entity: str,
        present: bool,
        confidence: float = 1.0,
        timestamp: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        timestamp = timestamp or datetime.utcnow()

        if not entity or not entity.strip():
            raise ValueError(
                "Entity cannot be empty."
            )

        confidence = max(
            0.0,
            min(1.0, confidence),
        )

        if present:
            event_type = "entity_present"
            description = (
                f"Entity '{entity}' is present "
                "in the environment."
            )
        else:
            event_type = "entity_absent"
            description = (
                f"Entity '{entity}' is absent "
                "from the environment."
            )

        event = self._create_event(
            event_type=event_type,
            description=description,
            confidence=confidence,
            timestamp=timestamp,
            metadata={
                "entity": entity,
                "present": present,
            },
        )

        result = {
            "status": "success",
            "event_count": 1,
            "events": [event],
        }

        self.last_result = result

        return result

    def detect_threshold_event(
        self,
        sensor_name: str,
        value: float,
        threshold: float,
        operator: str = "greater_than",
        confidence: float = 1.0,
        timestamp: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        timestamp = timestamp or datetime.utcnow()

        valid_operators = {
            "greater_than",
            "less_than",
            "greater_equal",
            "less_equal",
            "equal",
        }

        if operator not in valid_operators:
            raise ValueError(
                "Unsupported operator. Use one of: "
                "greater_than, less_than, "
                "greater_equal, less_equal, equal."
            )

        triggered = False

        if operator == "greater_than":
            triggered = value > threshold

        elif operator == "less_than":
            triggered = value < threshold

        elif operator == "greater_equal":
            triggered = value >= threshold

        elif operator == "less_equal":
            triggered = value <= threshold

        elif operator == "equal":
            triggered = value == threshold

        events = []

        if triggered:
            event = self._create_event(
                event_type="threshold_exceeded",
                description=(
                    f"Sensor '{sensor_name}' triggered "
                    f"a threshold condition: "
                    f"{value} {operator} {threshold}."
                ),
                confidence=max(
                    0.0,
                    min(1.0, confidence),
                ),
                timestamp=timestamp,
                severity="high",
                metadata={
                    "sensor_name": sensor_name,
                    "value": value,
                    "threshold": threshold,
                    "operator": operator,
                },
            )

            events.append(event)

        result = {
            "status": "success",
            "triggered": triggered,
            "event_count": len(events),
            "events": events,
        }

        self.last_result = result

        return result

    def add_custom_event(
        self,
        event_type: str,
        description: str,
        confidence: float = 1.0,
        severity: str = "normal",
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        timestamp = timestamp or datetime.utcnow()

        if not event_type.strip():
            raise ValueError(
                "Event type cannot be empty."
            )

        if not description.strip():
            raise ValueError(
                "Event description cannot be empty."
            )

        event = self._create_event(
            event_type=event_type,
            description=description,
            confidence=confidence,
            timestamp=timestamp,
            severity=severity,
            metadata=metadata,
        )

        result = {
            "status": "success",
            "event_count": 1,
            "events": [event],
        }

        self.last_result = result

        return result

    def get_all_events(self) -> Dict[str, Any]:
        result = {
            "status": "success",
            "event_count": len(self.events),
            "events": self.events,
        }

        self.last_result = result

        return result

    def get_last_result(self):
        return self.last_result

    def _create_event(
        self,
        event_type: str,
        description: str,
        confidence: float,
        timestamp: datetime,
        severity: str = "normal",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        event = {
            "event_id": str(uuid4()),
            "event_type": event_type,
            "description": description,
            "confidence": max(
                0.0,
                min(1.0, confidence),
            ),
            "timestamp": timestamp,
            "severity": severity,
            "metadata": metadata or {},
        }

        self.events.append(event)

        return event


event_detection_engine = EventDetectionEngine()