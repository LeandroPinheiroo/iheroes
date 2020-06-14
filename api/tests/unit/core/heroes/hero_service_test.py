from operator import attrgetter

import pytest

from iheroes_api.core.heroes import hero_service
from iheroes_api.core.heroes.exceptions import HeroNotUniqueError
from iheroes_api.core.protocols import HeroRepo


@pytest.fixture(name="hero_repo")
def hero_repo_fixture(mock_module):
    return mock_module("hero_repo", HeroRepo)


@pytest.mark.unit
@pytest.mark.asyncio
class TestCreate:
    async def test_success(self, hero_repo, user_registry, hero, create_hero_dto):
        hero_repo.persist.return_value = hero
        result = await hero_service.create(hero_repo, create_hero_dto, user_registry)

        assert await hero_repo.persist.called_once_with(
            create_hero_dto, user_registry.id
        )
        assert result is hero

    async def test_conflict(self, hero_repo, user_registry, create_hero_dto):
        user_id = user_registry.id
        error = HeroNotUniqueError(
            user_id, create_hero_dto.name, create_hero_dto.nickname
        )
        hero_repo.persist.side_effect = error

        assert await hero_repo.persist.called_once_with(create_hero_dto, user_id)
        with pytest.raises(HeroNotUniqueError):
            await hero_service.create(hero_repo, create_hero_dto, user_registry)


@pytest.mark.unit
@pytest.mark.asyncio
class TestDelete:
    async def test_found(self, hero_repo, user_registry, hero):
        id_ = hero.id
        hero_repo.delete.return_value = True

        result = await hero_service.delete(hero_repo, user_registry, id_)

        assert await hero_repo.delete.called_once_with(user_registry.id, id_)
        assert result is True

    async def test_not_found(self, hero_repo, user_registry, hero):
        id_ = hero.id
        hero_repo.delete.return_value = False

        result = await hero_service.delete(hero_repo, user_registry, id_)

        assert await hero_repo.delete.called_once_with(user_registry.id, id_)
        assert result is False


@pytest.mark.unit
@pytest.mark.asyncio
class TestGet:
    async def test_found(self, hero_repo, user_registry, hero):
        id_ = hero.id
        hero_repo.fetch.return_value = hero

        result = await hero_service.get(hero_repo, user_registry, id_)

        assert await hero_repo.fetch.called_once_with(user_registry.id, id_)
        assert result is hero

    async def test_not_found(self, hero_repo, user_registry, hero):
        id_ = hero.id
        hero_repo.fetch.return_value = None

        result = await hero_service.get(hero_repo, user_registry, id_)

        assert await hero_repo.fetch.called_once_with(user_registry.id, id_)
        assert result is None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_all(hero_repo, heroes):
    return_val = heroes(5)
    hero_repo.fetch_all.return_value = return_val

    result = await hero_service.get_all(hero_repo)

    assert await hero_repo.fetch_all.called_once()
    assert result
    assert len(result) == 5
    assert result == sorted(result, key=attrgetter("id"))


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_all_by_user(hero_repo, user_registry, heroes):
    return_val = heroes(5)
    hero_repo.fetch_all_by_user.return_value = return_val

    result = await hero_service.get_all_by_user(hero_repo, user_registry)

    assert await hero_repo.fetch_all_by_user.called_once_with(user_registry.id)
    assert result
    assert len(result) == 5
    assert result == sorted(result, key=attrgetter("id"))


@pytest.mark.unit
@pytest.mark.asyncio
class TestUpdate:
    async def test_found(self, hero_repo, user_registry, hero, update_hero_dto):
        id_ = hero.id
        user_id = user_registry.id
        hero_repo.update.return_value = hero

        result = await hero_service.update(
            hero_repo, update_hero_dto, user_registry, id_
        )

        assert await hero_repo.update.called_once_with(
            update_hero_dto, user_id, hero.id
        )
        assert result is hero

    async def test_not_found(self, hero_repo, user_registry, hero, update_hero_dto):
        id_ = hero.id
        user_id = user_registry.id
        hero_repo.update.return_value = None

        result = await hero_service.update(
            hero_repo, update_hero_dto, user_registry, id_
        )

        assert await hero_repo.update.called_once_with(
            update_hero_dto, user_id, hero.id
        )
        assert result is None
