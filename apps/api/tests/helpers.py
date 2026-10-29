import uuid
from typing import Any

from fastapi.testclient import TestClient


def setup_household(client: TestClient, headers: dict[str, str]) -> dict[str, Any]:
    """Bootstraps the user and returns ids for the default account and some categories."""
    me = client.get("/v1/me", headers=headers).json()
    accounts = client.get("/v1/accounts", headers=headers).json()
    categories = client.get("/v1/categories", headers=headers).json()
    by_name = {c["name"]: c["id"] for c in categories}
    return {"me": me, "wallet": accounts[0]["id"], "categories": by_name}


def put_tx(client: TestClient, headers: dict[str, str], **body: Any) -> Any:
    tx_id = body.pop("id", None) or str(uuid.uuid4())
    body.setdefault("description", "Lançamento")
    body.setdefault("date", "2026-10-10")
    return client.put(f"/v1/transactions/{tx_id}", json=body, headers=headers)
