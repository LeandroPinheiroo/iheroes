from typing import Iterable, Optional

from iheroes_api.core.heroes.hero import CreateHeroDto, Hero, UpdateHeroDto
from iheroes_api.infra.database.models import Hero as HeroModel
from iheroes_api.infra.database.sqlalchemy import database


async def delete(user_id: int, id_: int) -> bool:
    if not await exists(id_):
        return False

    query = (
        HeroModel.delete()
        .where(HeroModel.c.user_id == user_id)
        .where(HeroModel.c.id == id_)
    )
    await database.execute(query)
    return True


async def exists(id_: int) -> bool:
    query = HeroModel.count().where(HeroModel.c.id == id_)
    return bool(await database.execute(query))


async def fetch(user_id: int, id_: int) -> Optional[Hero]:
    query = (
        HeroModel.select()
        .where(HeroModel.c.user_id == user_id)
        .where(HeroModel.c.id == id_)
    )

    result = await database.fetch_one(query)
    return Hero.parse_obj(dict(result)) if result else None


async def fetch_all() -> Iterable[Hero]:
    query = HeroModel.select()

    results = await database.fetch_all(query)
    return (Hero.parse_obj(dict(result)) for result in results)


async def fetch_all_by_user(user_id: int) -> Iterable[Hero]:
    query = HeroModel.select().where(HeroModel.c.user_id == user_id)

    results = await database.fetch_all(query)
    return (Hero.parse_obj(dict(result)) for result in results)


async def persist(user_id: int, dto: CreateHeroDto) -> Hero:
    values = {**dto.dict(), "user_id": user_id}
    query = HeroModel.insert().values(**values)

    last_record_id = await database.execute(query)
    return Hero.parse_obj({**values, "id": last_record_id})


async def update(user_id: int, dto: UpdateHeroDto, id_: int) -> Optional[Hero]:
    if not await exists(id_):
        return None

    values = dto.dict(exclude_unset=True)
    query = (
        HeroModel.update()
        .where(HeroModel.c.user_id == user_id)
        .where(HeroModel.c.id == id_)
        .values(**values)
    )
    await database.execute(query)

    return await fetch(user_id, id_)
