from typing import Annotated, Self
from uuid import UUID

from pydantic import Field, model_validator

from app.models import AccountKind, CategoryKind
from app.schemas.common import Cents, Color, Icon, Name, Schema, SignedCents

Day = Annotated[int, Field(ge=1, le=31)]


class AccountIn(Schema):
    name: Name
    kind: AccountKind
    initial_balance_cents: SignedCents = 0
    color: Color = "#2b478b"
    icon: Icon = "wallet"
    credit_limit_cents: Cents | None = None
    closing_day: Day | None = None
    due_day: Day | None = None

    @model_validator(mode="after")
    def _card_fields(self) -> Self:
        if self.kind == AccountKind.CREDIT_CARD:
            if self.closing_day is None or self.due_day is None:
                raise ValueError("Cartões precisam de dia de fechamento e de vencimento.")
        else:
            self.credit_limit_cents = self.closing_day = self.due_day = None
        return self


class AccountUpdate(Schema):
    name: Name | None = None
    initial_balance_cents: SignedCents | None = None
    color: Color | None = None
    icon: Icon | None = None
    archived: bool | None = None
    position: int | None = Field(default=None, ge=0, le=1000)
    credit_limit_cents: Cents | None = None
    closing_day: Day | None = None
    due_day: Day | None = None


class AccountOut(Schema):
    id: UUID
    name: str
    kind: AccountKind
    initial_balance_cents: int
    color: str
    icon: str
    archived: bool
    position: int
    credit_limit_cents: int | None
    closing_day: int | None
    due_day: int | None
    balance_cents: int = 0
    projected_balance_cents: int = 0


class CategoryIn(Schema):
    name: Name
    kind: CategoryKind
    color: Color = "#98a6af"
    icon: Icon = "tag"


class CategoryUpdate(Schema):
    name: Name | None = None
    color: Color | None = None
    icon: Icon | None = None
    archived: bool | None = None
    position: int | None = Field(default=None, ge=0, le=1000)


class CategoryOut(Schema):
    id: UUID
    name: str
    kind: CategoryKind
    color: str
    icon: str
    archived: bool
    position: int
