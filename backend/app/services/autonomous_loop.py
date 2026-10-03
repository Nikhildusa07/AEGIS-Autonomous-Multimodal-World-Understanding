from datetime import datetime
from typing import Any, Dict, List, Optional

from app.environment.action_executor import (
    action_execution_engine,
)
from app.environment.action_verifier import (
    action_verification_engine,
)
from app.environment.observation_loop import (
    continuous_observation_engine,
)
from app.planning.action_engine import (
    action_planning_engine,
)
from app.planning.replanning_engine import (
    replanning_engine,
)
from app.reasoning.uncertainty_engine import (
    uncertainty_estimation_engine,
)
from app.reasoning.vision_language_engine import (
    vision_language_reasoning_engine,
)


class AutonomousLoopEngine:

    def __init__(self):
        self.cycle_history: List[Dict[str, Any]] = []
        self.last_result: Optional[Dict[str, Any]] = None
        self.cycle_count: int = 0

    def run_cycle(
        self,
        world_state: Dict[str, Any],
        visual_objects: Optional[
            List[Dict[str, Any]]
        ] = None,
        visual_scene: Optional[str] = None,
        ocr_text: Optional[str] = None,
        audio_transcript: Optional[str] = None,
        text_context: Optional[str] = None,
        execute_actions: bool = True,
        observation_inputs: Optional[
            List[Dict[str, Any]]
        ] = None,
    ) -> Dict[str, Any]:

        if not isinstance(world_state, dict):
            raise ValueError(
                "World state must be a dictionary."
            )

        self.cycle_count += 1

        cycle_id = (
            f"aegis-cycle-{self.cycle_count}"
        )

        stages: Dict[str, Any] = {}

        # =================================================
        # 1. CONTINUOUS OBSERVATION
        # =================================================

        observation_results = []

        if observation_inputs:

            for observation in observation_inputs:

                if not isinstance(
                    observation,
                    dict,
                ):
                    continue

                observation_result = (
                    continuous_observation_engine
                    .add_observation(
                        modality=observation.get(
                            "modality",
                            "unknown",
                        ),
                        source=observation.get(
                            "source",
                            "autonomous_loop",
                        ),
                        content=observation.get(
                            "content"
                        ),
                        confidence=float(
                            observation.get(
                                "confidence",
                                1.0,
                            )
                        ),
                        metadata=observation.get(
                            "metadata",
                            {},
                        ),
                        environment=observation.get(
                            "environment",
                            world_state.get(
                                "environment",
                                "simulated_environment",
                            ),
                        ),
                        location=observation.get(
                            "location",
                            world_state.get(
                                "location"
                            ),
                        ),
                    )
                )

                observation_results.append(
                    observation_result
                )

        stages[
            "continuous_observation"
        ] = {
            "observation_count": len(
                observation_results
            ),
            "results": observation_results,
        }

        # =================================================
        # 2. VISION-LANGUAGE REASONING
        # =================================================

        vision_language_result = (
            vision_language_reasoning_engine.reason(
                visual_objects=visual_objects or [],
                visual_scene=visual_scene,
                ocr_text=ocr_text,
                audio_transcript=audio_transcript,
                text_context=text_context,
                metadata={
                    "source": "autonomous_loop",
                    "cycle_id": cycle_id,
                },
            )
        )

        stages[
            "vision_language_reasoning"
        ] = vision_language_result

        # =================================================
        # 3. UNCERTAINTY ESTIMATION
        # =================================================

        uncertainty_result = (
            uncertainty_estimation_engine
            .estimate_from_world_state(
                world_state=world_state
            )
        )

        stages[
            "uncertainty_estimation"
        ] = uncertainty_result

        uncertainty = (
            uncertainty_result.get(
                "estimation",
                {},
            )
        )

        requires_attention = bool(
            uncertainty.get(
                "requires_attention",
                False,
            )
        )

        # =================================================
        # 4. ACTION PLANNING
        # =================================================

        detected_events = world_state.get(
            "detected_events",
            [],
        )

        planned_actions: List[
            Dict[str, Any]
        ] = []

        if detected_events:

            planning_result = (
                action_planning_engine
                .plan_from_events(
                    detected_events
                )
            )

            planned_actions.extend(
                planning_result.get(
                    "actions",
                    [],
                )
            )

        stages["action_planning"] = {
            "status": "success",
            "action_count": len(
                planned_actions
            ),
            "actions": planned_actions,
        }

        # =================================================
        # 5. ACTION EXECUTION
        # =================================================

        execution_results: List[
            Dict[str, Any]
        ] = []

        if execute_actions:

            for action in planned_actions:

                try:

                    action_type = action.get(
                        "action_type",
                        "",
                    )

                    description = action.get(
                        "description",
                        "",
                    )

                    target = action.get(
                        "target"
                    )

                    parameters = action.get(
                        "parameters",
                        {},
                    )

                    raw_execution = (
                        action_execution_engine
                        .execute_action(
                            action_type=action_type,
                            description=description,
                            target=target,
                            parameters=parameters,
                        )
                    )

                    # -----------------------------------------
                    # IMPORTANT:
                    # The executor may return either:
                    #
                    # 1. Direct execution dictionary
                    #
                    # OR
                    #
                    # 2. Wrapper:
                    # {
                    #     "status": "success",
                    #     "execution": {...}
                    # }
                    #
                    # Always extract the actual execution.
                    # -----------------------------------------

                    if (
                        isinstance(
                            raw_execution,
                            dict,
                        )
                        and isinstance(
                            raw_execution.get(
                                "execution"
                            ),
                            dict,
                        )
                    ):

                        execution = dict(
                            raw_execution[
                                "execution"
                            ]
                        )

                    elif isinstance(
                        raw_execution,
                        dict,
                    ):

                        execution = dict(
                            raw_execution
                        )

                    else:

                        raise ValueError(
                            "Action execution returned "
                            "an invalid response."
                        )

                    # -----------------------------------------
                    # Normalize execution information.
                    # -----------------------------------------

                    execution[
                        "action_id"
                    ] = action.get(
                        "action_id"
                    )

                    execution[
                        "action_type"
                    ] = action_type

                    execution.setdefault(
                        "description",
                        description,
                    )

                    execution.setdefault(
                        "target",
                        target,
                    )

                    execution.setdefault(
                        "parameters",
                        parameters,
                    )

                    execution_results.append(
                        execution
                    )

                except Exception as exc:

                    execution_results.append(
                        {
                            "status": "failed",
                            "success": False,
                            "action_id": action.get(
                                "action_id"
                            ),
                            "action_type": action.get(
                                "action_type"
                            ),
                            "description": action.get(
                                "description",
                                "",
                            ),
                            "target": action.get(
                                "target"
                            ),
                            "parameters": action.get(
                                "parameters",
                                {},
                            ),
                            "message": str(exc),
                            "verification_confidence": 0.0,
                        }
                    )

        stages["action_execution"] = {
            "status": "success",
            "execution_count": len(
                execution_results
            ),
            "executions": execution_results,
        }

        # =================================================
        # 6. ACTION VERIFICATION
        # =================================================

        verification_results: List[
            Dict[str, Any]
        ] = []

        for execution in execution_results:

            # ---------------------------------------------
            # Final defensive normalization.
            # If a wrapper somehow reaches this stage,
            # unwrap it before verification.
            # ---------------------------------------------

            verification_input = execution

            if (
                isinstance(
                    execution,
                    dict,
                )
                and isinstance(
                    execution.get(
                        "execution"
                    ),
                    dict,
                )
            ):

                verification_input = (
                    execution[
                        "execution"
                    ]
                )

            verification = (
                action_verification_engine
                .verify_execution(
                    execution=verification_input
                )
            )

            verification_results.append(
                verification
            )

        stages[
            "action_verification"
        ] = {
            "status": "success",
            "verification_count": len(
                verification_results
            ),
            "verifications": verification_results,
        }

        failed_verification = any(
            not item.get(
                "verification",
                {},
            ).get(
                "verified",
                False,
            )
            for item in verification_results
        )

        # =================================================
        # 7. REPLANNING
        # =================================================

        verification_for_replanning = None

        if verification_results:

            verification_for_replanning = (
                verification_results[-1].get(
                    "verification"
                )
            )

        should_replan = (
            world_state.get(
                "requires_replanning",
                False,
            )
            or requires_attention
            or failed_verification
        )

        replanning_result = {
            "status": "success",
            "replanned": False,
            "message": (
                "Replanning was not required."
            ),
        }

        if should_replan:

            replanning_result = (
                replanning_engine
                .generate_new_plan(
                    world_state=world_state,
                    verification=(
                        verification_for_replanning
                    ),
                )
            )

        stages["replanning"] = (
            replanning_result
        )

        # =================================================
        # 8. FINAL AUTONOMOUS STATE
        # =================================================

        if failed_verification:

            final_status = (
                "replanning_required"
            )

        elif requires_attention:

            final_status = (
                "uncertainty_detected"
            )

        elif should_replan:

            final_status = "replanned"

        else:

            final_status = "completed"

        result = {
            "status": "success",
            "cycle_id": cycle_id,
            "cycle_number": self.cycle_count,
            "final_status": final_status,
            "should_replan": should_replan,
            "stages": stages,
            "summary": {
                "observations_processed": len(
                    observation_results
                ),
                "actions_planned": len(
                    planned_actions
                ),
                "actions_executed": len(
                    execution_results
                ),
                "actions_verified": len(
                    verification_results
                ),
                "uncertainty_level": uncertainty.get(
                    "uncertainty_level"
                ),
                "overall_confidence": uncertainty.get(
                    "overall_confidence"
                ),
                "replanned": bool(
                    replanning_result.get(
                        "replanned",
                        False,
                    )
                ),
            },
            "timestamp": datetime.utcnow(),
        }

        self.cycle_history.append(
            result
        )

        self.last_result = result

        return result

    def get_history(
        self,
    ) -> Dict[str, Any]:

        return {
            "status": "success",
            "cycle_count": self.cycle_count,
            "cycles": self.cycle_history,
        }

    def get_last_result(
        self,
    ):

        return self.last_result


autonomous_loop_engine = (
    AutonomousLoopEngine()
)