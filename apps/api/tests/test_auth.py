import uuid

from cryptography.hazmat.primitives.asymmetric import ec
from fastapi.testclient import TestClient

from tests.conftest import AuthFactory, make_token


def test_health_is_public(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/health?deep=true").status_code == 200


def test_missing_token_is_401(client: TestClient) -> None:
    res = client.get("/v1/me")
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "unauthorized"


def test_expired_token_is_401(client: TestClient) -> None:
    token = make_token(uuid.uuid4(), expires_in=-10)
    assert client.get("/v1/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_token_signed_by_other_key_is_401(client: TestClient) -> None:
    token = make_token(uuid.uuid4(), key=ec.generate_private_key(ec.SECP256R1()))
    assert client.get("/v1/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_first_access_bootstraps_household(client: TestClient, auth: AuthFactory) -> None:
    user_id = uuid.uuid4()
    headers = auth(user_id, name="Ana Souza")
    me = client.get("/v1/me", headers=headers).json()

    assert me["id"] == str(user_id)
    assert me["full_name"] == "Ana Souza"
    assert me["household"]["name"] == "Minha casa"
    assert me["household"]["role"] == "owner"
    assert [m["display_name"] for m in me["household"]["members"]] == ["Ana"]

    accounts = client.get("/v1/accounts", headers=headers).json()
    assert [(a["name"], a["kind"], a["balance_cents"]) for a in accounts] == [
        ("Carteira", "cash", 0)
    ]
    categories = client.get("/v1/categories", headers=headers).json()
    assert {c["kind"] for c in categories} == {"income", "expense"}

    # Idempotent: a second call does not seed again.
    client.get("/v1/me", headers=headers)
    assert len(client.get("/v1/accounts", headers=headers).json()) == 1
    assert len(client.get("/v1/categories", headers=headers).json()) == len(categories)


def test_update_me_merges_preferences(client: TestClient, auth: AuthFactory) -> None:
    headers = auth()
    client.patch("/v1/me", json={"preferences": {"theme": "dark"}}, headers=headers)
    me = client.patch(
        "/v1/me", json={"preferences": {"privacy": True}, "onboarded": True}, headers=headers
    ).json()
    assert me["preferences"] == {"theme": "dark", "privacy": True}
    assert me["onboarded_at"] is not None


def test_unknown_household_header_is_404(client: TestClient, auth: AuthFactory) -> None:
    headers = auth() | {"X-Household-Id": str(uuid.uuid4())}
    assert client.get("/v1/accounts", headers=headers).status_code == 404
