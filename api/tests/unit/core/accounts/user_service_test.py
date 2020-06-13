import pytest

from iheroes_api.core.accounts import hash_service, user_service
from iheroes_api.core.accounts.exceptions import UserNotFoundError
from iheroes_api.core.accounts.user import User
from iheroes_api.core.protocols import UserRepo


@pytest.fixture()
def user_repo(mock_module):
    return mock_module("user_repo", UserRepo)


@pytest.mark.unit
@pytest.mark.asyncio
class TestGetByCredentials:
    async def test_valid_credentials(self, user_repo, credentials, user):
        # Setup
        email = credentials.email
        password_hash = hash_service.hash_(credentials.password)

        user_repo.fetch_by_email.return_value = User(
            **{**user.dict(), "email": email, "password_hash": password_hash}
        )

        # Test
        result = await user_service.get_by_credentials(user_repo, credentials)

        # Assertions
        user_repo.fetch_by_email.assert_called_once_with(email)
        assert result
        assert result.email == email

    async def test_user_not_found(self, user_repo, credentials):
        # Setup
        user_repo.fetch_by_email.return_value = None

        # Test
        result = await user_service.get_by_credentials(user_repo, credentials)

        # Assertions
        user_repo.fetch_by_email.assert_called_once_with(credentials.email)
        assert not result

    async def test_invalid_credentials(self, user_repo, credentials, user):
        # Setup
        email = credentials.email
        password_hash = hash_service.hash_("other password")

        user_repo.fetch_by_email.return_value = User(
            **{**user.dict(), "email": email, "password_hash": password_hash}
        )

        # Test
        result = await user_service.get_by_credentials(user_repo, credentials)

        # Assertions
        user_repo.fetch_by_email.assert_called_once_with(email)
        assert not result


@pytest.mark.unit
@pytest.mark.asyncio
class TestGetById:
    async def test_valid_id(self, user_repo, user):
        # Setup
        id_ = 1
        user_repo.fetch.return_value = User(**{**user.dict(), "id": id_})

        # Test
        result = await user_service.get_by_id(user_repo, id_)

        # Assertions
        user_repo.fetch.assert_called_once_with(id_)
        assert result
        assert result.id == id_

    async def test_invalid_id(self, user_repo):
        # Setup
        id_ = 1
        user_repo.fetch.return_value = None

        # Test
        result = await user_service.get_by_id(user_repo, id_)

        # Assertions
        user_repo.fetch.assert_called_once_with(id_)
        assert not result


@pytest.mark.unit
@pytest.mark.asyncio
class TestGetByIdOrRaise:
    async def test_valid_id(self, user_repo, user):
        # Setup
        id_ = 1
        user_repo.fetch.return_value = User(**{**user.dict(), "id": id_})

        # Test
        result = await user_service.get_by_id_or_raise(user_repo, id_)

        # Assertions
        user_repo.fetch.assert_called_once_with(id_)
        assert result
        assert result.id == id_

    async def test_invalid_id(self, user_repo):
        # Setup
        id_ = 1
        user_repo.fetch.return_value = None

        # Test
        with pytest.raises(UserNotFoundError) as excinfo:
            await user_service.get_by_id_or_raise(user_repo, id_)

        # Assertions
        user_repo.fetch.assert_called_once_with(id_)
        error = excinfo.value
        assert error.msg == "user not found"
        assert error.user_id == id_
