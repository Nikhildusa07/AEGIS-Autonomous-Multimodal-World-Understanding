# AEGIS

AEGIS is an autonomous multimodal intelligence system designed to observe an environment, interpret what is happening, decide on actions, execute those actions, verify results, and re-plan when needed.

The project is structured as a full-stack application:

- Backend: Python + FastAPI for perception, reasoning, planning, execution, and verification
- Frontend: React + Vite dashboard for real-time monitoring and visualization
- Domain focus: warehouse / environment monitoring, obstacle awareness, and autonomous decision support

## What this project does

AEGIS models a continuous autonomous loop that mirrors a perception-to-action pipeline:

1. Observe the environment from multiple modalities
2. Reason over visual, audio, OCR, and textual context
3. Estimate uncertainty and confidence
4. Plan safe actions
5. Execute the chosen actions
6. Verify whether the action succeeded
7. Trigger replanning when confidence or verification indicates risk

This is not just a dashboard. The code is built around an autonomous control loop that takes a world state, interprets it, and produces a structured cycle result.

## Project overview

The application is organized around a warehouse-style simulated environment with a person, laptop, obstacle, and sensor readings. The dashboard visualizes a live world model and the autonomous cycle results.

The default sample payload in the frontend includes:

- environment: warehouse
- location: Zone A
- detected_objects: person, laptop
- sensor_readings: obstacle_distance = 2.5 meters
- detected_events: obstacle_detected
- overall confidence around 0.88

This matches the operational narrative of the app: detect an obstacle, interpret the scene, choose a safe path, verify action quality, and continue safely with replanning if conditions change.

## System components

### Frontend

The frontend lives in the `frontend` folder and is built with React and Vite.

Key features:

- 3D warehouse world visualization using React Three Fiber
- glassmorphism-style monitoring dashboard
- multimodal perception cards for vision, audio, sensors, and OCR
- autonomous cycle timeline with stages such as observe, understand, plan, act, verify, and replan
- confidence indicators and event history panels

Main frontend files:

- `frontend/src/App.jsx`
- `frontend/src/pages/Dashboard.jsx`
- `frontend/src/components/WorldView.jsx`
- `frontend/src/components/AutonomousControlLoop.jsx`
- `frontend/src/services/api.js`

### Backend

The backend lives in the `backend` folder and is implemented with FastAPI.

The core FastAPI app in `backend/app/main.py` includes routers for:

- observation
- perception
- OCR
- object detection
- speech
- scene understanding
- embeddings / retrieval / knowledge
- spatial reasoning
- event handling
- planning
- execution
- verification
- autonomous loop execution
- replanning
- uncertainty estimation
- vision-language reasoning

These modules show that the backend is designed as an end-to-end autonomous agent framework rather than a single API.

## Core autonomous loop

The central execution engine is `backend/app/services/autonomous_loop.py`.

The loop does this:

- collects observation inputs
- adds them to the continuous observation stream
- runs vision-language reasoning on the multimodal evidence
- estimates uncertainty from the world state
- converts detected events into planned actions
- executes those actions
- verifies results
- decides whether replanning is needed

The final cycle produces a structured result containing:

- `cycle_id`
- `cycle_number`
- `final_status`
- `should_replan`
- `stages`
- `summary`
- `timestamp`

The backend exposes this cycle through the `/api/autonomous/run` and `/api/autonomous/result` endpoints.

## Architectural modules

The backend is organized by responsibility:

- `app/api/` — HTTP routers and REST endpoints
- `app/environment/` — observation loops, action execution, and verification logic
- `app/planning/` — action planning and replanning engines
- `app/reasoning/` — uncertainty and vision-language reasoning engines
- `app/services/` — orchestration service like the autonomous loop engine
- `app/perception/` and related modules — multimodal sensing and understanding components

## Key design ideas

### Multimodal grounding
The `VisionLanguageReasoningEngine` combines:

- visual detections
- scene descriptions
- OCR text
- audio transcript
- textual context

It computes grounding confidence and modality alignment to support interpretation.

### Action planning
The action planner maps incoming events such as `obstacle_detected`, `entity_present`, or `threshold_exceeded` into executable actions like:

- `avoid_obstacle`
- `inspect_object`
- `monitor_entity`
- `search_entity`
- `respond_to_threshold`

### Verification and replanning
The project explicitly includes both verification and replanning stages. That means the system is designed to validate action success and trigger a new plan when uncertainty or failed verification is detected.

## Data and runtime artifacts

The backend contains runtime directories such as:

- `backend/data/`
- `backend/logs/`
- `backend/uploads/`
- `backend/.env`

The project also includes a YOLO model asset:

- `backend/yolo11n.pt`

This suggests the system is built to support object detection via computer vision models in addition to its orchestration logic.

## Stack summary

### Backend

- Python
- FastAPI
- Pydantic
- OpenCV
- YOLO
- PyTorch / TorchVision
- Transformers
- NumPy / SciPy / scikit-learn
- embedding / retrieval / spatial / multimodal processing libraries

### Frontend

- React
- Vite
- Tailwind-inspired styling
- Framer Motion
- Three.js / React Three Fiber
- Recharts
- Lucide icons

## Repository structure

```text
AEGIS/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── environment/
│   │   ├── memory/
│   │   ├── models/
│   │   ├── perception/
│   │   ├── planning/
│   │   ├── reasoning/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   ├── data/
│   ├── logs/
│   ├── uploads/
│   ├── .env
│   ├── requirements.txt
│   ├── yolo11n.pt
│   └── venv/
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── README.md
└── .gitignore
```

## Intended use

This project is best understood as an intelligent autonomous monitoring and decision system for structured environments. It is designed for a modern simulation or operational dashboard where an AI agent continuously:

- sees the world
- interprets the scene
- decides what to do
- confirms action outcomes
- adjusts itself if the situation is uncertain

## Summary

AEGIS is a multimodal autonomous control system that combines computer vision, language grounding, planning, execution, verification, and replanning into a single loop. The front-end dashboard visualizes that loop for a warehouse-like environment, while the backend API implements the full intelligence stack behind it.

This README is intended to explain the overall system architecture and purpose without executing the application.
