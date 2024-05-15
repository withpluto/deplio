from sqlalchemy import ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from .api_key import DBAPIKey
from .user_and_team import DBTeam

from ..enums import HTTPMethod
from ._base import TimestampedDeplioModel
from uuid import UUID


class DBQRequest(TimestampedDeplioModel):
    __tablename__ = 'q_request'

    team_id: Mapped[UUID] = mapped_column(
        ForeignKey('team.id'),
        nullable=False,
    )
    team: Mapped[DBTeam] = relationship()

    api_key_id: Mapped[UUID] = mapped_column(
        ForeignKey('api_key.id'),
        nullable=False,
    )
    api_key: Mapped[DBAPIKey] = relationship()

    destination: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    method: Mapped[HTTPMethod] = mapped_column(
        Text,
        nullable=False,
    )
    body: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    headers: Mapped[dict[str, str] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    query_params: Mapped[dict[str, str] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    responses: Mapped[list['DBQResponse']] = relationship(
        back_populates='request',
        order_by='DBQResponse.created_at.desc()',
    )


class DBQResponse(TimestampedDeplioModel):
    __tablename__ = 'q_response'

    request_id: Mapped[UUID] = mapped_column(
        ForeignKey('q_request.id'),
        nullable=False,
    )
    request: Mapped[DBQRequest] = relationship(
        back_populates='responses',
    )

    status_code: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    body: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    headers: Mapped[dict[str, str] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    response_time_ns: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
