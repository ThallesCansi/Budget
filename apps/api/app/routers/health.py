from fastapi import APIRouter
from sqlalchemy import text

from app.core.deps import DB

router = APIRouter(tags=["health"])


@router.get("/health")
def health(db: DB, deep: bool = False) -> dict[str, str]:
    if deep:
        db.execute(text("SELECT 1"))
    return {"status": "ok"}
