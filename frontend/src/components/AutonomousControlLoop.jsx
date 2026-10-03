import { useEffect, useMemo, useState } from "react";

import {
  Brain,
  CheckCircle2,
  Eye,
  RefreshCw,
  ShieldCheck,
  Target,
  Zap,
} from "lucide-react";

import {
  getAutonomousResult,
  runAutonomousCycle,
} from "../services/api";

const stages = [
  {
    key: "observe",
    label: "OBSERVE",
    icon: Eye,
  },
  {
    key: "understand",
    label: "UNDERSTAND",
    icon: Brain,
  },
  {
    key: "plan",
    label: "PLAN",
    icon: Target,
  },
  {
    key: "act",
    label: "ACT",
    icon: Zap,
  },
  {
    key: "verify",
    label: "VERIFY",
    icon: ShieldCheck,
  },
  {
    key: "replan",
    label: "REPLAN",
    icon: RefreshCw,
  },
];

const autonomousPayload = {
  world_state: {
    state_id: "autonomous-test-001",
    environment: "warehouse",
    location: "Zone A",
    requires_replanning: false,
    overall_confidence: 0.88,
    detected_objects: [
      {
        object_id: "obj-001",
        label: "person",
        confidence: 0.94,
      },
      {
        object_id: "obj-002",
        label: "laptop",
        confidence: 0.91,
      },
    ],
    sensor_readings: [
      {
        sensor_name: "obstacle_distance",
        value: 2.5,
        unit: "meters",
        confidence: 0.95,
      },
    ],
    detected_events: [
      {
        event_id: "event-001",
        event_type: "obstacle_detected",
        description: "Obstacle detected in Zone A",
        confidence: 0.9,
        severity: "high",
      },
    ],
    planned_actions: [],
    action_results: [],
  },

  visual_objects: [
    {
      object_id: "obj-001",
      label: "person",
      confidence: 0.94,
    },
    {
      object_id: "obj-002",
      label: "laptop",
      confidence: 0.91,
    },
  ],

  visual_scene:
    "Warehouse Zone A with a person near a laptop and an obstacle in the area.",

  ocr_text: "Zone A - Warehouse",

  audio_transcript: "There is an obstacle in Zone A.",

  text_context:
    "The environment should be monitored for obstacles.",

  execute_actions: true,

  observation_inputs: [
    {
      modality: "sensor",
      source: "obstacle_sensor",
      content: "Obstacle detected at 2.5 meters.",
      confidence: 0.95,
      metadata: {
        sensor: "obstacle_distance",
      },
      environment: "warehouse",
      location: "Zone A",
    },
    {
      modality: "audio",
      source: "microphone",
      content: "There is an obstacle in Zone A.",
      confidence: 0.9,
      metadata: {},
      environment: "warehouse",
      location: "Zone A",
    },
  ],
};

function unwrapStage(stage) {
  if (!stage) {
    return null;
  }

  if (stage.result && typeof stage.result === "object") {
    return stage.result;
  }

  return stage;
}

function getLatestItem(stage, collectionName, singularName) {
  const normalizedStage = unwrapStage(stage);

  if (!normalizedStage) {
    return null;
  }

  const collection = normalizedStage[collectionName];

  if (Array.isArray(collection) && collection.length > 0) {
    return collection[collection.length - 1];
  }

  if (
    normalizedStage[singularName] &&
    typeof normalizedStage[singularName] === "object"
  ) {
    return normalizedStage[singularName];
  }

  return null;
}

function normalizeVerification(stage) {
  const verificationStage = unwrapStage(stage);

  if (!verificationStage) {
    return null;
  }

  let verification = getLatestItem(
    verificationStage,
    "verifications",
    "verification"
  );

  if (!verification) {
    verification = getLatestItem(
      verificationStage,
      "results",
      "result"
    );
  }

  if (
    verification?.verification &&
    typeof verification.verification === "object"
  ) {
    verification = verification.verification;
  }

  return verification;
}

function normalizeExecution(stage) {
  const executionStage = unwrapStage(stage);

  if (!executionStage) {
    return null;
  }

  let execution = getLatestItem(
    executionStage,
    "executions",
    "execution"
  );

  if (
    execution?.execution &&
    typeof execution.execution === "object"
  ) {
    execution = execution.execution;
  }

  return execution;
}

