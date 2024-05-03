from typing import Optional
from uuid import UUID

from pydantic import AwareDatetime, BaseModel

from deplio.models.data.head.db.jobs import Executor


class PostScheduledJobRequest(BaseModel):
    executor: Executor
    schedule_for: AwareDatetime
    metadata: Optional[dict[str, str]] = None


class PostScheduledJobResponse(BaseModel):
    scheduled_job_id: UUID
    next_invocation: Optional[AwareDatetime] = None
