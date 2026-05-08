from fastapi import HTTPException, status

class UnifiedException(HTTPException):
    def __init__(self, status_code: int, message: str, errors: list = None):
        super().__init__(status_code=status_code, detail={"message": message, "errors": errors or []})

class NotFoundException(UnifiedException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message)

class UnauthorizedException(UnifiedException):
    def __init__(self, message: str = "Could not validate credentials"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, message=message)

class ForbiddenException(UnifiedException):
    def __init__(self, message: str = "Not enough permissions"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, message=message)

class BadRequestException(UnifiedException):
    def __init__(self, message: str = "Bad request", errors: list = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message, errors=errors)

class ConflictException(UnifiedException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, message=message)
