from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """
    Custom handler for 422 validation errors to provide clear, frontend-friendly error messages
    """
    if not isinstance(exc, RequestValidationError):
        # Fallback for non-validation errors
        return JSONResponse(
            status_code=422,
            content={
                "status_code": 422,
                "detail": "Validation failed",
                "message": "Please check your input and try again",
                "errors": [str(exc)],
                "field_errors": {},
            },
        )

    errors = []
    field_errors = {}

    for error in exc.errors():
        # Extract field name (skip 'body' from location)
        field_path = error["loc"][1:] if len(error["loc"]) > 1 else error["loc"]
        field_name = " -> ".join(str(loc) for loc in field_path)

        # Get the error message
        message = error["msg"]
        error_type = error["type"]

        # Create user-friendly error messages
        if error_type == "missing":
            friendly_message = f"{field_name} is required"
        elif error_type == "value_error.email":
            friendly_message = f"{field_name} must be a valid email address"
        elif error_type == "string_too_short":
            friendly_message = f"{field_name} is too short"
        elif error_type == "string_too_long":
            friendly_message = f"{field_name} is too long"
        elif error_type == "type_error.str":
            friendly_message = f"{field_name} must be a string"
        elif error_type == "type_error.integer":
            friendly_message = f"{field_name} must be a number"
        elif error_type == "value_error":
            # Handle custom validator errors (like your username/password validators)
            friendly_message = message
        else:
            friendly_message = message

        errors.append(friendly_message)
        field_errors[field_name] = friendly_message

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status_code": 422,
            "detail": "Validation failed",
            "message": "Please check your input and try again",
            "errors": errors,
            "field_errors": field_errors,
        },
    )


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Custom handler for HTTP exceptions to maintain consistent response format
    """
    if not isinstance(exc, HTTPException):
        # Fallback for non-HTTP exceptions
        return JSONResponse(
            status_code=500,
            content={
                "status_code": 500,
                "detail": "Internal server error",
                "message": "An unexpected error occurred",
            },
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "detail": exc.detail,
            "message": exc.detail,
        },
    )
