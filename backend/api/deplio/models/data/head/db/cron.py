from enum import StrEnum
from typing import Annotated, Any, Literal, Optional
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field

from .._base import TimestampedDeplioModel
from .enums import HTTPMethod


class HTTPExecutorV1(BaseModel):
    type: Literal['http']
    version: Literal[1]
    destination: str
    method: HTTPMethod
    body: Optional[str] = None
    headers: Optional[dict[str, str]] = None


HTTPExecutor = Annotated[HTTPExecutorV1, Field(..., discriminator='version')]

Executor = Annotated[HTTPExecutor, Field(..., discriminator='type')]


class CronJobStatus(StrEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class CronJob(TimestampedDeplioModel):
    team_id: UUID
    api_key_id: UUID
    status: CronJobStatus
    executor: Executor
    schedule: str
    metadata: Optional[dict[str, Any]]


class ScheduledJobStatus(StrEnum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'


class ScheduledJob(TimestampedDeplioModel):
    status: ScheduledJobStatus
    executor: Executor
    scheduled_for: AwareDatetime
    started_at: Optional[AwareDatetime]
    finished_at: Optional[AwareDatetime]
    error: Optional[str]
    metadata: Optional[dict[str, Any]]


class CronInvocation(TimestampedDeplioModel):
    cron_job_id: UUID
    scheduled_job_id: UUID
    metadata: Optional[dict[str, Any]]