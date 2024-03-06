# THIS FILE WAS AUTO-GENERATED BY CADWYN. DO NOT EVER TRY TO EDIT IT BY HAND

import abc
from datetime import UTC, datetime
from typing import Any, Optional
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse


class DeplioWarning(BaseModel):
    message: str
    data: Optional[dict[str, Any]] = None


class DeplioError(BaseModel):
    message: str
    data: Optional[dict[str, Any]] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class DeplioResponse(BaseModel, abc.ABC):
    warnings: list[DeplioWarning]


class ErrorResponse(DeplioResponse):
    message: str
    errors: list[DeplioError]


def error_responses() -> dict[int | str, dict[str, Any]]:
    return {
        400: {'model': ErrorResponse, 'description': 'The request was invalid.'},
        401: {
            'model': ErrorResponse,
            'description': 'The request was not authenticated.',
        },
        403: {
            'model': ErrorResponse,
            'description': 'The authenticated party does not have permission to perform the requested action.',
        },
        500: {
            'model': ErrorResponse,
            'description': 'An internal error occurred while processing the request.',
        },
    }


def generate_responses(
    ok_response_model: type[DeplioResponse],
) -> dict[int | str, dict[str, Any]]:
    return {**error_responses(), 200: {'model': ok_response_model}}


def error_response(
    status_code: int,
    message: str,
    errors: list[DeplioError],
    warnings: list[DeplioWarning],
    **kwargs: Any,
) -> JSONResponse:
    model = error_responses().get(status_code, {'model': ErrorResponse})['model']
    if isinstance(model, str):
        model = ErrorResponse
    error = model(message=message, errors=errors, warnings=warnings, **kwargs)
    return JSONResponse(status_code=status_code, content=error.model_dump())
