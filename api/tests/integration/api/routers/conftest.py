import pytest
from pytest_factoryboy import register

from tests.factories.entity_factories import CredentialsFactory, UserFactory

factories = [CredentialsFactory, UserFactory]

for factory in factories:
    register(factory)


@pytest.fixture()
def user(user_factory):
    return user_factory()


@pytest.fixture()
def credentials(credentials_factory):
    return credentials_factory()
