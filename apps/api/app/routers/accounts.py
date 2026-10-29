from uuid import UUID

from fastapi import APIRouter, Response, status
from sqlalchemy import exists, or_, select

from app.core.deps import DB, Ctx
from app.models import Account, AccountKind, Transaction
from app.schemas.accounts import AccountIn, AccountOut, AccountUpdate
from app.services.balances import account_balances
from app.services.transactions import get_owned

router = APIRouter(prefix="/v1/accounts", tags=["accounts"])


def _with_balance(account: Account, balances: dict) -> AccountOut:  # type: ignore[type-arg]
    out = AccountOut.model_validate(account)
    if balance := balances.get(account.id):
        out.balance_cents = balance.balance_cents
        out.projected_balance_cents = balance.projected_cents
    return out


@router.get("", response_model=list[AccountOut])
def list_accounts(db: DB, ctx: Ctx) -> list[AccountOut]:
    accounts = db.scalars(
        select(Account)
        .where(Account.household_id == ctx.household_id)
        .order_by(Account.archived, Account.position, Account.created_at)
    ).all()
    balances = account_balances(db, ctx.household_id)
    return [_with_balance(a, balances) for a in accounts]


@router.post("", response_model=AccountOut, status_code=status.HTTP_201_CREATED)
def create_account(db: DB, ctx: Ctx, body: AccountIn) -> AccountOut:
    account = Account(household_id=ctx.household_id, **body.model_dump())
    db.add(account)
    db.commit()
    return _with_balance(account, account_balances(db, ctx.household_id))


@router.patch("/{account_id}", response_model=AccountOut)
def update_account(db: DB, ctx: Ctx, account_id: UUID, body: AccountUpdate) -> AccountOut:
    account: Account = get_owned(db, Account, account_id, ctx.household_id, "Conta")
    changes = body.model_dump(exclude_unset=True)
    if account.kind != AccountKind.CREDIT_CARD:
        for key in ("credit_limit_cents", "closing_day", "due_day"):
            changes.pop(key, None)
    for key, value in changes.items():
        setattr(account, key, value)
    db.commit()
    return _with_balance(account, account_balances(db, ctx.household_id))


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(db: DB, ctx: Ctx, account_id: UUID) -> Response:
    """Deletes an unused account; accounts with history are archived instead."""
    account: Account = get_owned(db, Account, account_id, ctx.household_id, "Conta")
    used = db.scalar(
        select(
            exists().where(
                or_(Transaction.account_id == account.id, Transaction.to_account_id == account.id)
            )
        )
    )
    if used:
        account.archived = True
    else:
        db.delete(account)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
