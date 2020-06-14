from operator import attrgetter
from typing import List, Optional

from iheroes_api.core.accounts.user import UserRegistry
from iheroes_api.core.heroes.hero import CreateHeroDto, Hero, UpdateHeroDto
from iheroes_api.core.protocols import HeroRepo


async def create(repo: HeroRepo, dto: CreateHeroDto, user: UserRegistry) -> Hero:
    return await repo.persist(dto, user.id)


async def delete(repo: HeroRepo, user: UserRegistry, id_: int) -> bool:
    return await repo.delete(user.id, id_)


async def get(repo: HeroRepo, user: UserRegistry, id_: int) -> Optional[Hero]:
    return await repo.fetch(user.id, id_)


async def get_all(repo: HeroRepo) -> List[Hero]:
    return sorted(await repo.fetch_all(), key=attrgetter("id"))


async def get_all_by_user(repo: HeroRepo, user: UserRegistry) -> List[Hero]:
    return sorted(await repo.fetch_all_by_user(user.id), key=attrgetter("id"))


async def update(repo: HeroRepo, dto: UpdateHeroDto, user: UserRegistry, id_: int):
    return await repo.update(dto, user.id, id_)
