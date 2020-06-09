from typing import Optional, Protocol

from iheroes_api.core.accounts.user import User


class UserRepo(Protocol):
    async def fetch(self, id_) -> Optional[User]:
        ...

    async def fetch_by_email(self, email: str) -> Optional[User]:
        ...

    async def persist(self, email: str, password_hash: str) -> User:
        ...
