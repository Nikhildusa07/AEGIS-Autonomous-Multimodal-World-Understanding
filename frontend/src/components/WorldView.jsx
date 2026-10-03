import { useEffect, useMemo, useRef, useState } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import {
  Environment,
  Float,
  Grid,
  Html,
  OrbitControls,
  PerspectiveCamera,
} from "@react-three/drei";

const API_BASE_URL = "http://127.0.0.1:8000/api";

const FALLBACK_OBJECTS = [
  {
    object_id: "person-001",
    label: "person",
    confidence: 0.94,
    position: [-3, 0, -1],
  },
  {
    object_id: "laptop-001",
    label: "laptop",
    confidence: 0.91,
    position: [2.5, 0.8, -1],
  },
];

function WarehouseFloor() {
  return (
    <group>
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, 0, 0]}
      >
        <planeGeometry args={[18, 12]} />

        <meshStandardMaterial
          color="#06101d"
          roughness={0.8}
          metalness={0.2}
        />
      </mesh>

      <Grid
        args={[18, 12]}
        cellSize={1}
        cellThickness={0.7}
        cellColor="#0e7490"
        sectionSize={3}
        sectionThickness={1.2}
        sectionColor="#155e75"
        fadeDistance={20}
        fadeStrength={1}
        infiniteGrid={false}
      />
    </group>
  );
}

function WarehouseWalls() {
  return (
    <group>
      <mesh position={[0, 2, -6]}>
        <boxGeometry args={[18, 4, 0.15]} />

        <meshStandardMaterial
          color="#071426"
          transparent
          opacity={0.7}
          roughness={0.6}
          metalness={0.25}
        />
      </mesh>

      <mesh position={[-9, 2, 0]}>
        <boxGeometry args={[0.15, 4, 12]} />

        <meshStandardMaterial
          color="#071426"
          transparent
          opacity={0.7}
          roughness={0.6}
          metalness={0.25}
        />
      </mesh>

      <mesh position={[9, 2, 0]}>
        <boxGeometry args={[0.15, 4, 12]} />

        <meshStandardMaterial
          color="#071426"
          transparent
          opacity={0.7}
          roughness={0.6}
          metalness={0.25}
        />
      </mesh>
    </group>
  );
}

function PersonModel({ position, confidence }) {
  const ringRef = useRef();

  useFrame((state) => {
    if (!ringRef.current) {
      return;
    }

    const pulse =
      1 +
      Math.sin(state.clock.elapsedTime * 2.5) * 0.12;

    ringRef.current.scale.set(
      pulse,
      pulse,
      pulse
    );

    ringRef.current.material.opacity =
      0.35 +
      Math.sin(state.clock.elapsedTime * 2.5) * 0.15;
  });

  return (
    <group position={position}>
      <Float
        speed={1.8}
        rotationIntensity={0.08}
        floatIntensity={0.12}
      >
        <mesh position={[0, 1.25, 0]}>
          <sphereGeometry args={[0.35, 24, 24]} />

          <meshStandardMaterial
            color="#22d3ee"
            emissive="#0891b2"
            emissiveIntensity={2}
          />
        </mesh>

        <mesh position={[0, 0.45, 0]}>
          <capsuleGeometry args={[0.42, 0.9, 8, 16]} />

          <meshStandardMaterial
            color="#0e7490"
            emissive="#0891b2"
            emissiveIntensity={0.7}
          />
        </mesh>
      </Float>

      <mesh
        ref={ringRef}
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, 0.035, 0]}
      >
        <ringGeometry args={[0.65, 0.73, 48]} />

        <meshBasicMaterial
          color="#22d3ee"
          transparent
          opacity={0.5}
        />
      </mesh>

      <Html
        position={[0, 1.9, 0]}
        center
        distanceFactor={10}
      >
        <div className="pointer-events-none whitespace-nowrap rounded-lg border border-cyan-400/25 bg-slate-950/90 px-2.5 py-1.5 text-center shadow-xl backdrop-blur">
          <p className="text-[8px] font-bold uppercase tracking-[0.15em] text-cyan-300">
            PERSON
          </p>

          <p className="mt-0.5 text-[8px] text-slate-400">
            {Math.round(confidence * 100)}% confidence
          </p>
        </div>
      </Html>
    </group>
  );
}

