import httpx
import pytest


@pytest.mark.integration
def test_no_token_returns_401(app_url):
    r = httpx.get(f"{app_url}/todos")
    assert r.status_code == 401


@pytest.mark.integration
def test_malformed_token_returns_401(app_url):
    r = httpx.get(f"{app_url}/todos", headers={"Authorization": "Bearer not-a-real-jwt"})
    assert r.status_code == 401
