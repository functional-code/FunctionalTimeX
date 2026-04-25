from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.vector_memory import VectorMemory

router = APIRouter(prefix="/tasks", tags=["tasks"])
vector_memory = VectorMemory()


@router.get("", response_model=list[TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return db.scalars(select(Task).order_by(Task.created_at.desc())).all()


@router.post("", response_model=TaskRead)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(
        raw_text=payload.raw_text,
        parsed_intent=payload.parsed_intent,
        deadline=payload.deadline,
        urgency_score=payload.urgency_score,
        status=payload.status,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    vector_memory.add_task_text(task.id, task.raw_text, task.parsed_intent)
    return task


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    vector_memory.update_task_text(task.id, task.raw_text, task.parsed_intent)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    vector_memory.remove_task_text(task_id)
    return {"status": "deleted", "task_id": task_id}


@router.get("/context/search")
def context_match(query: str, limit: int = 3):
    return {"matches": vector_memory.recall(query=query, limit=limit)}