function LaptopModel({ position, confidence }) {
  return (
    <group position={position}>
      <mesh position={[0, 0.3, 0]}>
        <boxGeometry args={[1.5, 0.08, 0.9]} />

        <meshStandardMaterial
          color="#312e81"
          emissive="#4338ca"
          emissiveIntensity={0.4}
          metalness={0.7}
          roughness={0.3}
        />
      </mesh>

      <mesh
        position={[0, 0.8, -0.32]}
        rotation={[-0.25, 0, 0]}
      >
        <boxGeometry args={[1.25, 0.8, 0.08]} />

        <meshStandardMaterial
          color="#7c3aed"
          emissive="#6d28d9"
          emissiveIntensity={0.6}
          metalness={0.5}
          roughness={0.25}
        />
      </mesh>

      <mesh
        position={[0, 0.8, -0.275]}
        rotation={[-0.25, 0, 0]}
      >
        <planeGeometry args={[0.95, 0.55]} />

        <meshBasicMaterial color="#22d3ee" />
      </mesh>

      <Html
        position={[0, 1.55, 0]}
        center
        distanceFactor={10}
      >
        <div className="pointer-events-none whitespace-nowrap rounded-lg border border-violet-400/25 bg-slate-950/90 px-2.5 py-1.5 text-center shadow-xl backdrop-blur">
          <p className="text-[8px] font-bold uppercase tracking-[0.15em] text-violet-300">
            LAPTOP
          </p>

          <p className="mt-0.5 text-[8px] text-slate-400">
            {Math.round(confidence * 100)}% confidence
          </p>
        </div>
      </Html>
    </group>
  );
}

function GenericObject({ position, label, confidence }) {
  return (
    <group position={position}>
      <mesh position={[0, 0.55, 0]}>
        <boxGeometry args={[0.9, 1.1, 0.9]} />

        <meshStandardMaterial
          color="#0e7490"
          emissive="#0891b2"
          emissiveIntensity={0.5}
        />
      </mesh>

      <Html
        position={[0, 1.35, 0]}
        center
        distanceFactor={10}
      >
        <div className="pointer-events-none whitespace-nowrap rounded-lg border border-cyan-400/20 bg-slate-950/90 px-2.5 py-1.5 text-center backdrop-blur">
          <p className="text-[8px] font-bold uppercase tracking-[0.15em] text-cyan-300">
            {label}
          </p>

          <p className="mt-0.5 text-[8px] text-slate-400">
            {Math.round(confidence * 100)}%
          </p>
        </div>
      </Html>
    </group>
  );
}

function DetectedObjects({ objects }) {
  const fallbackPositions = [
    [-3, 0, -1],
    [2.5, 0.8, -1],
    [4, 0, -2],
    [-1, 0, 3],
  ];

  return (
    <>
      {objects.map((object, index) => {
        const label = String(
          object.label || "object"
        ).toLowerCase();

        const confidence = Number(
          object.confidence ?? 0
        );

        const position =
          Array.isArray(object.position)
            ? object.position
            : fallbackPositions[
                index % fallbackPositions.length
              ];

        if (label.includes("person")) {
          return (
            <PersonModel
              key={object.object_id || `person-${index}`}
              position={position}
              confidence={confidence}
            />
          );
        }

        if (
          label.includes("laptop") ||
          label.includes("computer")
        ) {
          return (
            <LaptopModel
              key={object.object_id || `laptop-${index}`}
              position={position}
              confidence={confidence}
            />
          );
        }

        return (
          <GenericObject
            key={object.object_id || `object-${index}`}
            position={position}
            label={label}
            confidence={confidence}
          />
        );
      })}
    </>
  );
}

