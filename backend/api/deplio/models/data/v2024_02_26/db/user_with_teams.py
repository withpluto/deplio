# THIS FILE WAS AUTO-GENERATED BY CADWYN. DO NOT EVER TRY TO EDIT IT BY HAND

from uuid import UUID
from .enums import UserRole
from .user import User
from .team import Team


class TeamWithRole(Team):
    role: UserRole


class UserWithTeams(User):
    teams: list[TeamWithRole]
    current_team_id: UUID
