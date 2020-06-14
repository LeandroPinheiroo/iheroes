from typing import Iterable, Optional, Protocol

from iheroes_api.core.accounts.user import User
from iheroes_api.core.heroes.hero import CreateHeroDto, Hero, UpdateHeroDto


class HeroRepo(Protocol):
    async def delete(self, user_id: int, id_: int) -> bool:
        ...

    async def fetch(self, user_id: int, id_: int) -> Optional[Hero]:
        ...

    async def fetch_all(self) -> Iterable[Hero]:
        ...

    async def fetch_all_by_user(self, user_id: int) -> Iterable[Hero]:
        ...

    async def persist(self, dto: CreateHeroDto, user_id: int) -> Hero:
        ...

    async def update(
        self, dto: UpdateHeroDto, user_id: int, id_: int
    ) -> Optional[Hero]:
        ...


class UserRepo(Protocol):
    async def fetch(self, id_: int) -> Optional[User]:
        ...

    async def fetch_by_email(self, email: str) -> Optional[User]:
        ...

    async def persist(self, email: str, password_hash: str) -> User:
        ...
