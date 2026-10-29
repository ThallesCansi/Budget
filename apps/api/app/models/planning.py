import datetime as dt
import uuid

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, Timestamps, UUIDPk


class Budget(UUIDPk, Timestamps, Base):
    __tablename__ = "budgets"
    __table_args__ = (
        UniqueConstraint("category_id", "month"),
        CheckConstraint("amount_cents > 0", name="amount_positive"),
    )

    household_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("households.id", ondelete="CASCADE"), index=True
    )
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    month: Mapped[dt.date] = mapped_column(Date)
    amount_cents: Mapped[int] = mapped_column(BigInteger)


class Goal(UUIDPk, Timestamps, Base):
    __tablename__ = "goals"
    __table_args__ = (CheckConstraint("target_cents > 0", name="target_positive"),)

    household_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("households.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(80))
    target_cents: Mapped[int] = mapped_column(BigInteger)
    target_date: Mapped[dt.date | None] = mapped_column(Date)
    color: Mapped[str] = mapped_column(String(9), default="#56ab91")
    icon: Mapped[str] = mapped_column(String(40), default="target")
    description: Mapped[str | None] = mapped_column(Text)
    account_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("accounts.id", ondelete="SET NULL")
    )
    achieved_at: Mapped[dt.datetime | None] = mapped_column(DateTime(timezone=True))
    archived: Mapped[bool] = mapped_column(Boolean, default=False)


class GoalContribution(UUIDPk, Timestamps, Base):
    __tablename__ = "goal_contributions"
    __table_args__ = (CheckConstraint("amount_cents <> 0", name="amount_nonzero"),)

    goal_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("goals.id", ondelete="CASCADE"), index=True
    )
    household_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("households.id", ondelete="CASCADE"))
    # Negative values are withdrawals.
    amount_cents: Mapped[int] = mapped_column(BigInteger)
    date: Mapped[dt.date] = mapped_column(Date)
    note: Mapped[str | None] = mapped_column(String(140))
