from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    parsed_intent: Mapped[str] = mapped_column(String(120), default="general", nullable=False)
    deadline: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    urgency_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
