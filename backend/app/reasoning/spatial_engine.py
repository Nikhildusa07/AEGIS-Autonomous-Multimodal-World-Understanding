from math import sqrt
from typing import Any, Dict, List, Optional


class SpatialReasoningEngine:
    def __init__(self):
        self.spatial_relations: List[Dict[str, Any]] = []
        self.last_result: Optional[Dict[str, Any]] = None

    def add_relation(
        self,
        subject: str,
        relation: str,
        object_name: str,
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        if not subject.strip():
            raise ValueError("Subject cannot be empty.")

        if not relation.strip():
            raise ValueError("Spatial relation cannot be empty.")

        if not object_name.strip():
            raise ValueError("Object cannot be empty.")

        confidence = max(0.0, min(1.0, confidence))

        relation_data = {
            "subject": subject.strip(),
            "relation": relation.strip().lower(),
            "object": object_name.strip(),
            "confidence": confidence,
            "metadata": metadata or {},
        }

        self.spatial_relations.append(relation_data)

        return {
            "status": "success",
            "relation": relation_data,
            "message": "Spatial relation added successfully.",
        }

    def calculate_distance(
        self,
        point_a: Dict[str, float],
        point_b: Dict[str, float],
    ) -> Dict[str, Any]:

        required_coordinates = {"x", "y"}

        if not required_coordinates.issubset(point_a):
            raise ValueError(
                "point_a must contain x and y coordinates."
            )

        if not required_coordinates.issubset(point_b):
            raise ValueError(
                "point_b must contain x and y coordinates."
            )

        dx = point_a["x"] - point_b["x"]
        dy = point_a["y"] - point_b["y"]

        distance = sqrt(
            (dx * dx) + (dy * dy)
        )

        if "z" in point_a and "z" in point_b:
            dz = point_a["z"] - point_b["z"]

            distance = sqrt(
                (dx * dx)
                + (dy * dy)
                + (dz * dz)
            )

        result = {
            "status": "success",
            "point_a": point_a,
            "point_b": point_b,
            "distance": round(distance, 4),
        }

        self.last_result = result

        return result

    def determine_direction(
        self,
        subject_position: Dict[str, float],
        reference_position: Dict[str, float],
    ) -> Dict[str, Any]:

        subject_x = subject_position.get("x", 0.0)
        subject_y = subject_position.get("y", 0.0)

        reference_x = reference_position.get("x", 0.0)
        reference_y = reference_position.get("y", 0.0)

        delta_x = subject_x - reference_x
        delta_y = subject_y - reference_y

        horizontal_relation = "same_x"
        vertical_relation = "same_y"

        if delta_x > 0:
            horizontal_relation = "right_of"
        elif delta_x < 0:
            horizontal_relation = "left_of"

        if delta_y > 0:
            vertical_relation = "above"
        elif delta_y < 0:
            vertical_relation = "below"

        result = {
            "status": "success",
            "subject_position": subject_position,
            "reference_position": reference_position,
            "horizontal_relation": horizontal_relation,
            "vertical_relation": vertical_relation,
            "delta_x": round(delta_x, 4),
            "delta_y": round(delta_y, 4),
        }

        self.last_result = result

        return result

    def classify_proximity(
        self,
        distance: float,
        near_threshold: float = 2.0,
        far_threshold: float = 10.0,
    ) -> Dict[str, Any]:

        if distance < 0:
            raise ValueError(
                "Distance cannot be negative."
            )

        if near_threshold < 0:
            raise ValueError(
                "Near threshold cannot be negative."
            )

        if far_threshold < near_threshold:
            raise ValueError(
                "Far threshold must be greater than "
                "or equal to near threshold."
            )

        if distance <= near_threshold:
            classification = "near"
        elif distance >= far_threshold:
            classification = "far"
        else:
            classification = "moderate"

        result = {
            "status": "success",
            "distance": distance,
            "near_threshold": near_threshold,
            "far_threshold": far_threshold,
            "classification": classification,
        }

        self.last_result = result

        return result

    def query_relations(
        self,
        entity_name: Optional[str] = None,
        relation: Optional[str] = None,
    ) -> Dict[str, Any]:

        results = self.spatial_relations

        if entity_name:
            search_name = entity_name.strip().lower()

            results = [
                item
                for item in results
                if (
                    item["subject"].lower() == search_name
                    or item["object"].lower() == search_name
                )
            ]

        if relation:
            search_relation = relation.strip().lower()

            results = [
                item
                for item in results
                if item["relation"].lower()
                == search_relation
            ]

        result = {
            "status": "success",
            "entity": entity_name,
            "relation": relation,
            "result_count": len(results),
            "relations": results,
        }

        self.last_result = result

        return result

    def get_all_relations(self) -> Dict[str, Any]:

        result = {
            "status": "success",
            "relation_count": len(
                self.spatial_relations
            ),
            "relations": self.spatial_relations,
        }

        self.last_result = result

        return result

    def get_last_result(self):
        return self.last_result


spatial_reasoning_engine = SpatialReasoningEngine()