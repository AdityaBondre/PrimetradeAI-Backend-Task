from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_
from typing import List, Optional
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.user import User, UserRole
from app.schemas.task import TaskCreate, TaskUpdate
from app.core.exceptions import NotFoundException, ForbiddenException
import uuid

class TaskService:
    @staticmethod
    async def create_task(db: AsyncSession, user_id: uuid.UUID, task_in: TaskCreate) -> Task:
        db_task = Task(
            **task_in.model_dump(),
            user_id=user_id
        )
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task

    @staticmethod
    async def get_tasks(
        db: AsyncSession, 
        user: User, 
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        query = select(Task)
        
        # Admin sees all, users see their own
        if user.role != UserRole.ADMIN:
            query = query.where(Task.user_id == user.id)
            
        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
            
        query = query.offset(skip).limit(limit).order_by(Task.created_at.desc())
        
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_task_by_id(db: AsyncSession, task_id: uuid.UUID, user: User) -> Task:
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        
        if not task:
            raise NotFoundException("Task not found")
            
        # Ownership check
        if user.role != UserRole.ADMIN and task.user_id != user.id:
            raise ForbiddenException("You don't have access to this task")
            
        return task

    @staticmethod
    async def update_task(db: AsyncSession, task_id: uuid.UUID, user: User, task_in: TaskUpdate) -> Task:
        task = await TaskService.get_task_by_id(db, task_id, user)
        
        update_data = task_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
            
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def delete_task(db: AsyncSession, task_id: uuid.UUID, user: User):
        task = await TaskService.get_task_by_id(db, task_id, user)
        await db.delete(task)
        await db.commit()
