from dataclasses import dataclass
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.errors import Forbidden, NotFound
from app.core.security import CurrentUser, get_current_user
from app.models import HouseholdMember, MemberRole, Profile
from app.services.bootstrap import ensure_profile

DB = Annotated[Session, Depends(get_db)]
User = Annotated[CurrentUser, Depends(get_current_user)]


def get_profile(db: DB, user: User) -> Profile:
    return ensure_profile(db, user)


CurrentProfile = Annotated[Profile, Depends(get_profile)]


@dataclass(frozen=True, slots=True)
class HouseholdContext:
    user: CurrentUser
    household_id: UUID
    member_id: UUID
    role: MemberRole

    def require_owner(self) -> None:
        if self.role != MemberRole.OWNER:
            raise Forbidden("Apenas o dono da casa pode fazer isso.")


def get_household(
    db: DB,
    user: User,
    profile: CurrentProfile,
    x_household_id: Annotated[UUID | None, Header()] = None,
) -> HouseholdContext:
    """Resolves the active household (header or profile default) and checks membership."""
    query = select(HouseholdMember).where(HouseholdMember.user_id == user.id)
    household_id = x_household_id or profile.default_household_id
    if household_id is not None:
        member = db.scalar(query.where(HouseholdMember.household_id == household_id))
    else:
        member = db.scalar(query.order_by(HouseholdMember.created_at).limit(1))
    if member is None:
        raise NotFound("Casa")
    return HouseholdContext(
        user=user, household_id=member.household_id, member_id=member.id, role=member.role
    )


Ctx = Annotated[HouseholdContext, Depends(get_household)]
