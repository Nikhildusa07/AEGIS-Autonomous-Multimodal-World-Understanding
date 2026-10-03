from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.models.world_state import Observation
from app.services.sensor_fusion import sensor_fusion_engine


class ContinuousObservationEngine:
    def __init__(self):
        self.observation_history: List[Observation] = []
        self.latest_observation: Optional[Observation] = None
        self.latest_world_state: Optional[Dict[str, Any]] = None
        self.is_observing: bool = False
        self.observation_count: int = 0
        self.last_result: Optional[Dict[str, Any]] = None

    def start_observation(
        self,
        environment: str = "simulated_environment",
        location: Optional[str] = None,
    ) -> Dict[str, Any]:

        self.is_observing = True

        result = {
            "status": "success",
            "observing": True,
            "environment": environment,
            "location": location,
            "started_at": datetime.utcnow(),
            "message": (
                "Continuous observation started."
            ),
        }

        self.last_result = result

        return result

    def stop_observation(self) -> Dict[str, Any]:

        self.is_observing = False

        result = {
            "status": "success",
            "observing": False,
            "observation_count": self.observation_count,
            "message": (
                "Continuous observation stopped."
            ),
        }

        self.last_result = result

        return result

    def add_observation(
        self,
        modality: str,
        source: str,
        content: Optional[str] = None,
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None,
        environment: str = "simulated_environment",
        location: Optional[str] = None,
    ) -> Dict[str, Any]:

        if not modality.strip():
            raise ValueError(
                "Observation modality cannot be empty."
            )

        if not source.strip():
            raise ValueError(
                "Observation source cannot be empty."
            )

        confidence = max(
            0.0,
            min(1.0, confidence),
        )

        observation = Observation(
            observation_id=str(uuid4()),
            modality=modality.strip().lower(),
            source=source.strip(),
            content=content,
            confidence=confidence,
            timestamp=datetime.utcnow(),
            metadata=metadata or {},
        )

        self.observation_history.append(
            observation
        )

        self.latest_observation = observation
        self.observation_count += 1

        world_state = (
            sensor_fusion_engine.fuse_observations(
                observations=[
                    *self.observation_history
                ],
                environment=environment,
                location=location,
            )
        )

        self.latest_world_state = (
            world_state.model_dump()
        )

        result = {
            "status": "success",
            "observation": observation,
            "observation_count": (
                self.observation_count
            ),
            "world_state": (
                self.latest_world_state
            ),
            "message": (
                "Observation received and world state updated."
            ),
        }

        self.last_result = result

        return result

    def get_latest_observation(
        self,
    ) -> Dict[str, Any]:

        if self.latest_observation is None:
            return {
                "status": "success",
                "observation": None,
                "message": (
                    "No observation available."
                ),
            }

        return {
            "status": "success",
            "observation": self.latest_observation,
            "message": (
                "Latest observation retrieved."
            ),
        }

    def get_latest_world_state(
        self,
    ) -> Dict[str, Any]:

        if self.latest_world_state is None:
            return {
                "status": "success",
                "world_state": None,
                "message": (
                    "No world state available."
                ),
            }

        return {
            "status": "success",
            "world_state": (
                self.latest_world_state
            ),
            "message": (
                "Latest world state retrieved."
            ),
        }

    def get_observation_history(
        self,
    ) -> Dict[str, Any]:

        result = {
            "status": "success",
            "observing": self.is_observing,
            "observation_count": (
                self.observation_count
            ),
            "observations": (
                self.observation_history
            ),
        }

        self.last_result = result

        return result

    def get_status(self) -> Dict[str, Any]:

        return {
            "status": "success",
            "observing": self.is_observing,
            "observation_count": (
                self.observation_count
            ),
            "has_latest_observation": (
                self.latest_observation is not None
            ),
            "has_world_state": (
                self.latest_world_state is not None
            ),
        }

    def get_last_result(self):
        return self.last_result


continuous_observation_engine = (
    ContinuousObservationEngine()
)