function ObstacleModel({
  distance,
  severity,
  eventConfidence,
}) {
  const obstacleRef = useRef();

  const isCritical =
    severity === "critical" ||
    (distance !== null && distance < 1);

  useFrame((state) => {
    if (!obstacleRef.current) {
      return;
    }

    const speed = isCritical ? 5 : 3;

    const pulse =
      1 +
      Math.sin(
        state.clock.elapsedTime * speed
      ) *
        (isCritical ? 0.12 : 0.06);

    obstacleRef.current.scale.set(
      pulse,
      pulse,
      pulse
    );

    obstacleRef.current.rotation.y +=
      isCritical ? 0.008 : 0.003;
  });

  return (
    <group position={[0, 0.65, 2]}>
      <mesh ref={obstacleRef}>
        <boxGeometry args={[1.2, 1.2, 1.2]} />

        <meshStandardMaterial
          color={isCritical ? "#991b1b" : "#78350f"}
          emissive={isCritical ? "#ef4444" : "#f59e0b"}
          emissiveIntensity={isCritical ? 2.2 : 1.5}
          transparent
          opacity={0.9}
          roughness={0.35}
          metalness={0.25}
        />
      </mesh>

      <mesh scale={[1.15, 1.15, 1.15]}>
        <boxGeometry args={[1.2, 1.2, 1.2]} />

        <meshBasicMaterial
          color={
            isCritical
              ? "#ef4444"
              : "#f59e0b"
          }
          wireframe
          transparent
          opacity={0.5}
        />
      </mesh>

      <Html
        position={[0, 1.45, 0]}
        center
        distanceFactor={10}
      >
        <div
          className={`pointer-events-none whitespace-nowrap rounded-lg border px-3 py-2 text-center shadow-xl backdrop-blur ${
            isCritical
              ? "border-red-400/40 bg-red-950/90"
              : "border-amber-400/30 bg-amber-950/85"
          }`}
        >
          <p
            className={`text-[8px] font-bold uppercase tracking-[0.15em] ${
              isCritical
                ? "text-red-300"
                : "text-amber-300"
            }`}
          >
            {isCritical
              ? "CRITICAL OBSTACLE"
              : "OBSTACLE"}
          </p>

          <p className="mt-1 text-[8px] text-slate-300">
            {distance !== null
              ? `${distance} m distance`
              : "Detected"}
          </p>

          {eventConfidence !== null && (
            <p className="text-[8px] text-slate-500">
              {Math.round(
                eventConfidence * 100
              )}
              % confidence
            </p>
          )}
        </div>
      </Html>
    </group>
  );
}

function SafePath({ active }) {
  const pathRef = useRef();

  useFrame((state) => {
    if (!pathRef.current) {
      return;
    }

    pathRef.current.material.opacity = active
      ? 0.55 +
        Math.sin(
          state.clock.elapsedTime * 3
        ) *
          0.25
      : 0.18;
  });

  return (
    <group>
      <mesh
        ref={pathRef}
        position={[2, 0.04, 2]}
        rotation={[-Math.PI / 2, 0, -0.35]}
      >
        <planeGeometry args={[7, 0.14]} />

        <meshBasicMaterial
          color="#22d3ee"
          transparent
          opacity={active ? 0.8 : 0.18}
        />
      </mesh>

      <mesh position={[5.2, 0.07, 0.85]}>
        <sphereGeometry args={[0.14, 16, 16]} />

        <meshBasicMaterial color="#67e8f9" />
      </mesh>

      {active && (
        <Html
          position={[4.3, 0.25, 1]}
          center
          distanceFactor={10}
        >
          <div className="pointer-events-none whitespace-nowrap rounded-lg border border-cyan-400/25 bg-slate-950/90 px-3 py-2 shadow-xl backdrop-blur">
            <p className="text-[8px] font-bold uppercase tracking-[0.15em] text-cyan-300">
              SAFE PATH
            </p>

            <p className="mt-1 text-[8px] text-slate-400">
              AEGIS selected route
            </p>
          </div>
        </Html>
      )}
    </group>
  );
}

