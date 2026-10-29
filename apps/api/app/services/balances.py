from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import case, func, literal, select, union_all
from sqlalchemy.orm import Session

from app.models import Account, Transaction, TransactionKind


@dataclass(frozen=True, slots=True)
class Balance:
    balance_cents: int
    projected_cents: int


def account_balances(db: Session, household_id: UUID) -> dict[UUID, Balance]:
    """Balance per account: initial balance + movements. `projected` includes unpaid entries."""
    outflow = case(
        (Transaction.kind == TransactionKind.INCOME, Transaction.amount_cents),
        else_=-Transaction.amount_cents,
    )
    movements = union_all(
        select(
            Transaction.account_id.label("account_id"),
            outflow.label("delta"),
            Transaction.paid.label("paid"),
        ).where(Transaction.household_id == household_id),
        select(
            Transaction.to_account_id,
            Transaction.amount_cents,
            Transaction.paid,
        ).where(
            Transaction.household_id == household_id,
            Transaction.kind == TransactionKind.TRANSFER,
        ),
    ).subquery()

    totals = (
        select(
            movements.c.account_id,
            func.coalesce(func.sum(movements.c.delta).filter(movements.c.paid), 0).label("paid"),
            func.sum(movements.c.delta).label("projected"),
        )
        .group_by(movements.c.account_id)
        .subquery()
    )

    rows = db.execute(
        select(
            Account.id,
            Account.initial_balance_cents + func.coalesce(totals.c.paid, literal(0)),
            Account.initial_balance_cents + func.coalesce(totals.c.projected, literal(0)),
        )
        .outerjoin(totals, totals.c.account_id == Account.id)
        .where(Account.household_id == household_id)
    ).all()
    return {row[0]: Balance(int(row[1]), int(row[2])) for row in rows}
