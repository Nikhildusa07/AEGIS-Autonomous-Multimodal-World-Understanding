from datetime import datetime
from typing import Any, Dict, Optional


class ActionVerificationEngine:
    def __init__(self):
        self.verification_history: list[Dict[str, Any]] = []
        self.last_result: Optional[Dict[str, Any]] = None

    def verify_action(
        self,
        action_id: str,
        action_type: str,
        execution_status: str,
        execution_success: bool,
        expected_outcome: Optional[str] = None,
        actual_outcome: Optional[str] = None,
        verification_confidence: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        if not action_id.strip():
            raise ValueError(
                "Action ID cannot be empty."
            )

        if not action_type.strip():
            raise ValueError(
                "Action type cannot be empty."
            )

        verification_confidence = max(
            0.0,
            min(1.0, verification_confidence),
        )

        normalized_status = (
            execution_status.strip().lower()
        )

        expected = (
            expected_outcome.strip().lower()
            if expected_outcome
            else None
        )

        actual = (
            actual_outcome.strip().lower()
            if actual_outcome
            else None
        )

        if not execution_success:
            verified = False
            verification_status = "failed"

        elif normalized_status != "completed":
            verified = False
            verification_status = "incomplete"

        elif expected and actual:
            verified = expected == actual

            if verified:
                verification_status = "verified"
            else:
                verification_status = "mismatch"

        else:
            verified = True
            verification_status = "verified"

        if verified and verification_confidence < 0.5:
            verification_status = "low_confidence"

        verification = {
            "verification_id": self._generate_id(),
            "action_id": action_id,
            "action_type": action_type,
            "execution_status": execution_status,
            "execution_success": execution_success,
            "expected_outcome": expected_outcome,
            "actual_outcome": actual_outcome,
            "verified": verified,
            "verification_status": verification_status,
            "verification_confidence": (
                verification_confidence
            ),
            "requires_replanning": not verified,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow(),
        }

        self.verification_history.append(
            verification
        )

        result = {
            "status": "success",
            "verification": verification,
            "message": (
                "Action verification completed."
            ),
        }

        self.last_result = result

        return result

    def verify_execution(
        self,
        execution: Dict[str, Any],
        expected_outcome: Optional[str] = None,
        actual_outcome: Optional[str] = None,
    ) -> Dict[str, Any]:

        if not isinstance(execution, dict):
            raise ValueError(
                "Execution must be a dictionary."
            )

        return self.verify_action(
            action_id=execution.get(
                "action_id",
                "",
            ),
            action_type=execution.get(
                "action_type",
                "",
            ),
            execution_status=execution.get(
                "status",
                "unknown",
            ),
            execution_success=bool(
                execution.get(
                    "success",
                    False,
                )
            ),
            expected_outcome=expected_outcome,
            actual_outcome=actual_outcome,
            verification_confidence=float(
                execution.get(
                    "verification_confidence",
                    0.0,
                )
            ),
            metadata={
                "execution_id": execution.get(
                    "execution_id"
                ),
                "source": "action_execution",
            },
        )

    def verify_by_confidence(
        self,
        action_id: str,
        action_type: str,
        confidence: float,
        minimum_confidence: float = 0.8,
    ) -> Dict[str, Any]:

        confidence = max(
            0.0,
            min(1.0, confidence),
        )

        minimum_confidence = max(
            0.0,
            min(1.0, minimum_confidence),
        )

        verified = confidence >= minimum_confidence

        verification = {
            "verification_id": self._generate_id(),
            "action_id": action_id,
            "action_type": action_type,
            "verified": verified,
            "verification_status": (
                "verified"
                if verified
                else "low_confidence"
            ),
            "verification_confidence": confidence,
            "minimum_confidence": minimum_confidence,
            "requires_replanning": not verified,
            "timestamp": datetime.utcnow(),
        }

        self.verification_history.append(
            verification
        )

        result = {
            "status": "success",
            "verification": verification,
            "message": (
                "Confidence-based action verification completed."
            ),
        }

        self.last_result = result

        return result

    def get_verification_history(
        self,
    ) -> Dict[str, Any]:

        result = {
            "status": "success",
            "verification_count": len(
                self.verification_history
            ),
            "verifications": self.verification_history,
        }

        self.last_result = result

        return result

    def get_last_result(self):
        return self.last_result

    def _generate_id(self) -> str:
        from uuid import uuid4

        return str(uuid4())


action_verification_engine = ActionVerificationEngine()