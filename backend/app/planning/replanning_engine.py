from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.planning.action_engine import (
    action_planning_engine,
)


class ReplanningEngine:
    def __init__(self):
        self.replanning_history: List[Dict[str, Any]] = []
        self.last_result: Optional[Dict[str, Any]] = None

    def evaluate_replanning(
        self,
        world_state: Dict[str, Any],
        verification: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        reasons: List[str] = []

        if not isinstance(world_state, dict):
            raise ValueError(
                "World state must be a dictionary."
            )

        if world_state.get("requires_replanning"):
            reasons.append(
                "World state requires replanning."
            )

        detected_events = world_state.get(
            "detected_events",
            [],
        )

        for event in detected_events:
            if not isinstance(event, dict):
                continue

            severity = str(
                event.get(
                    "severity",
                    "normal",
                )
            ).lower()

            if severity in {"high", "critical"}:
                reasons.append(
                    f"High-priority event detected: "
                    f"{event.get('event_type', 'unknown')}."
                )

        sensor_readings = world_state.get(
            "sensor_readings",
            [],
        )

        for reading in sensor_readings:
            if not isinstance(reading, dict):
                continue

            sensor_name = str(
                reading.get(
                    "sensor_name",
                    "",
                )
            ).lower()

            value = reading.get("value")

            if (
                sensor_name
                in {
                    "obstacle_distance",
                    "distance",
                }
                and value is not None
                and float(value) < 1.0
            ):
                reasons.append(
                    "Obstacle distance is below the "
                    "safe threshold."
                )

        if verification:
            if not isinstance(verification, dict):
                raise ValueError(
                    "Verification must be a dictionary."
                )

            if not verification.get(
                "verified",
                False,
            ):
                reasons.append(
                    "Previous action verification failed."
                )

            if verification.get(
                "requires_replanning",
                False,
            ):
                reasons.append(
                    "Previous action requires replanning."
                )

        should_replan = len(reasons) > 0

        result = {
            "status": "success",
            "should_replan": should_replan,
            "reason_count": len(reasons),
            "reasons": reasons,
            "timestamp": datetime.utcnow(),
        }

        self.last_result = result

        return result

    def generate_new_plan(
        self,
        world_state: Dict[str, Any],
        verification: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        evaluation = self.evaluate_replanning(
            world_state=world_state,
            verification=verification,
        )

        if not evaluation["should_replan"]:
            result = {
                "status": "success",
                "replanned": False,
                "evaluation": evaluation,
                "actions": [],
                "message": (
                    "Replanning is not required."
                ),
            }

            self.last_result = result

            return result

        events = world_state.get(
            "detected_events",
            [],
        )

        actions: List[Dict[str, Any]] = []

        if events:
            planned = (
                action_planning_engine
                .plan_from_events(events)
            )

            actions.extend(
                planned.get(
                    "actions",
                    [],
                )
            )

        if not actions:
            actions.append(
                action_planning_engine.create_action(
                    action_type="reobserve_environment",
                    description=(
                        "Reobserve the environment "
                        "before selecting the next action."
                    ),
                    target=world_state.get(
                        "location"
                    ),
                    parameters={
                        "reason": evaluation[
                            "reasons"
                        ]
                    },
                    confidence=0.85,
                    priority="high",
                )["action"]
            )

        replanning_record = {
            "replanning_id": str(uuid4()),
            "replanned": True,
            "evaluation": evaluation,
            "actions": actions,
            "timestamp": datetime.utcnow(),
        }

        self.replanning_history.append(
            replanning_record
        )

        result = {
            "status": "success",
            "replanned": True,
            "evaluation": evaluation,
            "actions": actions,
            "message": (
                "New plan generated successfully."
            ),
        }

        self.last_result = result

        return result

    def replan_from_verification(
        self,
        world_state: Dict[str, Any],
        verification: Dict[str, Any],
    ) -> Dict[str, Any]:

        return self.generate_new_plan(
            world_state=world_state,
            verification=verification,
        )

    def get_replanning_history(
        self,
    ) -> Dict[str, Any]:

        result = {
            "status": "success",
            "replanning_count": len(
                self.replanning_history
            ),
            "replanning_history": (
                self.replanning_history
            ),
        }

        self.last_result = result

        return result

    def get_last_result(self):
        return self.last_result


replanning_engine = ReplanningEngine()