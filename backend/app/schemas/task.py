from datetime import datetime

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    raw_text: str = Field(min_length=3)
    parsed_intent: str = Field(default="general", min_length=1, max_length=120)
    deadline: datetime | None = None
    urgency_score: float = Field(default=0.0, ge=0, le=1)
    status: str = Field(default="pending", min_length=1, max_length=20)


class TaskUpdate(BaseModel):
    raw_text: str | None = Field(default=None, min_length=3)
    parsed_intent: str | None = Field(default=None, min_length=1, max_length=120)
    deadline: datetime | None = None
    urgency_score: float | None = Field(default=None, ge=0, le=1)
    status: str | None = Field(default=None, min_length=1, max_length=20)


class TaskRead(TaskCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
