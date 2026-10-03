from typing import Any, Dict, List


class TemporalEngine:
    def __init__(self):
        self.last_result: Dict[str, Any] | None = None

    def analyze_timeline(
        self,
        frames: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        timeline: List[Dict[str, Any]] = []
        previous_labels: set[str] = set()

        for frame in frames:
            timestamp = frame.get(
                "timestamp_seconds",
                0,
            )

            objects = frame.get(
                "objects",
                [],
            )

            current_labels = {
                obj.get("label", "unknown")
                for obj in objects
                if isinstance(obj, dict)
            }

            appeared = sorted(
                current_labels - previous_labels
            )

            disappeared = sorted(
                previous_labels - current_labels
            )

            if appeared or disappeared:
                event = {
                    "timestamp_seconds": timestamp,
                    "appeared": appeared,
                    "disappeared": disappeared,
                    "active_objects": sorted(
                        current_labels
                    ),
                }

                timeline.append(event)

            previous_labels = current_labels

        result = {
            "status": "success",
            "event_count": len(timeline),
            "events": timeline,
        }

        self.last_result = result

        return result

    def get_last_result(self):
        return self.last_result


temporal_engine = TemporalEngine()