from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, ENUM as PgEnum
from ._base import TimestampedDeplioTable
from ..db.jobs import ScheduledJobStatus

scheduled_job_table = TimestampedDeplioTable(
    'scheduled_job',
    Column('team_id', ForeignKey('team.id'), nullable=False),
    Column('api_key_id', ForeignKey('api_key.id'), nullable=False),
    Column(
        'status',
        PgEnum(ScheduledJobStatus, name='scheduled_job_status'),
        nullable=False,
    ),
    Column('executor', JSONB, nullable=False),
    Column('scheduled_for', TIMESTAMP(timezone=True), nullable=False),
    Column('started_at', TIMESTAMP(timezone=True), nullable=True),
    Column('finished_at', TIMESTAMP(timezone=True), nullable=True),
    Column('error', Text, nullable=True),
    Column('metadata', JSONB, nullable=True),
)
