import base64
import datetime as dt
from uuid import UUID

from sqlalchemy import Select, and_, or_
from sqlalchemy.orm import Session

from app.core.deps import HouseholdContext
from app.core.errors import AppError, NotFound
from app.models import (
    Account,
    AccountKind,
    Category,
    CategoryKind,
    HouseholdMember,
    Transaction,
    TransactionKind,
)
from app.schemas.transactions import TransactionIn
from app.services.invoices import payment_invoice_month, purchase_invoice_month


def get_owned[T](db: Session, model: type[T], obj_id: UUID, household_id: UUID, what: str) -> T:
    """Loads a row scoped to the household; rows from other households look missing (404)."""
    obj = db.get(model, obj_id)
    if obj is None or getattr(obj, "household_id", None) != household_id:
        raise NotFound(what)
    return obj


def _card_days(account: Account) -> tuple[int, int] | None:
    if account.kind != AccountKind.CREDIT_CARD or not account.closing_day or not account.due_day:
        return None
    return account.closing_day, account.due_day


def _invoice_month(
    data: TransactionIn, account: Account, to_account: Account | None
) -> dt.date | None:
    if data.kind != TransactionKind.TRANSFER and (days := _card_days(account)):
        return data.invoice_month or purchase_invoice_month(data.date, *days)
    if to_account is not None and (days := _card_days(to_account)):
        return data.invoice_month or payment_invoice_month(data.date, *days)
    return None


def validate_references(
    db: Session, ctx: HouseholdContext, data: TransactionIn
) -> tuple[Account, Account | None]:
    hid = ctx.household_id
    account = get_owned(db, Account, data.account_id, hid, "Conta")
    to_account = (
        get_owned(db, Account, data.to_account_id, hid, "Conta de destino")
        if data.to_account_id
        else None
    )
    if data.category_id is not None:
        category = get_owned(db, Category, data.category_id, hid, "Categoria")
        expected = CategoryKind(data.kind.value)
        if category.kind != expected:
            raise AppError(
                "A categoria não corresponde ao tipo do lançamento.", code="category_kind_mismatch"
            )
    if data.member_id is not None:
        get_owned(db, HouseholdMember, data.member_id, hid, "Membro")
    return account, to_account


def upsert_transaction(
    db: Session, ctx: HouseholdContext, tx_id: UUID, data: TransactionIn
) -> tuple[Transaction, bool]:
    """Creates or replaces the transaction with a client-generated id. Returns (tx, created)."""
    account, to_account = validate_references(db, ctx, data)
    values = data.model_dump()
    values["invoice_month"] = _invoice_month(data, account, to_account)

    tx = db.get(Transaction, tx_id)
    created = tx is None
    if tx is None:
        tx = Transaction(id=tx_id, household_id=ctx.household_id, created_by=ctx.user.id)
        db.add(tx)
    elif tx.household_id != ctx.household_id:
        raise NotFound("Lançamento")
    for key, value in values.items():
        setattr(tx, key, value)
    db.commit()
    db.refresh(tx)
    return tx, created


# --- listing ---------------------------------------------------------------------------------


def encode_cursor(tx: Transaction) -> str:
    raw = f"{tx.date.isoformat()}|{tx.created_at.isoformat()}|{tx.id}"
    return base64.urlsafe_b64encode(raw.encode()).decode()


def decode_cursor(cursor: str) -> tuple[dt.date, dt.datetime, UUID]:
    try:
        day, created, tx_id = base64.urlsafe_b64decode(cursor.encode()).decode().split("|")
        return dt.date.fromisoformat(day), dt.datetime.fromisoformat(created), UUID(tx_id)
    except ValueError as exc:
        raise AppError("Cursor inválido.", code="invalid_cursor") from exc


def apply_cursor(query: Select[Transaction], cursor: str) -> Select[Transaction]:
    day, created, tx_id = decode_cursor(cursor)
    return query.where(
        or_(
            Transaction.date < day,
            and_(Transaction.date == day, Transaction.created_at < created),
            and_(
                Transaction.date == day, Transaction.created_at == created, Transaction.id < tx_id
            ),
        )
    )
