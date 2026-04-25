from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.assistant import AssistantOutput
from app.services.calendar_service import CalendarService
from app.services.llm_parser import LLMParser
from app.services.vector_memory import VectorMemory


class AssistantService:
    def __init__(self) -> None:
        self.parser = LLMParser()
        self.memory = VectorMemory()
        self.calendar = CalendarService()

    def process_message(self, db: Session, message: str) -> AssistantOutput:
        parsed = self.parser.parse(message)
        recalled = self.memory.recall(message)

        for item in parsed.extracted_tasks:
            existing = db.scalar(select(Task).where(Task.raw_text == item))
            if not existing:
                task = Task(
                    raw_text=item,
                    parsed_intent=parsed.intent,
                    deadline=parsed.suggested_event_time,
                    urgency_score=0.7 if parsed.risk_level in {"high", "critical"} else 0.4,
                    status="pending",
                )
                db.add(task)
        db.commit()
        for item in parsed.extracted_tasks:
            existing = db.scalar(select(Task).where(Task.raw_text == item))
            if existing:
                self.memory.add_task_text(existing.id, existing.raw_text, existing.parsed_intent)

        upcoming = self.calendar.get_upcoming()
        next_actions = parsed.extracted_tasks[:3] + [f"Review upcoming: {event['title']}" for event in upcoming[:1]]
        response = (
            "I mapped your intent and prepped your next actions. "
            f"I also recalled {len(recalled)} memory items to stay context-aware."
        )
        return AssistantOutput(
            response=response,
            next_actions=next_actions,
            priority_focus=["high impact", "deadline alignment", parsed.risk_level],
            intent=parsed,
        )
