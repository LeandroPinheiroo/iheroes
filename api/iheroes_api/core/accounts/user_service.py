from typing import Optional

from iheroes_api.core.accounts import hash_service
from iheroes_api.core.accounts.exceptions import EmailNotUniqueError, UserNotFoundError
from iheroes_api.core.accounts.user import Credentials, UserRegistry
from iheroes_api.core.protocols import UserRepo


async def get_by_credentials(
    repo: UserRepo, credentials: Credentials
) -> Optional[UserRegistry]:
    user = await repo.fetch_by_email(credentials.email.lower())
    if not user:
        hash_service.dummy_verify()
        return None

    password, hash_ = credentials.password, user.password_hash

    if not hash_service.verify(password, hash_):
        return None

    return UserRegistry(**user.dict())


async def get_by_id(repo: UserRepo, id_: int) -> Optional[UserRegistry]:
    user = await repo.fetch(id_)
    return UserRegistry(**user.dict()) if user else None


async def get_by_id_or_raise(repo: UserRepo, id_: int) -> UserRegistry:
    user = await get_by_id(repo, id_)
    if not user:
        raise UserNotFoundError(id_)
    return user


async def register(repo: UserRepo, credentials: Credentials) -> UserRegistry:
    email = credentials.email.lower()

    user = await repo.fetch_by_email(email)
    if user:
        raise EmailNotUniqueError(email)

    password_hash = hash_service.hash_(credentials.password)

    user = await repo.persist(email, password_hash)
    return UserRegistry(**user.dict())
