from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List
from app.models.user import User, UserRole
from app.schemas.user import UserUpdate, UserRoleUpdate
from app.core.exceptions import NotFoundException
import uuid

class AdminService:
    @staticmethod
    async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        result = await db.execute(select(User).offset(skip).limit(limit).order_by(User.created_at.desc()))
        return result.scalars().all()

    @staticmethod
    async def update_user(db: AsyncSession, user_id: uuid.UUID, user_in: UserUpdate) -> User:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User not found")
            
        update_data = user_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
            
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def update_user_role(db: AsyncSession, user_id: uuid.UUID, role_in: UserRoleUpdate) -> User:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User not found")
            
        user.role = role_in.role
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: uuid.UUID):
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User not found")
            
        await db.delete(user)
        await db.commit()