function Scene({
  objects,
  obstacleDistance,
  obstacleSeverity,
  obstacleConfidence,
  actionActive,
}) {
  return (
    <>
      <PerspectiveCamera
        makeDefault
        position={[8, 6, 8]}
        fov={48}
      />

      <ambientLight intensity={0.65} />

      <directionalLight
        position={[5, 10, 5]}
        intensity={2.5}
      />

      <pointLight
        position={[-4, 4, 2]}
        intensity={18}
        distance={12}
        color="#22d3ee"
      />

      <pointLight
        position={[4, 3, -2]}
        intensity={12}
        distance={10}
        color="#7c3aed"
      />

      <Environment preset="night" />

      <WarehouseFloor />

      <WarehouseWalls />

      <DetectedObjects objects={objects} />

      <ObstacleModel
        distance={obstacleDistance}
        severity={obstacleSeverity}
        eventConfidence={obstacleConfidence}
      />

      <SafePath active={actionActive} />

      <OrbitControls
        enableDamping
        dampingFactor={0.08}
        minDistance={5}
        maxDistance={18}
        maxPolarAngle={Math.PI / 2.05}
        target={[0, 0.5, 0]}
      />
    </>
  );
}

function WorldView() {
  const [autonomousResult, setAutonomousResult] =
    useState(null);

  const [observationState, setObservationState] =
    useState(null);

  const [backendConnected, setBackendConnected] =
    useState(false);

  useEffect(() => {
    let mounted = true;

    const fetchBackendState = async () => {
      try {
        const [
          autonomousResponse,
          observationResponse,
        ] = await Promise.all([
          fetch(
            `${API_BASE_URL}/autonomous/result`
          ),
          fetch(
            `${API_BASE_URL}/observation-loop/world-state`
          ),
        ]);

        if (!mounted) {
          return;
        }

        if (
          autonomousResponse.ok
        ) {
          const autonomousData =
            await autonomousResponse.json();

          setAutonomousResult(
            autonomousData?.result ?? null
          );
        }

        if (
          observationResponse.ok
        ) {
          const observationData =
            await observationResponse.json();

          setObservationState(
            observationData?.result
              ?.world_state ?? null
          );
        }

        setBackendConnected(true);
      } catch {
        if (!mounted) {
          return;
        }

        setBackendConnected(false);
      }
    };

    fetchBackendState();

    const interval = setInterval(
      fetchBackendState,
      3000
    );

    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  const worldState =
    autonomousResult?.world_state ||
    observationState ||
    {};

  const detectedObjects = useMemo(() => {
    const objects =
      worldState?.detected_objects;

    if (
      Array.isArray(objects) &&
      objects.length > 0
    ) {
      return objects;
    }

    return FALLBACK_OBJECTS;
  }, [worldState]);

  const sensorReadings =
    Array.isArray(
      worldState?.sensor_readings
    )
      ? worldState.sensor_readings
      : [];

  const obstacleSensor =
    sensorReadings.find(
      (sensor) =>
        String(
          sensor?.sensor_name || ""
        ).toLowerCase() ===
          "obstacle_distance" ||
        String(
          sensor?.sensor_name || ""
        ).toLowerCase() ===
          "distance"
    );

  const obstacleDistance =
    obstacleSensor?.value !== undefined
      ? Number(obstacleSensor.value)
      : null;

  const events =
    Array.isArray(
      worldState?.detected_events
    )
      ? worldState.detected_events
      : [];

  const obstacleEvent =
    events.find((event) =>
      String(
        event?.event_type || ""
      )
        .toLowerCase()
        .includes("obstacle")
    );

  const obstacleSeverity =
    String(
      obstacleEvent?.severity || "normal"
    ).toLowerCase();

  const obstacleConfidence =
    obstacleEvent?.confidence !== undefined
      ? Number(obstacleEvent.confidence)
      : null;

  const execution =
    autonomousResult?.stages
      ?.action_execution
      ?.executions?.[0]
      ?.execution;

  const verification =
    autonomousResult?.stages
      ?.action_verification
      ?.verifications?.[0]
      ?.verification;

  const actionActive =
    Boolean(execution?.success) ||
    Boolean(
      autonomousResult?.stages
        ?.action_planning
        ?.actions?.length
    );

  const environment =
    worldState?.environment ||
    "warehouse";

  const location =
    worldState?.location ||
    "Zone A";

  const observationCount =
    worldState?.observations?.length ??
    0;

  const objectCount =
    worldState?.detected_objects
      ?.length ??
    detectedObjects.length;

  const verified =
    verification?.verified === true;

  return (
    <div className="relative h-[440px] w-full overflow-hidden rounded-b-2xl bg-[#030b18]">
      <Canvas
        className="!block"
        style={{
          width: "100%",
          height: "100%",
          display: "block",
        }}
        dpr={[1, 2]}
        gl={{
          antialias: true,
          alpha: true,
        }}
      >
        <Scene
          objects={detectedObjects}
          obstacleDistance={
            obstacleDistance
          }
          obstacleSeverity={
            obstacleSeverity
          }
          obstacleConfidence={
            obstacleConfidence
          }
          actionActive={actionActive}
        />
      </Canvas>

      <div className="pointer-events-none absolute left-5 top-5 z-10">
        <p className="text-[8px] uppercase tracking-[0.25em] text-cyan-400/60">
          LIVE WORLD STATE
        </p>

        <p className="mt-1 text-xs font-semibold text-slate-200">
          {environment.toUpperCase()} /{" "}
          {location.toUpperCase()}
        </p>
      </div>

      <div className="pointer-events-none absolute right-5 top-5 z-10 space-y-2">
        {obstacleDistance !== null && (
          <div className="rounded-lg border border-amber-400/20 bg-black/50 px-3 py-2 text-right backdrop-blur">
            <p className="text-[7px] uppercase tracking-[0.16em] text-slate-500">
              OBSTACLE DISTANCE
            </p>

            <p className="mt-0.5 text-xs font-bold text-amber-300">
              {obstacleDistance} m
            </p>
          </div>
        )}

        {execution && (
          <div className="rounded-lg border border-cyan-400/20 bg-black/50 px-3 py-2 text-right backdrop-blur">
            <p className="text-[7px] uppercase tracking-[0.16em] text-slate-500">
              ACTION
            </p>

            <p className="mt-0.5 text-[8px] font-bold uppercase text-cyan-300">
              {execution.action_type ||
                "executing"}
            </p>
          </div>
        )}

        {verified && (
          <div className="rounded-lg border border-emerald-400/20 bg-black/50 px-3 py-2 text-right backdrop-blur">
            <p className="text-[7px] uppercase tracking-[0.16em] text-slate-500">
              STATUS
            </p>

            <p className="mt-0.5 text-[8px] font-bold uppercase text-emerald-300">
              ACTION VERIFIED
            </p>
          </div>
        )}
      </div>

      <div className="pointer-events-none absolute bottom-4 left-4 z-10 flex items-center gap-2 rounded-lg border border-white/8 bg-black/50 px-3 py-2 backdrop-blur">
        <span
          className={`h-2 w-2 rounded-full ${
            backendConnected
              ? "animate-pulse bg-emerald-400"
              : "bg-amber-400"
          }`}
        />

        <span className="text-[8px] uppercase tracking-[0.16em] text-slate-400">
          {backendConnected
            ? "Backend synchronized"
            : "Backend unavailable"}
        </span>

        {backendConnected && (
          <span className="text-[8px] text-slate-600">
            {observationCount} observations
          </span>
        )}
      </div>

      <div className="pointer-events-none absolute bottom-4 right-4 z-10 rounded-lg border border-white/8 bg-black/50 px-3 py-2 backdrop-blur">
        <span className="text-[8px] uppercase tracking-[0.16em] text-slate-500">
          OBJECTS
        </span>

        <span className="ml-2 text-xs font-semibold text-slate-200">
          {objectCount}
        </span>
      </div>
    </div>
  );
}

export default WorldView;