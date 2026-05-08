from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.dependencies import get_db, get_current_user
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.services.task_service import TaskService
from app.utils.response import success_response
from app.models.user import User
from app.models.task import TaskStatus, TaskPriority
import uuid

router = APIRouter()

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    task = await TaskService.create_task(db, current_user.id, task_in)
    return success_response("Task created successfully", data=TaskOut.model_validate(task))

@router.get("/", response_model=dict)
async def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = await TaskService.get_tasks(db, current_user, status, priority, skip, limit)
    return success_response(
        "Tasks fetched successfully", 
        data=[TaskOut.model_validate(t) for t in tasks],
        meta={"skip": skip, "limit": limit, "count": len(tasks)}
    )

@router.get("/{task_id}", response_model=dict)
async def get_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = await TaskService.get_task_by_id(db, task_id, current_user)
    return success_response("Task fetched successfully", data=TaskOut.model_validate(task))

@router.put("/{task_id}", response_model=dict)
async def update_task(
    task_id: uuid.UUID,
    task_in: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = await TaskService.update_task(db, task_id, current_user, task_in)
    return success_response("Task updated successfully", data=TaskOut.model_validate(task))

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await TaskService.delete_task(db, task_id, current_user)
    return None
