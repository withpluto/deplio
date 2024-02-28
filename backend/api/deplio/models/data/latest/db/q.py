from pydantic import AnyHttpUrl

from .enums import HTTPMethod
from .._base import TimestampedDeplioModel
from uuid import UUID
from typing import Any, Optional


class QRequest(TimestampedDeplioModel):
    team_id: UUID
    api_key_id: UUID
    destination: AnyHttpUrl
    method: HTTPMethod
    body: Optional[str]
    headers: Optional[dict[str, str]]
    query_params: Optional[dict[str, Any]]


class QResponse(TimestampedDeplioModel):
    request_id: UUID
    status_code: Optional[int]
    body: Optional[str]
    headers: Optional[dict[str, str]]
    response_time_ns: Optional[int]
