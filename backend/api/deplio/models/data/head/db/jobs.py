from enum import StrEnum
from typing import Annotated, Any, Literal, Optional
from uuid import UUID

from pydantic import AnyHttpUrl, AwareDatetime, BaseModel, Field

from .._base import TimestampedDeplioModel
from .enums import HTTPMethod


class HTTPExecutorV1(BaseModel):
    type: Literal['http']
    version: Literal[1]
    destination: AnyHttpUrl
    method: HTTPMethod
    body: Optional[str] = None
    headers: Optional[dict[str, str]] = None


HTTPExecutor = Annotated[HTTPExecutorV1, Field(..., discriminator='version')]

Executor = Annotated[HTTPExecutor, Field(..., discriminator='type')]


class ScheduledJobStatus(StrEnum):
    pending = 'pending'
    running = 'running'
    completed = 'completed'
    failed = 'failed'


class ScheduledJob(TimestampedDeplioModel):
    team_id: UUID
    api_key_id: UUID
    status: ScheduledJobStatus
    executor: Executor
    scheduled_for: AwareDatetime
    started_at: Optional[AwareDatetime]
    finished_at: Optional[AwareDatetime]
    error: Optional[str]
    metadata: Optional[dict[str, Any]]
