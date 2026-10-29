import datetime as dt
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, Response, status
from sqlalchemy import or_, select

from app.core.deps import DB, Ctx
from app.models import Transaction, TransactionKind
from app.schemas.transactions import TransactionIn, TransactionOut, TransactionPage
from app.services.transactions import apply_cursor, encode_cursor, get_owned, upsert_transaction

router = APIRouter(prefix="/v1/transactions", tags=["transactions"])


@router.get("", response_model=TransactionPage)
def list_transactions(
    db: DB,
    ctx: Ctx,
    date_from: Annotated[dt.date | None, Query(alias="from")] = None,
    date_to: Annotated[dt.date | None, Query(alias="to")] = None,
    account_id: UUID | None = None,
    category_id: UUID | None = None,
    member_id: UUID | None = None,
    kind: TransactionKind | None = None,
    paid: bool | None = None,
    q: Annotated[str | None, Query(max_length=80)] = None,
    cursor: str | None = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
) -> TransactionPage:
    query = select(Transaction).where(Transaction.household_id == ctx.household_id)
    if date_from:
        query = query.where(Transaction.date >= date_from)
    if date_to:
        query = query.where(Transaction.date <= date_to)
    if account_id:
        query = query.where(
            or_(Transaction.account_id == account_id, Transaction.to_account_id == account_id)
        )
    if category_id:
        query = query.where(Transaction.category_id == category_id)
    if member_id:
        query = query.where(Transaction.member_id == member_id)
    if kind:
        query = query.where(Transaction.kind == kind)
    if paid is not None:
        query = query.where(Transaction.paid == paid)
    if q:
        query = query.where(Transaction.description.ilike(f"%{q.strip()}%"))
    if cursor:
        query = apply_cursor(query, cursor)

    rows = list(
        db.scalars(
            query.order_by(
                Transaction.date.desc(), Transaction.created_at.desc(), Transaction.id.desc()
            ).limit(limit + 1)
        )
    )
    has_more = len(rows) > limit
    rows = rows[:limit]
    return TransactionPage(
        items=[TransactionOut.model_validate(t) for t in rows],
        next_cursor=encode_cursor(rows[-1]) if has_more else None,
    )


@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(db: DB, ctx: Ctx, transaction_id: UUID) -> Transaction:
    return get_owned(db, Transaction, transaction_id, ctx.household_id, "Lançamento")


@router.put(
    "/{transaction_id}",
    response_model=TransactionOut,
    responses={201: {"model": TransactionOut, "description": "Criado"}},
)
def put_transaction(
    db: DB, ctx: Ctx, transaction_id: UUID, body: TransactionIn, response: Response
) -> Transaction:
    """Idempotent create-or-replace. The client generates the id (UUID v4)."""
    tx, created = upsert_transaction(db, ctx, transaction_id, body)
    if created:
        response.status_code = status.HTTP_201_CREATED
    return tx


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(db: DB, ctx: Ctx, transaction_id: UUID) -> Response:
    """Idempotent: deleting a missing transaction also returns 204."""
    tx = db.get(Transaction, transaction_id)
    if tx is not None:
        get_owned(db, Transaction, transaction_id, ctx.household_id, "Lançamento")
        db.delete(tx)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
