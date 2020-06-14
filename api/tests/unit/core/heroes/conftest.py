from functools import partial

import pytest
from pytest_factoryboy import register

from tests.factories.entity_factories import (
    CreateHeroDtoFactory,
    HeroFactory,
    UpdateHeroDtoFactory,
)
from tests.factories.utils import make_many

factories = [
    CreateHeroDtoFactory,
    HeroFactory,
    UpdateHeroDtoFactory,
]

for factory in factories:
    register(factory)


@pytest.fixture()
def create_hero_dto(create_hero_dto_factory):
    return create_hero_dto_factory()


@pytest.fixture()
def hero(hero_factory):
    return hero_factory()


@pytest.fixture()
def heroes(hero_factory):
    return partial(make_many, hero_factory)


@pytest.fixture()
def update_hero_dto(update_hero_dto_factory):
    return update_hero_dto_factory()
