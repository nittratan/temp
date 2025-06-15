from fastapi import HTTPException
from app.config.error_codes import ErrorCode

class NextGenException(HTTPException):
    def __init__(self, status_code: int = ErrorCode.SERVER_ERROR, detail: str = "An error occurred", headers: dict = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class InvalidPayloadException(NextGenException):
    def __init__(self, detail: str = "Invalid input payload"):
        super().__init__(status_code=ErrorCode.BAD_REQUEST, detail=detail)

class NotFoundException(NextGenException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=ErrorCode.NOT_FOUND, detail=detail)

class UnauthorizedException(NextGenException):
    def __init__(self, detail: str = "Unauthorized access"):
        super().__init__(status_code=ErrorCode.UNAUTHORIZED, detail=detail)

class ForbiddenException(NextGenException):
    def __init__(self, detail: str = "Access forbidden"):
        super().__init__(status_code=ErrorCode.FORBIDDEN, detail=detail)
