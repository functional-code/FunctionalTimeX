from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.assistant import AssistantInput, AssistantOutput
from app.services.assistant_service import AssistantService

router = APIRouter(prefix="/assistant", tags=["assistant"])
service = AssistantService()


@router.post("/parse", response_model=AssistantOutput)
def parse_and_plan(payload: AssistantInput, db: Session = Depends(get_db)):
    return service.process_message(db, payload.message)
