from typing import Any, Dict, List, Optional
from uuid import uuid4


class KnowledgeRepresentationEngine:
    def __init__(self):
        self.entities: Dict[str, Dict[str, Any]] = {}
        self.relations: List[Dict[str, Any]] = []
        self.last_result: Optional[Dict[str, Any]] = None

    def add_entity(
        self,
        name: str,
        entity_type: str = "unknown",
        attributes: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        if not name or not name.strip():
            raise ValueError("Entity name cannot be empty.")

        entity_id = str(uuid4())

        entity = {
            "id": entity_id,
            "name": name.strip(),
            "type": entity_type,
            "attributes": attributes or {},
        }

        self.entities[entity_id] = entity

        return {
            "status": "success",
            "entity": entity,
            "message": "Entity added to knowledge representation.",
        }

    def find_entity(
        self,
        name: str,
    ) -> Optional[Dict[str, Any]]:

        search_name = name.strip().lower()

        for entity in self.entities.values():
            if entity["name"].lower() == search_name:
                return entity

        return None

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
            raise ValueError("Relation cannot be empty.")

        if not object_name.strip():
            raise ValueError("Object cannot be empty.")

        confidence = max(0.0, min(1.0, confidence))

        subject_entity = self.find_entity(subject)

        if subject_entity is None:
            subject_entity = self.add_entity(
                name=subject,
                entity_type="unknown",
            )["entity"]

        object_entity = self.find_entity(object_name)

        if object_entity is None:
            object_entity = self.add_entity(
                name=object_name,
                entity_type="unknown",
            )["entity"]

        relation_data = {
            "id": str(uuid4()),
            "subject": {
                "id": subject_entity["id"],
                "name": subject_entity["name"],
            },
            "relation": relation.strip(),
            "object": {
                "id": object_entity["id"],
                "name": object_entity["name"],
            },
            "confidence": confidence,
            "metadata": metadata or {},
        }

        self.relations.append(relation_data)

        return {
            "status": "success",
            "relation": relation_data,
            "message": "Knowledge relation added successfully.",
        }

    def get_entity_relations(
        self,
        entity_name: str,
    ) -> List[Dict[str, Any]]:

        search_name = entity_name.strip().lower()

        results = []

        for relation in self.relations:
            subject_name = relation["subject"]["name"].lower()
            object_name = relation["object"]["name"].lower()

            if (
                subject_name == search_name
                or object_name == search_name
            ):
                results.append(relation)

        return results

    def query(
        self,
        entity_name: Optional[str] = None,
        relation: Optional[str] = None,
    ) -> Dict[str, Any]:

        results = self.relations

        if entity_name:
            search_name = entity_name.strip().lower()

            results = [
                item
                for item in results
                if (
                    item["subject"]["name"].lower()
                    == search_name
                    or item["object"]["name"].lower()
                    == search_name
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

    def get_knowledge_graph(self) -> Dict[str, Any]:

        result = {
            "status": "success",
            "entity_count": len(self.entities),
            "relation_count": len(self.relations),
            "entities": list(self.entities.values()),
            "relations": self.relations,
        }

        self.last_result = result

        return result

    def get_last_result(self):
        return self.last_result


knowledge_representation_engine = (
    KnowledgeRepresentationEngine()
)