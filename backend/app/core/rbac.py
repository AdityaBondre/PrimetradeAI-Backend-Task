from fastapi import Depends
from typing import List
from app.models.user import UserRole, User
from app.core.exceptions import ForbiddenException
from app.dependencies import get_current_user

class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise ForbiddenException(f"Role '{user.role}' is not allowed to access this resource")
        return user

def allow_roles(roles: List[UserRole]):
    return Depends(RoleChecker(roles))
