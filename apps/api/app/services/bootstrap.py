from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.core.security import CurrentUser
from app.models import Account, Category, Household, HouseholdMember, MemberRole, Profile
from app.services.defaults import DEFAULT_ACCOUNT, default_categories


def _first_name(user: CurrentUser) -> str:
    if user.full_name and user.full_name.strip():
        return user.full_name.strip().split()[0]
    if user.email:
        return user.email.split("@")[0]
    return "Eu"


def create_household(db: Session, user: CurrentUser, name: str) -> Household:
    household = Household(name=name, created_by=user.id)
    db.add(household)
    db.flush()
    db.add(
        HouseholdMember(
            household_id=household.id,
            user_id=user.id,
            display_name=_first_name(user),
            role=MemberRole.OWNER,
        )
    )
    db.add(Account(household_id=household.id, **DEFAULT_ACCOUNT))
    db.add_all(Category(household_id=household.id, **row) for row in default_categories())
    return household


def ensure_profile(db: Session, user: CurrentUser) -> Profile:
    """Returns the user's profile, creating it (plus a starter household) on first access.

    Safe under concurrent first requests: the insert races on the primary key and only the
    winner seeds the household.
    """
    profile = db.get(Profile, user.id)
    if profile is not None:
        return profile

    created = db.execute(
        insert(Profile)
        .values(id=user.id, full_name=user.full_name)
        .on_conflict_do_nothing(index_elements=[Profile.id])
        .returning(Profile.id)
    ).scalar_one_or_none()

    if created is not None:
        household = create_household(db, user, "Minha casa")
        db.flush()
        profile = db.get_one(Profile, user.id)
        profile.default_household_id = household.id
        db.commit()
        return profile

    db.commit()
    return db.scalars(
        select(Profile).where(Profile.id == user.id).execution_options(populate_existing=True)
    ).one()
