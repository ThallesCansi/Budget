import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, Timestamps, UUIDPk, str_enum
from app.models.enums import MemberRole


class Profile(Timestamps, Base):
    """One row per Supabase auth user (`id` = auth.users.id)."""

    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    full_name: Mapped[str | None] = mapped_column(String(120))
    avatar_path: Mapped[str | None] = mapped_column(String(255))
    default_household_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("households.id", ondelete="SET NULL")
    )
    preferences: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, server_default="{}")
    onboarded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Household(UUIDPk, Timestamps, Base):
    __tablename__ = "households"

    name: Mapped[str] = mapped_column(String(80))
    created_by: Mapped[uuid.UUID]

    members: Mapped[list["HouseholdMember"]] = relationship(
        back_populates="household",
        cascade="all, delete-orphan",
        order_by="HouseholdMember.created_at",
    )


class HouseholdMember(UUIDPk, Timestamps, Base):
    """A person in the household. `user_id` is null for people without a login (e.g. kids)."""

    __tablename__ = "household_members"
    __table_args__ = (UniqueConstraint("household_id", "user_id"),)

    household_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("households.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(index=True)
    display_name: Mapped[str] = mapped_column(String(80))
    role: Mapped[MemberRole] = mapped_column(
        str_enum(MemberRole, "member_role"), default=MemberRole.MEMBER
    )
    color: Mapped[str | None] = mapped_column(String(9))

    household: Mapped[Household] = relationship(back_populates="members")


class HouseholdInvite(UUIDPk, Timestamps, Base):
    __tablename__ = "household_invites"

    household_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("households.id", ondelete="CASCADE"), index=True
    )
    email: Mapped[str] = mapped_column(String(255))
    token_hash: Mapped[str] = mapped_column(String(64), unique=True)
    invited_by: Mapped[uuid.UUID]
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    accepted_by: Mapped[uuid.UUID | None]
