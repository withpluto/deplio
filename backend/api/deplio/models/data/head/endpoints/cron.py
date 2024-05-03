from typing import Annotated, Optional

from cron_converter import Cron
from fastapi.exceptions import RequestValidationError
from pydantic import AfterValidator, BaseModel

from deplio.models.data.head.db.cron import CronJobStatus, HTTPExecutor


def validate_cron_schedule(schedule: str) -> str:
    try:
        c = Cron(schedule)
        if c.parts is None:
            raise RequestValidationError(
                ["Invalid cron schedule: cron schedule is empty"]
            )
    except ValueError as e:
        raise RequestValidationError([f"Invalid cron schedule: {e}"]) from e

    return schedule


CronSchedule = Annotated[str, AfterValidator(validate_cron_schedule)]


class PostCronJobRequest(BaseModel):
    status: CronJobStatus = CronJobStatus.ACTIVE
    executor: HTTPExecutor
    schedule: CronSchedule
    metadata: Optional[dict[str, str]] = None
