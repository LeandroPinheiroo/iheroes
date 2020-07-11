from operator import attrgetter

import pytest
from pytest_factoryboy import register
from toolz import pipe
from toolz.curried import do

from iheroes_api.core.heroes.exceptions import HeroNotUniqueError
from iheroes_api.infra.database.repositories import hero_repository
from tests.factories.entity_factories import CreateHeroDtoFactory, UpdateHeroDtoFactory
from tests.factories.model_factories import insert_hero, insert_user

factories = [CreateHeroDtoFactory, UpdateHeroDtoFactory]

for factory in factories:
    register(factory)


@pytest.fixture(name="make_create_hero_dto")
def make_create_hero_dto_fixture(create_hero_dto_factory):
    return lambda **override: create_hero_dto_factory(**override)


@pytest.fixture(name="make_update_hero_dto")
def make_update_hero_dto_fixture(update_hero_dto_factory):
    return lambda **override: update_hero_dto_factory(**override)


@pytest.mark.integration
@pytest.mark.asyncio
class TestDelete:
    async def test_found(self, database, make_user, make_hero):
        user = make_user()
        insert_user(user.dict())

        id_ = 1
        user_id = user.id
        insert_hero(make_hero(id=id_, user_id=user_id).dict())

        async with database.transaction():
            assert await hero_repository.delete(user_id, id_)

    async def test_not_found(self, database):
        async with database.transaction():
            assert not await hero_repository.delete(1, 1)


@pytest.mark.integration
@pytest.mark.asyncio
class TestExists:
    async def test_found(self, database, make_user, make_hero):
        user = make_user()
        insert_user(user.dict())

        id_ = 1
        insert_hero(make_hero(id=id_, user_id=user.id).dict())

        async with database.transaction():
            assert await hero_repository.exists(id_)

    async def test_not_found(self, database):
        async with database.transaction():
            assert not await hero_repository.exists(1)


@pytest.mark.integration
@pytest.mark.asyncio
class TestFetch:
    async def test_found(self, database, make_user, make_hero):
        user = make_user()
        insert_user(user.dict())

        id_ = 1
        user_id = user.id
        hero = make_hero(id=id_, user_id=user_id)
        insert_hero(hero.dict())

        async with database.transaction():
            result = await hero_repository.fetch(user_id, id_)

        assert result == hero

    async def test_not_found(self, database):
        async with database.transaction():
            assert not await hero_repository.fetch(1, 1)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fetch_all(database, make_user, make_heroes):
    user = make_user()
    insert_user(user.dict())

    heroes = make_heroes(10, user_id=user.id)
    for hero in heroes:
        insert_hero(hero.dict())

    async with database.transaction():
        result = list(await hero_repository.fetch_all())

    assert len(result) == len(heroes)
    for hero in result:
        assert hero in heroes


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fetch_all_by_user(database, make_user, make_heroes):
    users = make_user(), make_user()
    for user in users:
        insert_user(user.dict())

    users_heroes = pipe(
        users,
        lambda users: {user.id: make_heroes(10, user_id=user.id) for user in users},
        do(
            lambda mapping: [
                insert_hero(hero.dict())
                for user, heroes in mapping.items()
                for hero in heroes
            ]
        ),
    )

    async with database.transaction():
        for user in users:
            user_id = user.id
            heroes = users_heroes[user_id]

            result = list(await hero_repository.fetch_all_by_user(user_id))
            assert len(result) == len(heroes)
            for hero in result:
                assert hero in heroes


@pytest.mark.integration
@pytest.mark.asyncio
class TestPersist:
    async def test_success(self, database, make_user, make_create_hero_dto):
        user = make_user()
        insert_user(user.dict())

        dto = make_create_hero_dto()

        async with database.transaction():
            result = await hero_repository.persist(user.id, dto)

        assert attrgetter("user_id", "name", "nickname", "power_class", "location")(
            result
        ) == (user.id, *attrgetter("name", "nickname", "power_class", "location")(dto))

    async def test_hero_not_unique_error(
        self, database, make_user, make_hero, make_create_hero_dto
    ):
        user = make_user()
        insert_user(user.dict())

        id_ = 1
        user_id = user.id
        hero = make_hero(id=id_, user_id=user_id)
        insert_hero(hero.dict())

        dto = make_create_hero_dto()

        async with database.transaction():
            with pytest.raises(HeroNotUniqueError):
                await hero_repository.persist(user_id, dto)


@pytest.mark.integration
@pytest.mark.asyncio
class TestUpdate:
    async def test_found(self, database, make_user, make_hero, make_update_hero_dto):
        user = make_user()
        insert_user(user.dict())

        id_ = 1
        user_id = user.id
        hero = make_hero(id=id_, user_id=user_id)
        insert_hero(hero.dict())

        dto = make_update_hero_dto()

        async with database.transaction():
            result = await hero_repository.update(user_id, dto, id_)

        assert result
        assert (result.id, result.user_id) == (hero.id, hero.user_id)

        getter = attrgetter("name", "nickname", "power_class", "location")
        assert getter(result) != getter(hero)

    async def test_not_found(self, database, make_update_hero_dto):
        id_ = 1
        user_id = 1
        dto = make_update_hero_dto

        async with database.transaction():
            assert not await hero_repository.update(user_id, dto, id_)

    async def test_hero_not_unique_error(
        self, database, make_user, make_hero, make_update_hero_dto
    ):
        user = make_user()
        insert_user(user.dict())

        id_ = 1
        user_id = user.id
        hero = make_hero(id=id_, user_id=user_id)
        other_hero = make_hero(user_id=user_id)
        insert_hero([hero.dict(), other_hero.dict()])

        dto = make_update_hero_dto(name=other_hero.name, nickname=other_hero.nickname)

        async with database.transaction():
            with pytest.raises(HeroNotUniqueError):
                await hero_repository.update(user_id, dto, id_)
