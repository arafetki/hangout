from fastapi import Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from core.logging.logger import logger


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP {exc.status_code} Error: {exc.detail} - Path: {request.url.path}")
    custom_messages = {
        status.HTTP_400_BAD_REQUEST: "The request could not be understood by the server due to malformed syntax.",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "The server encountered a problem and could not process your request.",
    }

    detail = custom_messages.get(exc.status_code, exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": detail})


async def not_found_handler(request: Request, exc: HTTPException):
    detail = "The requested resource could not be found."
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": detail})


async def method_not_allowed_handler(request: Request, exc: HTTPException):
    detail = f"The {request.method} method is not supported for this resource."
    return JSONResponse(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, content={"detail": detail})


async def validation_execption_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation Error: {exc.errors()} - Path: {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "The request could not be processed. Please ensure all fields are valid."},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc} - Path: {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred on the server."},
    )
