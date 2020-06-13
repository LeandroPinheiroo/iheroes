import pytest

from iheroes_api.core.accounts import hash_service, user_service
from iheroes_api.core.accounts.user import Credentials, User
from iheroes_api.core.protocols import UserRepo


@pytest.fixture()
def user_repo(mock_module):
    return mock_module("user_repo", UserRepo)


@pytest.mark.unit
class TestGetByCredentials:
    @pytest.mark.asyncio
    async def test_user_found(self, user_repo, credentials: Credentials, user: User):
        email = credentials.email
        password_hash = hash_service.hash_(credentials.password)
        user_repo.fetch_by_email.return_value = User(
            **{**user.dict(), "email": email, "password_hash": password_hash}
        )

        result = await user_service.get_by_crendentials(user_repo, credentials)

        user_repo.fetch_by_email.assert_called_with(email)
        assert result
        assert result.email == email
