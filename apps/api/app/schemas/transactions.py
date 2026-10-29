import datetime as dt
from typing import Self
from uuid import UUID

from pydantic import Field, model_validator

from app.models import TransactionKind
from app.schemas.common import Cents, Description, Schema


class TransactionIn(Schema):
    kind: TransactionKind
    account_id: UUID
    to_account_id: UUID | None = None
    category_id: UUID | None = None
    member_id: UUID | None = None
    amount_cents: Cents
    date: dt.date
    description: Description
    notes: str | None = Field(default=None, max_length=2000)
    paid: bool = True
    # Only meaningful for credit cards; computed from the date when omitted.
    invoice_month: dt.date | None = None

    @model_validator(mode="after")
    def _shape(self) -> Self:
        if self.kind == TransactionKind.TRANSFER:
            if self.to_account_id is None:
                raise ValueError("Transferências precisam de uma conta de destino.")
            if self.to_account_id == self.account_id:
                raise ValueError("Origem e destino devem ser contas diferentes.")
            self.category_id = None
        else:
            self.to_account_id = None
        if self.invoice_month is not None:
            self.invoice_month = self.invoice_month.replace(day=1)
        return self


class TransactionOut(Schema):
    id: UUID
    kind: TransactionKind
    account_id: UUID
    to_account_id: UUID | None
    category_id: UUID | None
    member_id: UUID | None
    amount_cents: int
    date: dt.date
    description: str
    notes: str | None
    paid: bool
    invoice_month: dt.date | None
    installment_group_id: UUID | None
    installment_number: int | None
    installment_total: int | None
    recurring_rule_id: UUID | None
    created_at: dt.datetime
    updated_at: dt.datetime


class TransactionPage(Schema):
    items: list[TransactionOut]
    next_cursor: str | None


class MonthSummary(Schema):
    month: dt.date
    income_cents: int
    expense_cents: int
    net_cents: int
    pending_income_cents: int
    pending_expense_cents: int
    balance_cents: int
    projected_balance_cents: int
