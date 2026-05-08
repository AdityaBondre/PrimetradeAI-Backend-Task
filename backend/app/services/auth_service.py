from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime, timedelta, timezone
from app.models.user import User, UserRole
from app.models.refresh_token import RefreshToken
from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from app.core.security import (
    get_password_hash, verify_password, create_access_token, 
    create_refresh_token, hash_token
)
from app.core.exceptions import UnauthorizedException, ConflictException, NotFoundException
import uuid

class AuthService:
    @staticmethod
    async def register(db: AsyncSession, user_in: UserCreate) -> User:
        result = await db.execute(select(User).where(User.email == user_in.email))
        if result.scalar_one_or_none():
            raise ConflictException("Email already registered")
        
        # Check if this is the first user, make them admin
        result = await db.execute(select(User).limit(1))
        is_first_user = result.scalar_one_or_none() is None
        
        db_user = User(
            name=user_in.name,
            email=user_in.email,
            password_hash=get_password_hash(user_in.password),
            role=UserRole.ADMIN if is_first_user else UserRole.USER
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def login(db: AsyncSession, login_data: LoginRequest) -> TokenResponse:
        result = await db.execute(select(User).where(User.email == login_data.email))
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(login_data.password, user.password_hash):
            raise UnauthorizedException("Invalid email or password")
        
        if not user.is_active:
            raise UnauthorizedException("Account is deactivated")

        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)
        
        # Store refresh token hash
        db_refresh_token = RefreshToken(
            user_id=user.id,
            token_hash=hash_token(refresh_token),
            expires_at=datetime.now(timezone.utc) + timedelta(days=7)
        )
        db.add(db_refresh_token)
        await db.commit()
        
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    async def refresh_token(db: AsyncSession, refresh_data: RefreshRequest) -> TokenResponse:
        # In a real app, we would verify the JWT first
        # For this assignment, we'll check the hash in DB
        token_hash = hash_token(refresh_data.refresh_token)
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.expires_at > datetime.now(timezone.utc)
            )
        )
        db_token = result.scalar_one_or_none()
        
        if not db_token:
            raise UnauthorizedException("Invalid or expired refresh token")
            
        user_id = db_token.user_id
        access_token = create_access_token(subject=user_id)
        # Reuse refresh token or rotate? Let's rotate for better security
        new_refresh_token = create_refresh_token(subject=user_id)
        
        db_token.token_hash = hash_token(new_refresh_token)
        db_token.expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        
        await db.commit()
        
        return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)

    @staticmethod
    async def logout(db: AsyncSession, refresh_token: str):
        token_hash = hash_token(refresh_token)
        await db.execute(delete(RefreshToken).where(RefreshToken.token_hash == token_hash))
        await db.commit()
