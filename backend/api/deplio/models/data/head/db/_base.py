from typing import cast
from pydantic import AwareDatetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.dialects.postgresql import UUID as SAUUID
from sqlalchemy import TIMESTAMP
import sqlalchemy as sa
import uuid

PostgresUUID = cast(
    'sa.types.TypeEngine[uuid.UUID]',
    SAUUID(as_uuid=True),
)


class Model(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


class DeplioModel(Model):
    __abstract__ = True
    id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID,
        primary_key=True,
        server_default='tuid6()',
        index=True,
        unique=True,
    )


class TimestampedDeplioModel(DeplioModel):
    __abstract__ = True
    created_at: Mapped[AwareDatetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
    )
    deleted_at: Mapped[AwareDatetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )
