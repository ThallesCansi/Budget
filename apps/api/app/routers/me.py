from datetime import UTC, datetime

from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.deps import DB, CurrentProfile, User
from app.core.errors import NotFound
from app.models import Household, HouseholdMember, Profile
from app.schemas.me import HouseholdBrief, HouseholdOut, MemberOut, MeOut, MeUpdate

router = APIRouter(prefix="/v1/me", tags=["me"])


def _me(db: DB, user: User, profile: Profile) -> MeOut:
    memberships = db.execute(
        select(HouseholdMember, Household)
        .join(Household, Household.id == HouseholdMember.household_id)
        .where(HouseholdMember.user_id == user.id)
        .order_by(HouseholdMember.created_at)
    ).all()
    if not memberships:
        raise NotFound("Casa")
    active = next(
        (pair for pair in memberships if pair[1].id == profile.default_household_id),
        memberships[0],
    )
    household = db.scalars(
        select(Household)
        .where(Household.id == active[1].id)
        .options(selectinload(Household.members))
    ).one()
    return MeOut(
        id=profile.id,
        email=user.email,
        full_name=profile.full_name or user.full_name,
        avatar_url=profile.avatar_path or user.avatar_url,
        preferences=profile.preferences,
        onboarded_at=profile.onboarded_at,
        household=HouseholdOut(
            id=household.id,
            name=household.name,
            role=active[0].role,
            members=[MemberOut.model_validate(m) for m in household.members],
        ),
        households=[HouseholdBrief(id=h.id, name=h.name, role=m.role) for m, h in memberships],
    )


@router.get("", response_model=MeOut)
def get_me(db: DB, user: User, profile: CurrentProfile) -> MeOut:
    return _me(db, user, profile)


@router.patch("", response_model=MeOut)
def update_me(db: DB, user: User, profile: CurrentProfile, body: MeUpdate) -> MeOut:
    changes = body.model_dump(exclude_unset=True)
    if "default_household_id" in changes:
        is_member = db.scalar(
            select(HouseholdMember.id).where(
                HouseholdMember.user_id == user.id,
                HouseholdMember.household_id == changes["default_household_id"],
            )
        )
        if is_member is None:
            raise NotFound("Casa")
    if "preferences" in changes:
        changes["preferences"] = {**profile.preferences, **(changes["preferences"] or {})}
    if changes.pop("onboarded", None):
        profile.onboarded_at = profile.onboarded_at or datetime.now(UTC)
    for key, value in changes.items():
        setattr(profile, key, value)
    db.commit()
    return _me(db, user, profile)
