import os

import boto3
import httpx
import pytest

APP_BASE_URL = "http://localhost:8000"
REQUIRED_ENV_VARS = [
    "KEYCLOAK_URL",
    "KEYCLOAK_REALM",
    "KEYCLOAK_CLIENT_ID",
    "KEYCLOAK_CLIENT_SECRET",
    "AWS_ENDPOINT_URL_DYNAMODB",
]


@pytest.fixture(scope="session")
def required_env():
    missing = [v for v in REQUIRED_ENV_VARS if not os.getenv(v)]
    if missing:
        pytest.skip(f"Missing required env vars: {', '.join(missing)}")


@pytest.fixture(scope="session")
def app_url(required_env):
    try:
        httpx.get(f"{APP_BASE_URL}/docs", timeout=3).raise_for_status()
    except Exception:
        pytest.skip(f"App not reachable at {APP_BASE_URL} — start it with: fastapi dev app/main.py")
    return APP_BASE_URL


def _fetch_token(client_id: str, client_secret: str) -> str:
    url = f"{os.environ['KEYCLOAK_URL']}/realms/{os.environ['KEYCLOAK_REALM']}/protocol/openid-connect/token"
    r = httpx.post(
        url,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["access_token"]


@pytest.fixture(scope="session")
def token_a(app_url):
    return _fetch_token(os.environ["KEYCLOAK_CLIENT_ID"], os.environ["KEYCLOAK_CLIENT_SECRET"])


@pytest.fixture(scope="session")
def token_b(app_url):
    cid = os.getenv("KEYCLOAK_CLIENT_ID_B")
    secret = os.getenv("KEYCLOAK_CLIENT_SECRET_B")
    if not cid or not secret:
        pytest.skip("KEYCLOAK_CLIENT_ID_B/KEYCLOAK_CLIENT_SECRET_B not set — re-run bin/bootstrap")
    return _fetch_token(cid, secret)


@pytest.fixture(scope="session")
def dynamo_table(app_url):
    db = boto3.resource(
        "dynamodb",
        region_name="us-east-1",
        endpoint_url=os.environ["AWS_ENDPOINT_URL_DYNAMODB"],
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    return db.Table("todos")


@pytest.fixture
def http_a(app_url, token_a):
    with httpx.Client(base_url=app_url, headers={"Authorization": f"Bearer {token_a}"}) as c:
        yield c


@pytest.fixture
def http_b(app_url, token_b):
    with httpx.Client(base_url=app_url, headers={"Authorization": f"Bearer {token_b}"}) as c:
        yield c


@pytest.fixture
def cleanup_ids(dynamo_table):
    """Collect todo IDs created during a test; delete them from DynamoDB after."""
    ids = []
    yield ids
    for todo_id in ids:
        dynamo_table.delete_item(Key={"id": todo_id})
