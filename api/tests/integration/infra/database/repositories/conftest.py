from functools import partial

import pytest
from pytest_factoryboy import register

from iheroes_api.infra.database.sqlalchemy import (
    connect_database,
    database,
    disconnect_database,
)
from tests.factories.entity_factories import (
    HeroFactory,
    UserFactory,
)
from tests.factories.utils import make_many
from tests.utils.database import clear_database

factories = [HeroFactory, UserFactory]

for factory in factories:
    register(factory)


@pytest.fixture(name="database")
async def database_fixture():
    with clear_database():
        await connect_database()
        yield database
        await disconnect_database()


# Entity Fixtures
@pytest.fixture()
def make_hero(hero_factory):
    return lambda **override: hero_factory(**override)


@pytest.fixture()
def make_heroes(hero_factory):
    return partial(make_many, hero_factory)


@pytest.fixture()
def make_user(user_factory):
    return lambda **override: user_factory(**override)
