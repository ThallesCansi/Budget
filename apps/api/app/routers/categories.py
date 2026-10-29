from uuid import UUID

from fastapi import APIRouter, Response, status
from sqlalchemy import exists, select

from app.core.deps import DB, Ctx
from app.models import Category, Transaction
from app.schemas.accounts import CategoryIn, CategoryOut, CategoryUpdate
from app.services.transactions import get_owned

router = APIRouter(prefix="/v1/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
def list_categories(db: DB, ctx: Ctx) -> list[Category]:
    return list(
        db.scalars(
            select(Category)
            .where(Category.household_id == ctx.household_id)
            .order_by(Category.kind, Category.archived, Category.position, Category.name)
        )
    )


@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(db: DB, ctx: Ctx, body: CategoryIn) -> Category:
    category = Category(household_id=ctx.household_id, position=999, **body.model_dump())
    db.add(category)
    db.commit()
    return category


@router.patch("/{category_id}", response_model=CategoryOut)
def update_category(db: DB, ctx: Ctx, category_id: UUID, body: CategoryUpdate) -> Category:
    category: Category = get_owned(db, Category, category_id, ctx.household_id, "Categoria")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(category, key, value)
    db.commit()
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(db: DB, ctx: Ctx, category_id: UUID) -> Response:
    """Deletes an unused category; categories with history are archived instead."""
    category: Category = get_owned(db, Category, category_id, ctx.household_id, "Categoria")
    if db.scalar(select(exists().where(Transaction.category_id == category.id))):
        category.archived = True
    else:
        db.delete(category)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
