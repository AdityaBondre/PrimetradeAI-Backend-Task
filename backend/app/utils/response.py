from typing import Any, Optional
from pydantic import BaseModel

class UnifiedResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    meta: Optional[dict] = None

def success_response(message: str, data: Any = None, meta: dict = None) -> dict:
    return {
        "success": True,
        "message": message,
        "data": data,
        "meta": meta
    }

def error_response(message: str, errors: list = None) -> dict:
    return {
        "success": False,
        "message": message,
        "errors": errors or []
    }
