from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import Field

from app.models import MemberRole
from app.schemas.common import PersonName, Schema


class MemberOut(Schema):
    id: UUID
    user_id: UUID | None
    display_name: str
    role: MemberRole
    color: str | None


class HouseholdOut(Schema):
    id: UUID
    name: str
    role: MemberRole
    members: list[MemberOut]


class HouseholdBrief(Schema):
    id: UUID
    name: str
    role: MemberRole


class MeOut(Schema):
    id: UUID
    email: str | None
    full_name: str | None
    avatar_url: str | None
    preferences: dict[str, Any]
    onboarded_at: datetime | None
    household: HouseholdOut
    households: list[HouseholdBrief]


class MeUpdate(Schema):
    full_name: PersonName | None = None
    avatar_path: str | None = Field(default=None, max_length=255)
    default_household_id: UUID | None = None
    preferences: dict[str, Any] | None = None
    onboarded: bool | None = None
