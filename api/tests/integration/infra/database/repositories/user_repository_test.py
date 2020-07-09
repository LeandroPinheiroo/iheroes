from operator import attrgetter

import pytest
from asyncpg.exceptions import UniqueViolationError

from iheroes_api.infra.database.repositories import user_repository
from tests.factories.model_factories import insert_user


@pytest.mark.integration
@pytest.mark.asyncio
class TestFetch:
    async def test_has_result(self, database, make_user):
        user = make_user()
        insert_user({**user.dict()})
        getter = attrgetter("email", "password_hash")

        async with database.transaction():
            result = await user_repository.fetch(user.id)
            assert getter(user) == getter(result)

    async def test_has_no_result(self, database, make_user):
        user = make_user()
        async with database.transaction():
            result = await user_repository.fetch(user.id)
            assert not result


@pytest.mark.integration
@pytest.mark.asyncio
class TestFetchByEmail:
    async def test_has_result(self, database, make_user):
        user = make_user()
        insert_user({**user.dict()})
        getter = attrgetter("email", "password_hash")

        async with database.transaction():
            result = await user_repository.fetch_by_email(user.email)
            assert getter(user) == getter(result)

    async def test_has_no_result(self, database, make_user):
        user = make_user()
        async with database.transaction():
            result = await user_repository.fetch_by_email(user.email)
            assert not result


@pytest.mark.integration
@pytest.mark.asyncio
class TestPersist:
    async def test_unique_insertion(self, database, make_user):
        getter = attrgetter("email", "password_hash")
        user = make_user()
        email, password_hash = getter(user)

        async with database.transaction():
            result = await user_repository.persist(email, password_hash)
            assert email, password_hash == getter(result)

    async def test_non_unique_insertion(self, database, make_user):
        user = make_user()
        email, password_hash = attrgetter("email", "password_hash")(user)
        insert_user({**user.dict()})

        async with database.transaction():
            with pytest.raises(UniqueViolationError):
                await user_repository.persist(email, password_hash)
