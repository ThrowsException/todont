import os
from functools import lru_cache

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.openapi.models import OAuthFlowClientCredentials, OAuthFlows
from fastapi.security import OAuth2
from jwt import PyJWKClient

_keycloak_url = os.getenv("KEYCLOAK_URL", "")
_keycloak_realm = os.getenv("KEYCLOAK_REALM", "")

_oauth2_scheme = OAuth2(
    flows=OAuthFlows(
        clientCredentials=OAuthFlowClientCredentials(
            tokenUrl=f"{_keycloak_url}/realms/{_keycloak_realm}/protocol/openid-connect/token",
        )
    )
)


@lru_cache
def _jwks_client() -> PyJWKClient:
    keycloak_url = os.environ["KEYCLOAK_URL"]
    keycloak_realm = os.environ["KEYCLOAK_REALM"]
    jwks_url = f"{keycloak_url}/realms/{keycloak_realm}/protocol/openid-connect/certs"
    return PyJWKClient(jwks_url, cache_keys=True, cache_jwk_set=True, lifespan=300)


async def verify_token(token: str = Depends(_oauth2_scheme)) -> dict:
    keycloak_url = os.environ["KEYCLOAK_URL"]
    keycloak_realm = os.environ["KEYCLOAK_REALM"]
    keycloak_client_id = os.environ["KEYCLOAK_CLIENT_ID"]
    issuer = f"{keycloak_url}/realms/{keycloak_realm}"

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    scheme, _, token = token.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        signing_key = _jwks_client().get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=keycloak_client_id,
            issuer=issuer,
        )
    except jwt.exceptions.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    return payload
