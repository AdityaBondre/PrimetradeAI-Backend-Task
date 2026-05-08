from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from app.schemas.user import UserCreate, UserOut
from app.services.auth_service import AuthService
from app.utils.response import success_response
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await AuthService.register(db, user_in)
    return success_response("User registered successfully", data=UserOut.model_validate(user))

@router.post("/login", response_model=dict)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    tokens = await AuthService.login(db, login_data)
    return success_response("Login successful", data=tokens.model_dump())

@router.post("/refresh", response_model=dict)
async def refresh(refresh_data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    tokens = await AuthService.refresh_token(db, refresh_data)
    return success_response("Token refreshed successfully", data=tokens.model_dump())

@router.post("/logout", response_model=dict)
async def logout(refresh_data: RefreshRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    await AuthService.logout(db, refresh_data.refresh_token)
    return success_response("Logout successful")

@router.get("/me", response_model=dict)
async def get_me(current_user: User = Depends(get_current_user)):
    return success_response("User profile fetched", data=UserOut.model_validate(current_user))
