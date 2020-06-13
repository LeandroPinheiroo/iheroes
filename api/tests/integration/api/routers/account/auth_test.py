import jwt
import pytest

from iheroes_api.core.accounts import hash_service
from tests.factories.model_factories import insert_user
from tests.utils.auth import (
    auth_headers,
    build_form_data,
    oauth2_instrospect_url,
    oauth2_token_url,
    secret_key,
)


@pytest.mark.integration
class TestOAuth2Token:
    def test_success(self, test_client, credentials):
        insert_user(
            {
                "email": credentials.email,
                "password_hash": hash_service.hash_(credentials.password),
            }
        )
        with test_client as client:
            response = client.post(oauth2_token_url, data=build_form_data(credentials))
            body = response.json()
            assert body["access_token"]
            assert body["expire"]
            assert body["token_type"] == "bearer"
            assert response.status_code == 200

    def test_unauthorized(self, test_client, credentials):
        with test_client as client:
            response = client.post(oauth2_token_url, data=build_form_data(credentials))
            assert response.json().get("detail") == "invalid authentication credentials"
            assert response.status_code == 401


@pytest.mark.integration
class TestOAuth2Introspect:
    def test_success(self, test_client, logged_user):
        user, access_token = logged_user
        with test_client as client:
            response = client.get(
                oauth2_instrospect_url, headers=auth_headers(logged_user.access_token),
            )
            body = response.json()
            assert body == {
                "id": user.id,
                "email": user.email,
            }
            assert response.status_code == 200

    def test_unauthorized(self, test_client):
        with test_client as client:
            token = str(jwt.encode({"sub": "userid:1"}, secret_key))
            response = client.get(oauth2_instrospect_url, headers=auth_headers(token),)

            assert response.json().get("detail") == "invalid token"
            assert response.status_code == 401
