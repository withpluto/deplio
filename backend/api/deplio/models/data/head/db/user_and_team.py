from uuid import UUID
from pydantic import AnyUrl
from sqlalchemy import Column, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from ..enums import UserRole, TeamType
from ._base import TimestampedDeplioModel, PostgresUUID
from datetime import date


class DBTeamUser(TimestampedDeplioModel):
    __tablename__ = 'team_user'

    team_id: Column[UUID] = Column('team_id', ForeignKey('team.id'), nullable=False)
    user_id: Column[UUID] = Column('user_id', ForeignKey('user.id'), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        PgEnum(UserRole, name='user_role'),
        nullable=False,
    )


class DBTeam(TimestampedDeplioModel):
    __tablename__ = 'team'

    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    type: Mapped[TeamType] = mapped_column(
        PgEnum(TeamType, name='team_type'),
        nullable=False,
    )
    avatar_url: Mapped[AnyUrl | None] = mapped_column(
        Text,
        nullable=True,
    )
    api_version: Mapped[date] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )

    users: Mapped[list['DBUser']] = relationship(
        secondary=DBTeamUser.__table__,
        back_populates='teams',
    )


class DBUser(TimestampedDeplioModel):
    __tablename__ = 'user'

    user_id: Mapped[UUID] = mapped_column(
        PostgresUUID,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    first_name: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    last_name: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    avatar_url: Mapped[AnyUrl | None] = mapped_column(
        Text,
        nullable=True,
    )

    teams: Mapped[list[DBTeam]] = relationship(
        secondary=DBTeamUser.__table__,
        back_populates='users',
    )
