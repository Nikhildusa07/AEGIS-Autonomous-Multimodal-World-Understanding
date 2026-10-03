from pathlib import Path
from typing import Any, Dict, List

from ultralytics import YOLO


class ObjectDetectionEngine:
    def __init__(self):
        self.model = YOLO("yolo11n.pt")
        self.last_result: Dict[str, Any] | None = None

    def detect_objects(
        self,
        image_path: str,
        confidence_threshold: float = 0.25,
    ) -> Dict[str, Any]:

        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Image file not found: {image_path}"
            )

        try:
            results = self.model.predict(
                source=str(path),
                conf=confidence_threshold,
                verbose=False,
            )

            detected_objects: List[Dict[str, Any]] = []

            for result in results:
                boxes = result.boxes

                if boxes is None:
                    continue

                names = result.names

                for index in range(len(boxes)):
                    class_id = int(
                        boxes.cls[index].item()
                    )

                    confidence = float(
                        boxes.conf[index].item()
                    )

                    coordinates = boxes.xyxy[index].tolist()

                    detected_objects.append(
                        {
                            "object_id": f"object-{index + 1}",
                            "label": names[class_id],
                            "class_id": class_id,
                            "confidence": round(
                                confidence,
                                4,
                            ),
                            "bounding_box": {
                                "x1": round(
                                    coordinates[0],
                                    2,
                                ),
                                "y1": round(
                                    coordinates[1],
                                    2,
                                ),
                                "x2": round(
                                    coordinates[2],
                                    2,
                                ),
                                "y2": round(
                                    coordinates[3],
                                    2,
                                ),
                            },
                        }
                    )

            result_data = {
                "status": "success",
                "filename": path.name,
                "model": "YOLO11n",
                "object_count": len(
                    detected_objects
                ),
                "objects": detected_objects,
            }

            self.last_result = result_data

            return result_data

        except Exception as exc:
            result_data = {
                "status": "error",
                "filename": path.name,
                "model": "YOLO11n",
                "object_count": 0,
                "objects": [],
                "error": str(exc),
            }

            self.last_result = result_data

            return result_data

    def get_last_result(self):
        return self.last_result


object_detection_engine = ObjectDetectionEngine()