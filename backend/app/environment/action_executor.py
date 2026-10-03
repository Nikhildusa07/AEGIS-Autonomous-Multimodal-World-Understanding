from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4


class ActionExecutionEngine:
    def __init__(self):
        self.execution_history: list[Dict[str, Any]] = []
        self.last_result: Optional[Dict[str, Any]] = None

    def execute_action(
        self,
        action_type: str,
        description: str,
        target: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not action_type.strip():
            raise ValueError(
                "Action type cannot be empty."
            )

        if not description.strip():
            raise ValueError(
                "Action description cannot be empty."
            )

        parameters = parameters or {}

        action_id = str(uuid4())
        normalized_type = action_type.strip().lower()

        if normalized_type == "move":
            result = self._execute_move(
                action_id=action_id,
                target=target,
                parameters=parameters,
            )

        elif normalized_type == "avoid_obstacle":
            result = self._execute_avoid_obstacle(
                action_id=action_id,
                target=target,
                parameters=parameters,
            )

        elif normalized_type == "inspect_object":
            result = self._execute_inspect_object(
                action_id=action_id,
                target=target,
                parameters=parameters,
            )

        elif normalized_type == "monitor_entity":
            result = self._execute_monitor_entity(
                action_id=action_id,
                target=target,
                parameters=parameters,
            )

        elif normalized_type == "search_entity":
            result = self._execute_search_entity(
                action_id=action_id,
                target=target,
                parameters=parameters,
            )

        elif normalized_type == "respond_to_threshold":
            result = self._execute_threshold_response(
                action_id=action_id,
                target=target,
                parameters=parameters,
            )

        else:
            result = self._execute_generic_action(
                action_id=action_id,
                action_type=normalized_type,
                target=target,
                parameters=parameters,
            )

        execution = {
            "execution_id": str(uuid4()),
            "action_id": action_id,
            "action_type": normalized_type,
            "description": description,
            "target": target,
            "parameters": parameters,
            "status": result["status"],
            "success": result["success"],
            "message": result["message"],
            "verification_confidence": result[
                "verification_confidence"
            ],
            "timestamp": datetime.utcnow(),
        }

        self.execution_history.append(execution)

        self.last_result = {
            "status": "success",
            "execution": execution,
        }

        return self.last_result

    def _execute_move(
        self,
        action_id: str,
        target: Optional[str],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        distance = parameters.get("distance", 0)
        speed = parameters.get("speed", 1)

        return {
            "status": "completed",
            "success": True,
            "message": (
                f"Movement toward '{target or 'target'}' "
                f"completed for distance {distance} "
                f"at speed {speed}."
            ),
            "verification_confidence": 0.95,
        }

    def _execute_avoid_obstacle(
        self,
        action_id: str,
        target: Optional[str],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        obstacle_distance = parameters.get(
            "obstacle_distance"
        )

        return {
            "status": "completed",
            "success": True,
            "message": (
                f"Obstacle avoidance completed. "
                f"Selected path: "
                f"'{target or 'safe_path'}'. "
                f"Obstacle distance: "
                f"{obstacle_distance}."
            ),
            "verification_confidence": 0.94,
        }

    def _execute_inspect_object(
        self,
        action_id: str,
        target: Optional[str],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "status": "completed",
            "success": True,
            "message": (
                f"Inspection of object "
                f"'{target or 'unknown'}' completed."
            ),
            "verification_confidence": 0.9,
        }

    def _execute_monitor_entity(
        self,
        action_id: str,
        target: Optional[str],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "status": "completed",
            "success": True,
            "message": (
                f"Monitoring of entity "
                f"'{target or 'unknown'}' started successfully."
            ),
            "verification_confidence": 0.88,
        }

    def _execute_search_entity(
        self,
        action_id: str,
        target: Optional[str],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "status": "completed",
            "success": True,
            "message": (
                f"Search operation for entity "
                f"'{target or 'unknown'}' completed."
            ),
            "verification_confidence": 0.85,
        }

    def _execute_threshold_response(
        self,
        action_id: str,
        target: Optional[str],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "status": "completed",
            "success": True,
            "message": (
                f"Threshold response for "
                f"'{target or 'sensor'}' completed."
            ),
            "verification_confidence": 0.92,
        }

    def _execute_generic_action(
        self,
        action_id: str,
        action_type: str,
        target: Optional[str],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "status": "completed",
            "success": True,
            "message": (
                f"Generic action '{action_type}' "
                f"executed successfully."
            ),
            "verification_confidence": 0.8,
        }

    def get_execution_history(self) -> Dict[str, Any]:
        result = {
            "status": "success",
            "execution_count": len(
                self.execution_history
            ),
            "executions": self.execution_history,
        }

        self.last_result = result

        return result

    def get_last_result(self):
        return self.last_result


action_execution_engine = ActionExecutionEngine()