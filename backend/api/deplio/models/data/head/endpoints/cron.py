from typing import Annotated, Optional
from uuid import UUID

from cron_converter import Cron
from fastapi.exceptions import RequestValidationError
from pydantic import AfterValidator, AwareDatetime, BaseModel

from deplio.models.data.head.db.cron import CronJob, CronJobStatus
from deplio.models.data.head.db.jobs import Executor
from deplio.models.data.head.responses import DeplioResponse


def validate_cron_schedule(schedule: str) -> str:
    try:
        c = Cron(schedule)
        if c.parts is None:
            raise RequestValidationError(
                ['Invalid cron schedule: cron schedule is empty']
            )
    except ValueError as e:
        raise RequestValidationError([f'Invalid cron schedule: {e}']) from e

    return schedule


CronSchedule = Annotated[str, AfterValidator(validate_cron_schedule)]


class GetCronJobsResponse(DeplioResponse):
    cron_jobs: list[CronJob]
    count: int
    total: int
    page: int
    page_size: int


class PostCronJobRequest(BaseModel):
    status: CronJobStatus = CronJobStatus.ACTIVE
    executor: Executor
    schedule: CronSchedule
    metadata: Optional[dict[str, str]] = None


class PostCronJobResponse(DeplioResponse):
    cron_job_id: UUID
    next_invocation: Optional[AwareDatetime] = None


class DeleteCronJobResponse(DeplioResponse):
    cron_job_id: UUID
    scheduled_job_ids: list[UUID]
