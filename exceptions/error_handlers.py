from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from schemas.error import ErrorResponse
from exceptions.exceptions import AppException
from messages.message_source import MessageSource


def register_exception_handlers(app: FastAPI, message_source: MessageSource) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        message = message_source.get_message(exc.message_key, exc.params, default=exc.message_key)
        body = ErrorResponse(code=exc.code, message=message, details=exc.details).dict()
        return JSONResponse(status_code=exc.http_status, content=body)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        # Preserve existing status code, map to generic code
        body = ErrorResponse(
            code="HTTP_ERROR",
            message=str(exc.detail) if exc.detail else "HTTP error",
            details={"path": str(request.url), "method": request.method},
        ).dict()
        return JSONResponse(status_code=exc.status_code, content=body)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        body = ErrorResponse(
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details={"errors": exc.errors()},
        ).dict()
        return JSONResponse(status_code=422, content=body)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        body = ErrorResponse(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred",
            details={"path": str(request.url)},
        ).dict()
        return JSONResponse(status_code=500, content=body)
