from pathlib import Path
from typing import Any, Dict, List

import cv2

from app.perception.object_detection_engine import (
    object_detection_engine,
)
from app.perception.temporal_engine import (
    temporal_engine,
)


class VideoEngine:
    def __init__(self):
        self.last_result: Dict[str, Any] | None = None

    def analyze_video(
        self,
        video_path: str,
        sample_interval: int = 30,
    ) -> Dict[str, Any]:

        path = Path(video_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Video file not found: {video_path}"
            )

        capture = cv2.VideoCapture(str(path))

        if not capture.isOpened():
            raise ValueError(
                f"Unable to open video: {video_path}"
            )

        try:
            fps = capture.get(cv2.CAP_PROP_FPS)

            frame_count = int(
                capture.get(cv2.CAP_PROP_FRAME_COUNT)
            )

            if fps <= 0:
                fps = 1.0

            duration_seconds = frame_count / fps

            frame_index = 0
            sampled_frames = 0

            detected_objects: List[Dict[str, Any]] = []

            while True:
                success, frame = capture.read()

                if not success:
                    break

                if frame_index % sample_interval == 0:
                    sampled_frames += 1

                    frame_path = (
                        Path("uploads/video")
                        / f"frame_{frame_index}.jpg"
                    )

                    frame_path.parent.mkdir(
                        parents=True,
                        exist_ok=True,
                    )

                    cv2.imwrite(
                        str(frame_path),
                        frame,
                    )

                    detection = (
                        object_detection_engine.detect_objects(
                            str(frame_path)
                        )
                    )

                    detected_objects.append(
                        {
                            "frame_index": frame_index,
                            "timestamp_seconds": round(
                                frame_index / fps,
                                2,
                            ),
                            "objects": detection.get(
                                "objects",
                                [],
                            ),
                        }
                    )

                    if frame_path.exists():
                        frame_path.unlink()

                frame_index += 1

            temporal_result = (
                temporal_engine.analyze_timeline(
                    detected_objects
                )
            )

            result = {
                "status": "success",
                "filename": path.name,
                "fps": round(fps, 2),
                "frame_count": frame_count,
                "duration_seconds": round(
                    duration_seconds,
                    2,
                ),
                "sample_interval": sample_interval,
                "sampled_frames": sampled_frames,
                "frames": detected_objects,
                "temporal_analysis": temporal_result,
            }

            self.last_result = result

            return result

        except Exception as exc:
            result = {
                "status": "error",
                "filename": path.name,
                "error": str(exc),
            }

            self.last_result = result

            return result

        finally:
            capture.release()

    def get_last_result(self):
        return self.last_result


video_engine = VideoEngine()