function getStageState(cycle, stageKey) {
  if (!cycle) {
    return {
      completed: false,
      text: "Waiting for autonomous cycle...",
    };
  }

  const stageMap = {
    observe: cycle.stages?.continuous_observation,
    understand: cycle.stages?.vision_language_reasoning,
    plan: cycle.stages?.action_planning,
    act: cycle.stages?.action_execution,
    verify: cycle.stages?.action_verification,
    replan: cycle.stages?.replanning,
  };

  const stage = stageMap[stageKey];

  if (!stage) {
    if (
      stageKey === "replan" &&
      cycle.should_replan === false
    ) {
      return {
        completed: true,
        text: "No replanning required",
      };
    }

    return {
      completed: false,
      text: "Waiting for autonomous cycle...",
    };
  }

  const normalizedStage = unwrapStage(stage);

  if (stageKey === "observe") {
    return {
      completed: true,
      text: `${
        normalizedStage?.observation_count ||
        normalizedStage?.observations?.length ||
        0
      } observations processed`,
    };
  }

  if (stageKey === "understand") {
    const reasoning =
      normalizedStage?.reasoning ||
      normalizedStage?.result?.reasoning ||
      normalizedStage;

    const confidence =
      reasoning?.overall_confidence ??
      reasoning?.grounding_confidence ??
      0;

    return {
      completed: true,
      text: `Grounded at ${Math.round(
        confidence * 100
      )}% confidence`,
    };
  }

  if (stageKey === "plan") {
    const actions =
      normalizedStage?.actions ||
      normalizedStage?.result?.actions ||
      [];

    const actionCount =
      normalizedStage?.action_count ??
      actions.length ??
      0;

    return {
      completed: true,
      text: `${actionCount} ${
        actionCount === 1 ? "action" : "actions"
      } planned`,
    };
  }

  if (stageKey === "act") {
    const execution = normalizeExecution(stage);

    const success =
      execution?.success === true ||
      execution?.status === "completed";

    return {
      completed: success,
      text:
        execution?.message ||
        (success
          ? "Action executed successfully"
          : "Action execution requires attention"),
    };
  }

  if (stageKey === "verify") {
    const verification = normalizeVerification(stage);

    const verified =
      verification?.verified === true ||
      verification?.verification_status === "verified";

    const confidence =
      verification?.verification_confidence ??
      verification?.confidence ??
      0;

    return {
      completed: verified,
      text: verified
        ? `Action verified at ${Math.round(
            confidence * 100
          )}% confidence`
        : "Action verification requires attention",
    };
  }

  if (stageKey === "replan") {
    const shouldReplan =
      cycle.should_replan === true;

    return {
      completed: true,
      text: shouldReplan
        ? "New plan generated"
        : "No replanning required",
    };
  }

  return {
    completed: false,
    text: "Waiting...",
  };
}

