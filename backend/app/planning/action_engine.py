from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4


class ActionPlanningEngine:
    def __init__(self):
        self.planned_actions: List[Dict[str, Any]] = []
        self.last_result: Optional[Dict[str, Any]] = None

    def create_action(
        self,
        action_type: str,
        description: str,
        target: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        confidence: float = 1.0,
        priority: str = "normal",
    ) -> Dict[str, Any]:

        if not action_type.strip():
            raise ValueError(
                "Action type cannot be empty."
            )

        if not description.strip():
            raise ValueError(
                "Action description cannot be empty."
            )

        confidence = max(
            0.0,
            min(1.0, confidence),
        )

        action = {
            "action_id": str(uuid4()),
            "action_type": action_type.strip(),
            "description": description.strip(),
            "target": target,
            "parameters": parameters or {},
            "confidence": confidence,
            "priority": priority.lower(),
            "status": "planned",
            "created_at": datetime.utcnow(),
        }

        self.planned_actions.append(action)

        result = {
            "status": "success",
            "action": action,
            "message": "Action planned successfully.",
        }

        self.last_result = result

        return result

    def plan_from_event(
        self,
        event_type: str,
        description: str,
        severity: str = "normal",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        event_type = event_type.strip().lower()
        severity = severity.strip().lower()
        metadata = metadata or {}

        action_type = "observe"
        action_description = (
            "Continue observing the environment."
        )
        priority = "normal"
        target = None
        parameters: Dict[str, Any] = {}

        if event_type == "obstacle_detected":

            action_type = "avoid_obstacle"

            action_description = (
                "Avoid the detected obstacle "
                "and select a safe path."
            )

            priority = "high"
            target = "safe_path"

            obstacle_distance = self._extract_obstacle_distance(
                metadata
            )

            parameters = {
                "obstacle_distance": obstacle_distance
            }

        elif event_type == "object_appeared":

            action_type = "inspect_object"

            action_description = (
                "Inspect the newly appeared object."
            )

            priority = "normal"
            target = metadata.get("object")

        elif event_type == "object_disappeared":

            action_type = "verify_object_status"

            action_description = (
                "Verify the disappearance of the object."
            )

            priority = "normal"
            target = metadata.get("object")

        elif event_type == "entity_present":

            action_type = "monitor_entity"

            action_description = (
                "Monitor the detected entity."
            )

            priority = "normal"
            target = metadata.get("entity")

        elif event_type == "entity_absent":

            action_type = "search_entity"

            action_description = (
                "Search the environment for the "
                "missing entity."
            )

            priority = "medium"
            target = metadata.get("entity")

        elif event_type == "threshold_exceeded":

            action_type = "respond_to_threshold"

            action_description = (
                "Respond to the exceeded sensor "
                "threshold and reassess the environment."
            )

            priority = "high"
            target = metadata.get("sensor_name")

            parameters = {
                "value": metadata.get("value"),
                "threshold": metadata.get("threshold"),
                "operator": metadata.get("operator"),
            }

        if severity in {"high", "critical"}:
            priority = "high"

        return self.create_action(
            action_type=action_type,
            description=action_description,
            target=target,
            parameters=parameters,
            confidence=0.9,
            priority=priority,
        )

    def plan_from_events(
        self,
        events: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        planned = []

        for event in events:

            if not isinstance(event, dict):
                continue

            result = self.plan_from_event(
                event_type=event.get(
                    "event_type",
                    "unknown",
                ),
                description=event.get(
                    "description",
                    "",
                ),
                severity=event.get(
                    "severity",
                    "normal",
                ),
                metadata=event.get(
                    "metadata",
                    {},
                ),
            )

            planned.append(
                result["action"]
            )

        priority_order = {
            "high": 0,
            "medium": 1,
            "normal": 2,
            "low": 3,
        }

        planned.sort(
            key=lambda action: priority_order.get(
                action["priority"],
                2,
            )
        )

        result = {
            "status": "success",
            "action_count": len(planned),
            "actions": planned,
            "message": (
                "Actions planned from detected events."
            ),
        }

        self.last_result = result

        return result

    def update_action_status(
        self,
        action_id: str,
        status: str,
    ) -> Dict[str, Any]:

        valid_statuses = {
            "planned",
            "executing",
            "completed",
            "failed",
            "cancelled",
        }

        if status not in valid_statuses:
            raise ValueError(
                "Invalid action status."
            )

        for action in self.planned_actions:

            if action["action_id"] == action_id:

                action["status"] = status

                result = {
                    "status": "success",
                    "action": action,
                    "message": (
                        "Action status updated successfully."
                    ),
                }

                self.last_result = result

                return result

        raise ValueError(
            f"Action not found: {action_id}"
        )

    def get_all_actions(
        self,
    ) -> Dict[str, Any]:

        result = {
            "status": "success",
            "action_count": len(
                self.planned_actions
            ),
            "actions": self.planned_actions,
        }

        self.last_result = result

        return result

    def get_last_result(self):
        return self.last_result

    @staticmethod
    def _extract_obstacle_distance(
        metadata: Dict[str, Any],
    ) -> Optional[float]:

        if not isinstance(metadata, dict):
            return None

        possible_keys = [
            "distance",
            "obstacle_distance",
            "distance_meters",
            "distance_meter",
            "sensor_distance",
        ]

        for key in possible_keys:

            value = metadata.get(key)

            if value is None:
                continue

            try:
                return float(value)
            except (
                TypeError,
                ValueError,
            ):
                continue

        return None


action_planning_engine = ActionPlanningEngine()