import pytest
from pytest_factoryboy import register

from tests.factories.entity_factories import UserRegistryFactory

factories = [UserRegistryFactory]

for factory in factories:
    register(factory)


@pytest.fixture()
def user_registry(user_registry_factory):
    return user_registry_factory()