function AutonomousControlLoop() {
  const [cycle, setCycle] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadLatestCycle = async () => {
    try {
      const response = await getAutonomousResult();

      if (response?.result) {
        setCycle(response.result);
        setError("");
      }
    } catch {
      setError("Backend unavailable");
    }
  };

  const executeCycle = async () => {
    setLoading(true);
    setError("");

    try {
      const response =
        await runAutonomousCycle(
          autonomousPayload
        );

      if (response?.result) {
        setCycle(response.result);
      }
    } catch (err) {
      setError(
        err?.message ||
          "Autonomous cycle failed"
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLatestCycle();

    const interval = setInterval(() => {
      loadLatestCycle();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const confidence = useMemo(() => {
    const value =
      cycle?.stages
        ?.uncertainty_estimation
        ?.estimation
        ?.overall_confidence;

    if (typeof value !== "number") {
      return null;
    }

    return Math.round(value * 100);
  }, [cycle]);

  const status = cycle
    ? cycle.final_status === "completed"
      ? "COMPLETED"
      : cycle.final_status?.toUpperCase() ||
        "RUNNING"
    : "WAITING";

  return (
    <section className="rounded-2xl border border-white/10 bg-slate-900/55 shadow-2xl shadow-black/20 backdrop-blur-xl">
      <div className="flex items-center justify-between border-b border-white/8 px-5 py-4">
        <div className="flex items-center gap-3">
          <div className="rounded-xl border border-cyan-400/15 bg-cyan-400/5 p-2">
            <RefreshCw className="h-4 w-4 text-cyan-300" />
          </div>

          <div>
            <p className="text-[10px] font-semibold uppercase tracking-[0.22em] text-cyan-400/70">
              AUTONOMOUS CONTROL LOOP
            </p>

            <h2 className="mt-0.5 text-sm font-semibold text-slate-100">
              Observe → Understand → Act
            </h2>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span
            className={`h-2 w-2 rounded-full ${
              error
                ? "bg-red-400"
                : "animate-pulse bg-emerald-400"
            }`}
          />

          <span className="text-[9px] uppercase tracking-[0.18em] text-slate-500">
            {error
              ? "BACKEND ERROR"
              : "LIVE BACKEND"}
          </span>
        </div>
      </div>

      <div className="overflow-x-auto p-5">
        <div className="flex min-w-[900px] items-start justify-between gap-2">
          {stages.map((stage, index) => {
            const Icon = stage.icon;

            const state = getStageState(
              cycle,
              stage.key
            );

            return (
              <div
                key={stage.key}
                className="flex flex-1 items-start"
              >
                <div className="flex min-w-0 flex-1 flex-col items-center text-center">
                  <div
                    className={`relative flex h-16 w-16 items-center justify-center rounded-2xl border transition-all ${
                      state.completed
                        ? "border-cyan-400/40 bg-cyan-400/10 text-cyan-300 shadow-lg shadow-cyan-400/10"
                        : "border-white/10 bg-white/[0.03] text-slate-600"
                    }`}
                  >
                    <Icon className="h-5 w-5" />

                    {state.completed && (
                      <span className="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full border-2 border-slate-950 bg-emerald-400">
                        <CheckCircle2 className="h-2.5 w-2.5 text-slate-950" />
                      </span>
                    )}
                  </div>

                  <p
                    className={`mt-3 text-[9px] font-bold tracking-[0.16em] ${
                      state.completed
                        ? "text-cyan-300"
                        : "text-slate-600"
                    }`}
                  >
                    {stage.label}
                  </p>

                  <p
                    className={`mt-2 max-w-[150px] text-[9px] leading-4 ${
                      state.completed
                        ? "text-slate-400"
                        : "text-slate-700"
                    }`}
                  >
                    {state.text}
                  </p>
                </div>

                {index < stages.length - 1 && (
                  <div
                    className={`mt-8 h-px flex-1 ${
                      state.completed
                        ? "bg-cyan-400/30"
                        : "bg-white/8"
                    }`}
                  />
                )}
              </div>
            );
          })}
        </div>
      </div>

      <div className="grid gap-4 border-t border-white/8 p-5 md:grid-cols-3">
        <div className="rounded-xl border border-white/8 bg-white/[0.025] p-4">
          <p className="text-[9px] uppercase tracking-[0.18em] text-slate-500">
            Cycle
          </p>

          <p className="mt-2 text-sm font-semibold text-slate-200">
            {cycle?.cycle_id || "Waiting"}
          </p>
        </div>

        <div className="rounded-xl border border-white/8 bg-white/[0.025] p-4">
          <p className="text-[9px] uppercase tracking-[0.18em] text-slate-500">
            Status
          </p>

          <p
            className={`mt-2 text-sm font-semibold ${
              status === "COMPLETED"
                ? "text-emerald-300"
                : "text-slate-400"
            }`}
          >
            {status}
          </p>
        </div>

        <div className="rounded-xl border border-white/8 bg-white/[0.025] p-4">
          <p className="text-[9px] uppercase tracking-[0.18em] text-slate-500">
            Confidence
          </p>

          <p className="mt-2 text-sm font-semibold text-cyan-300">
            {confidence !== null
              ? `${confidence}%`
              : "--"}
          </p>
        </div>
      </div>

      <div className="flex items-center justify-between border-t border-white/8 px-5 py-4">
        <p className="text-[9px] text-slate-600">
          {error ||
            "AEGIS autonomous reasoning pipeline"}
        </p>

        <button
          type="button"
          onClick={executeCycle}
          disabled={loading}
          className="flex items-center gap-2 rounded-xl border border-cyan-400/20 bg-cyan-400/5 px-4 py-2 text-[9px] font-bold uppercase tracking-[0.15em] text-cyan-300 transition hover:border-cyan-300/40 hover:bg-cyan-400/10 disabled:cursor-not-allowed disabled:opacity-50"
        >
          <RefreshCw
            className={`h-3.5 w-3.5 ${
              loading ? "animate-spin" : ""
            }`}
          />

          {loading
            ? "RUNNING..."
            : "RUN AUTONOMOUS CYCLE"}
        </button>
      </div>
    </section>
  );
}

export default AutonomousControlLoop;