from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.dependencies import get_db, get_current_user
from app.core.rbac import allow_roles
from app.models.user import UserRole, User
from app.schemas.user import UserOut, UserUpdate, UserRoleUpdate
from app.services.admin_service import AdminService
from app.utils.response import success_response
import uuid

router = APIRouter(dependencies=[allow_roles([UserRole.ADMIN])])

@router.get("/users", response_model=dict)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    users = await AdminService.get_users(db, skip, limit)
    return success_response(
        "Users fetched successfully", 
        data=[UserOut.model_validate(u) for u in users],
        meta={"skip": skip, "limit": limit, "count": len(users)}
    )

@router.patch("/users/{user_id}", response_model=dict)
async def update_user(
    user_id: uuid.UUID,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    user = await AdminService.update_user(db, user_id, user_in)
    return success_response("User updated successfully", data=UserOut.model_validate(user))

@router.patch("/users/{user_id}/role", response_model=dict)
async def update_user_role(
    user_id: uuid.UUID,
    role_in: UserRoleUpdate,
    db: AsyncSession = Depends(get_db)
):
    user = await AdminService.update_user_role(db, user_id, role_in)
    return success_response("User role updated successfully", data=UserOut.model_validate(user))

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    await AdminService.delete_user(db, user_id)
    return None
