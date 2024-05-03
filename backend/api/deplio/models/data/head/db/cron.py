from enum import StrEnum
from typing import Any, Literal, Optional
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field

from .._base import TimestampedDeplioModel
from .enums import HTTPMethod


class HTTPExecutor(BaseModel):
    type: Literal['http']
    destination: str
    method: HTTPMethod
    body: Optional[str] = None
    headers: Optional[dict[str, str]] = None


class CronJobStatus(StrEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class CronJob(TimestampedDeplioModel):
    team_id: UUID
    api_key_id: UUID
    status: CronJobStatus
    executor: HTTPExecutor = Field(..., discriminator='type')
    schedule: str
    metadata: Optional[dict[str, Any]]


class ScheduledJobStatus(StrEnum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'


class ScheduledJob(TimestampedDeplioModel):
    status: ScheduledJobStatus
    started_at: Optional[AwareDatetime]
    finished_at: Optional[AwareDatetime]
    error: Optional[str]
    metadata: Optional[dict[str, Any]]


class CronInvocation(TimestampedDeplioModel):
    cron_job_id: UUID
    scheduled_job_id: UUID
