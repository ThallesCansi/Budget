import uuid

from fastapi.testclient import TestClient

from tests.conftest import AuthFactory
from tests.helpers import put_tx, setup_household


def _bank(client: TestClient, headers: dict[str, str], **extra: object) -> str:
    body = {"name": "Banco", "kind": "checking", "initial_balance_cents": 100_000} | extra
    res = client.post("/v1/accounts", json=body, headers=headers)
    assert res.status_code == 201, res.text
    return res.json()["id"]


def test_balances_with_transfers_and_pending(client: TestClient, auth: AuthFactory) -> None:
    headers = auth()
    h = setup_household(client, headers)
    bank = _bank(client, headers)
    cats = h["categories"]

    assert (
        put_tx(
            client,
            headers,
            kind="income",
            account_id=bank,
            amount_cents=500_000,
            category_id=cats["Salário"],
        ).status_code
        == 201
    )
    put_tx(
        client,
        headers,
        kind="expense",
        account_id=bank,
        amount_cents=12_345,
        category_id=cats["Mercado"],
    )
    put_tx(
        client,
        headers,
        kind="transfer",
        account_id=bank,
        to_account_id=h["wallet"],
        amount_cents=20_000,
    )
    put_tx(client, headers, kind="expense", account_id=bank, amount_cents=99_999, paid=False)

    balances = {a["name"]: a for a in client.get("/v1/accounts", headers=headers).json()}
    assert balances["Banco"]["balance_cents"] == 100_000 + 500_000 - 12_345 - 20_000
    assert balances["Banco"]["projected_balance_cents"] == 567_655 - 99_999
    assert balances["Carteira"]["balance_cents"] == 20_000

    summary = client.get("/v1/reports/summary?month=2026-10-01", headers=headers).json()
    assert summary["income_cents"] == 500_000
    assert summary["expense_cents"] == 12_345
    assert summary["pending_expense_cents"] == 99_999
    assert summary["balance_cents"] == 100_000 + 500_000 - 12_345


def test_put_is_idempotent_and_replaces(client: TestClient, auth: AuthFactory) -> None:
    headers = auth()
    h = setup_household(client, headers)
    tx_id = str(uuid.uuid4())
    body = {"id": tx_id, "kind": "expense", "account_id": h["wallet"], "amount_cents": 1000}

    assert put_tx(client, headers, **dict(body)).status_code == 201
    assert put_tx(client, headers, **dict(body)).status_code == 200
    res = put_tx(client, headers, **(body | {"amount_cents": 2500, "description": "Padaria"}))
    assert res.json()["amount_cents"] == 2500
    assert res.json()["description"] == "Padaria"

    items = client.get("/v1/transactions", headers=headers).json()["items"]
    assert len(items) == 1

    assert client.delete(f"/v1/transactions/{tx_id}", headers=headers).status_code == 204
    assert client.delete(f"/v1/transactions/{tx_id}", headers=headers).status_code == 204


def test_validation_rules(client: TestClient, auth: AuthFactory) -> None:
    headers = auth()
    h = setup_household(client, headers)
    wallet, cats = h["wallet"], h["categories"]

    res = put_tx(client, headers, kind="transfer", account_id=wallet, amount_cents=10)
    assert res.status_code == 422
    res = put_tx(client, headers, kind="expense", account_id=wallet, amount_cents=0)
    assert res.status_code == 422
    res = put_tx(
        client, headers, kind="expense", account_id=wallet, amount_cents=10, description="   "
    )
    assert res.status_code == 422
    res = put_tx(
        client,
        headers,
        kind="expense",
        account_id=wallet,
        amount_cents=10,
        category_id=cats["Salário"],
    )
    assert res.json()["error"]["code"] == "category_kind_mismatch"


def test_households_are_isolated(client: TestClient, auth: AuthFactory) -> None:
    alice, bob = auth(), auth()
    a = setup_household(client, alice)
    setup_household(client, bob)
    tx_id = str(uuid.uuid4())
    put_tx(client, alice, id=tx_id, kind="expense", account_id=a["wallet"], amount_cents=10)

    assert client.get(f"/v1/transactions/{tx_id}", headers=bob).status_code == 404
    assert client.delete(f"/v1/transactions/{tx_id}", headers=bob).status_code == 404
    # Bob cannot overwrite Alice's transaction by reusing its id...
    bob_wallet = client.get("/v1/accounts", headers=bob).json()[0]["id"]
    res = put_tx(client, bob, id=tx_id, kind="expense", account_id=bob_wallet, amount_cents=1)
    assert res.status_code == 404
    # ...nor point at Alice's account.
    res = put_tx(client, bob, kind="expense", account_id=a["wallet"], amount_cents=1)
    assert res.status_code == 404
    assert (
        client.patch(f"/v1/accounts/{a['wallet']}", json={"name": "x"}, headers=bob).status_code
        == 404
    )
    assert client.get("/v1/transactions", headers=bob).json()["items"] == []


def test_credit_card_assigns_invoice(client: TestClient, auth: AuthFactory) -> None:
    headers = auth()
    setup_household(client, headers)
    card = _bank(
        client,
        headers,
        name="Cartão",
        kind="credit_card",
        initial_balance_cents=0,
        credit_limit_cents=500_000,
        closing_day=25,
        due_day=5,
    )
    bank = _bank(client, headers)

    before = put_tx(
        client, headers, kind="expense", account_id=card, amount_cents=100, date="2026-10-24"
    ).json()
    after = put_tx(
        client, headers, kind="expense", account_id=card, amount_cents=100, date="2026-10-25"
    ).json()
    payment = put_tx(
        client,
        headers,
        kind="transfer",
        account_id=bank,
        to_account_id=card,
        amount_cents=100,
        date="2026-11-05",
    ).json()
    assert before["invoice_month"] == "2026-11-01"
    assert after["invoice_month"] == "2026-12-01"
    assert payment["invoice_month"] == "2026-11-01"


def test_card_requires_days(client: TestClient, auth: AuthFactory) -> None:
    headers = auth()
    setup_household(client, headers)
    res = client.post("/v1/accounts", json={"name": "C", "kind": "credit_card"}, headers=headers)
    assert res.status_code == 422


def test_pagination_and_filters(client: TestClient, auth: AuthFactory) -> None:
    headers = auth()
    h = setup_household(client, headers)
    for day in range(1, 8):
        put_tx(
            client,
            headers,
            kind="expense",
            account_id=h["wallet"],
            amount_cents=day,
            date=f"2026-10-0{day}",
            description=f"Item {day}",
        )

    seen: list[str] = []
    cursor = None
    while True:
        url = "/v1/transactions?limit=3" + (f"&cursor={cursor}" if cursor else "")
        page = client.get(url, headers=headers).json()
        seen += [t["description"] for t in page["items"]]
        if not (cursor := page["next_cursor"]):
            break
    assert seen == [f"Item {d}" for d in range(7, 0, -1)]

    res = client.get("/v1/transactions?from=2026-10-03&to=2026-10-04&q=item", headers=headers)
    assert [t["description"] for t in res.json()["items"]] == ["Item 4", "Item 3"]


def test_delete_used_account_archives(client: TestClient, auth: AuthFactory) -> None:
    headers = auth()
    h = setup_household(client, headers)
    put_tx(client, headers, kind="expense", account_id=h["wallet"], amount_cents=10)
    assert client.delete(f"/v1/accounts/{h['wallet']}", headers=headers).status_code == 204
    accounts = client.get("/v1/accounts", headers=headers).json()
    assert accounts[0]["archived"] is True
