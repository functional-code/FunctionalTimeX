from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.assistant import router as assistant_router
from app.api.tasks import router as tasks_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models import Log, Task  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(tasks_router)
app.include_router(assistant_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name}
