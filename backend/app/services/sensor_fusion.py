from datetime import datetime
from typing import Any, Dict, List
from uuid import uuid4

from app.models.world_state import (
    DetectedEvent,
    DetectedObject,
    Observation,
    SensorReading,
    WorldState,
)


class SensorFusionEngine:
    """
    Combines observations from multiple modalities into
    a unified AEGIS World State.
    """

    def __init__(self):
        self.current_state: WorldState | None = None

    def create_initial_state(
        self,
        environment: str = "unknown",
        location: str | None = None,
    ) -> WorldState:
        """
        Create a new empty world state.
        """

        self.current_state = WorldState(
            state_id=str(uuid4()),
            environment=environment,
            location=location,
            timestamp=datetime.utcnow(),
        )

        return self.current_state

    def fuse_observations(
        self,
        observations: List[Observation],
        environment: str = "unknown",
        location: str | None = None,
    ) -> WorldState:
        """
        Combine multimodal observations into a unified
        world state.
        """

        state = self.create_initial_state(
            environment=environment,
            location=location,
        )

        state.observations.extend(observations)

        for observation in observations:
            self._process_observation(
                state,
                observation,
            )

        state.overall_confidence = self._calculate_confidence(
            state
        )

        state.world_context = self._build_world_context(
            state
        )

        state.requires_replanning = self._check_replanning(
            state
        )

        self.current_state = state

        return state

    def _process_observation(
        self,
        state: WorldState,
        observation: Observation,
    ) -> None:
        """
        Convert individual observations into structured
        world-state information.
        """

        modality = observation.modality.lower()

        if modality == "image":
            self._process_image(
                state,
                observation,
            )

        elif modality == "video":
            self._process_video(
                state,
                observation,
            )

        elif modality == "audio":
            self._process_audio(
                state,
                observation,
            )

        elif modality == "document":
            self._process_document(
                state,
                observation,
            )

        elif modality == "text":
            self._process_text(
                state,
                observation,
            )

        elif modality == "sensor":
            self._process_sensor(
                state,
                observation,
            )

    def _process_image(
        self,
        state: WorldState,
        observation: Observation,
    ) -> None:
        """
        Process image-level information.

        Actual computer vision models will be connected
        in the perception layer later.
        """

        metadata = observation.metadata

        objects = metadata.get("objects", [])

        for index, item in enumerate(objects):
            if isinstance(item, str):
                label = item
                confidence = observation.confidence
            else:
                label = item.get("label", "unknown")
                confidence = float(
                    item.get(
                        "confidence",
                        observation.confidence,
                    )
                )

            state.detected_objects.append(
                DetectedObject(
                    object_id=f"image-object-{index}-{uuid4()}",
                    label=label,
                    confidence=confidence,
                    attributes={
                        "source": "image",
                    },
                )
            )

    def _process_video(
        self,
        state: WorldState,
        observation: Observation,
    ) -> None:
        """
        Process video-level information.

        Temporal reasoning will be added later.
        """

        metadata = observation.metadata

        events = metadata.get("events", [])

        for index, event in enumerate(events):
            if isinstance(event, str):
                event_type = event
                description = event
                confidence = observation.confidence
            else:
                event_type = event.get(
                    "event_type",
                    "unknown",
                )
                description = event.get(
                    "description",
                    "Video event detected.",
                )
                confidence = float(
                    event.get(
                        "confidence",
                        observation.confidence,
                    )
                )

            state.detected_events.append(
                DetectedEvent(
                    event_id=f"video-event-{index}-{uuid4()}",
                    event_type=event_type,
                    description=description,
                    confidence=confidence,
                    severity="normal",
                )
            )

    def _process_audio(
        self,
        state: WorldState,
        observation: Observation,
    ) -> None:
        """
        Process speech/audio information.

        Speech recognition will be connected later.
        """

        transcript = observation.metadata.get(
            "transcript"
        )

        if transcript:
            state.world_context["latest_audio_transcript"] = (
                transcript
            )

    def _process_document(
        self,
        state: WorldState,
        observation: Observation,
    ) -> None:
        """
        Process document information.
        """

        document_text = observation.metadata.get(
            "text"
        )

        if document_text:
            state.world_context["document_text"] = (
                document_text
            )

    def _process_text(
        self,
        state: WorldState,
        observation: Observation,
    ) -> None:
        """
        Process textual instructions or information.
        """

        text = observation.content

        if text:
            state.world_context["latest_text"] = text

        metadata_text = observation.metadata.get("text")

        if metadata_text:
            state.world_context["latest_text"] = (
                metadata_text
            )

    def _process_sensor(
        self,
        state: WorldState,
        observation: Observation,
    ) -> None:
        """
        Convert sensor metadata into structured readings.
        """

        metadata = observation.metadata

        sensor_name = metadata.get(
            "sensor_name",
            "unknown_sensor",
        )

        value = metadata.get(
            "value"
        )

        unit = metadata.get(
            "unit",
            "",
        )

        if value is not None:
            state.sensor_readings.append(
                SensorReading(
                    sensor_name=sensor_name,
                    value=float(value),
                    unit=unit,
                    confidence=observation.confidence,
                )
            )

    def _calculate_confidence(
        self,
        state: WorldState,
    ) -> float:
        """
        Calculate an overall confidence score from
        all available observations.
        """

        if not state.observations:
            return 0.0

        total_confidence = sum(
            observation.confidence
            for observation in state.observations
        )

        return round(
            total_confidence / len(state.observations),
            3,
        )

    def _build_world_context(
        self,
        state: WorldState,
    ) -> Dict[str, Any]:
        """
        Build a compact summary of the current world.
        """

        return {
            "environment": state.environment,
            "location": state.location,
            "observation_count": len(
                state.observations
            ),
            "object_count": len(
                state.detected_objects
            ),
            "sensor_count": len(
                state.sensor_readings
            ),
            "event_count": len(
                state.detected_events
            ),
            "modalities": sorted(
                {
                    observation.modality
                    for observation in state.observations
                }
            ),
        }

    def _check_replanning(
        self,
        state: WorldState,
    ) -> bool:
        """
        Determine whether the current state indicates
        that replanning may be required.
        """

        for event in state.detected_events:
            if event.severity.lower() in {
                "high",
                "critical",
            }:
                return True

        for reading in state.sensor_readings:
            if (
                reading.sensor_name.lower()
                in {
                    "obstacle_distance",
                    "distance",
                }
                and reading.value < 1.0
            ):
                return True

        return False

    def get_current_state(self) -> WorldState | None:
        """
        Return the latest fused world state.
        """

        return self.current_state


sensor_fusion_engine = SensorFusionEngine()