from datetime import datetime

from pydantic import BaseModel, Field


class AssistantInput(BaseModel):
    message: str = Field(min_length=3)


class ParsedIntent(BaseModel):
    intent: str
    confidence: float
    extracted_tasks: list[str]
    suggested_event_time: datetime | None = None
    risk_level: str


class AssistantOutput(BaseModel):
    response: str
    next_actions: list[str]
    priority_focus: list[str]
    intent: ParsedIntent
