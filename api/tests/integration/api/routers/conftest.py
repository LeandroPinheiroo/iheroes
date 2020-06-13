from collections import namedtuple

import pytest
from pytest_factoryboy import register

from iheroes_api.core.accounts import hash_service
from iheroes_api.core.accounts.user import User
from tests.factories.entity_factories import CredentialsFactory, UserFactory
from tests.factories.model_factories import insert_user
from tests.utils.auth import build_form_data, oauth2_token_url

LoggedUser = namedtuple("LoggedUser", ["user", "access_token"])

factories = [CredentialsFactory, UserFactory]

for factory in factories:
    register(factory)


@pytest.fixture()
def user(user_factory):
    return user_factory()


@pytest.fixture()
def credentials(credentials_factory):
    return credentials_factory()


@pytest.fixture()
def logged_user(test_client, credentials):
    id_ = 1
    email = credentials.email
    password_hash = hash_service.hash_(credentials.password)

    insert_user({"id": id_, "email": credentials.email, "password_hash": password_hash})
    with test_client as client:
        response = client.post(oauth2_token_url, data=build_form_data(credentials))
        body = response.json()
        return LoggedUser(
            User(id=id_, email=email, password_hash=password_hash),
            body["access_token"],
        )
