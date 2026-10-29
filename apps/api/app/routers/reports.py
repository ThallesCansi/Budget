import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Query
from sqlalchemy import func, select

from app.core.deps import DB, Ctx
from app.models import Transaction, TransactionKind
from app.schemas.transactions import MonthSummary
from app.services.balances import account_balances
from app.services.invoices import add_months

router = APIRouter(prefix="/v1/reports", tags=["reports"])


@router.get("/summary", response_model=MonthSummary)
def month_summary(
    db: DB,
    ctx: Ctx,
    month: Annotated[dt.date | None, Query(description="Qualquer dia do mês desejado")] = None,
) -> MonthSummary:
    start = (month or dt.date.today()).replace(day=1)
    end = add_months(start, 1)

    def total(kind: TransactionKind, paid: bool) -> int:
        value = db.scalar(
            select(func.coalesce(func.sum(Transaction.amount_cents), 0)).where(
                Transaction.household_id == ctx.household_id,
                Transaction.kind == kind,
                Transaction.paid.is_(paid),
                Transaction.date >= start,
                Transaction.date < end,
            )
        )
        return int(value or 0)

    income = total(TransactionKind.INCOME, True)
    expense = total(TransactionKind.EXPENSE, True)
    balances = account_balances(db, ctx.household_id).values()
    return MonthSummary(
        month=start,
        income_cents=income,
        expense_cents=expense,
        net_cents=income - expense,
        pending_income_cents=total(TransactionKind.INCOME, False),
        pending_expense_cents=total(TransactionKind.EXPENSE, False),
        balance_cents=sum(b.balance_cents for b in balances),
        projected_balance_cents=sum(b.projected_cents for b in balances),
    )
