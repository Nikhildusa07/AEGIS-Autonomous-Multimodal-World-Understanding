from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.fusion import router as fusion_router
from app.api.observation import router as observation_router
from app.api.object_detection import (
    router as object_detection_router,
)
from app.api.ocr import router as ocr_router
from app.api.perception import router as perception_router
from app.api.multimodal_perception import (
    router as multimodal_perception_router,
)
from app.api.speech import router as speech_router
from app.api.video import router as video_router
from app.api.scene import router as scene_router
from app.api.embeddings import router as embeddings_router
from app.api.retrieval import router as retrieval_router
from app.api.knowledge import router as knowledge_router
from app.api.spatial import router as spatial_router
from app.api.events import router as events_router
from app.api.planning import router as planning_router
from app.api.execution import router as execution_router
from app.api.verification import router as verification_router
from app.api.observation_loop import (
    router as observation_loop_router,
)
from app.api.replanning import router as replanning_router
from app.api.uncertainty import (
    router as uncertainty_router,
)
from app.api.vision_language import (
    router as vision_language_router,
)
from app.api.autonomous import (
    router as autonomous_router,
)


app = FastAPI(
    title="AEGIS",
    description="Autonomous Environment Grounded Intelligence System",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(observation_router, prefix="/api")
app.include_router(fusion_router, prefix="/api")
app.include_router(perception_router, prefix="/api")
app.include_router(ocr_router, prefix="/api")
app.include_router(object_detection_router, prefix="/api")
app.include_router(multimodal_perception_router, prefix="/api")
app.include_router(speech_router, prefix="/api")
app.include_router(video_router, prefix="/api")
app.include_router(scene_router, prefix="/api")
app.include_router(embeddings_router, prefix="/api")
app.include_router(retrieval_router, prefix="/api")
app.include_router(knowledge_router, prefix="/api")
app.include_router(spatial_router, prefix="/api")
app.include_router(events_router, prefix="/api")
app.include_router(planning_router, prefix="/api")
app.include_router(execution_router, prefix="/api")
app.include_router(verification_router, prefix="/api")

app.include_router(
    observation_loop_router,
    prefix="/api",
)

app.include_router(
    replanning_router,
    prefix="/api",
)

app.include_router(
    uncertainty_router,
    prefix="/api",
)

app.include_router(
    vision_language_router,
    prefix="/api",
)

app.include_router(
    autonomous_router,
    prefix="/api",
)


@app.get("/")
async def root():
    return {
        "project": "AEGIS",
        "full_name": (
            "Autonomous Environment "
            "Grounded Intelligence System"
        ),
        "status": "online",
        "message": (
            "AEGIS multimodal intelligence "
            "system is running."
        ),
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AEGIS Backend",
    }