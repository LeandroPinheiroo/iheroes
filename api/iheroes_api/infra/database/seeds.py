import logging
from typing import Any, Dict, Iterable

from databases import Database
from sqlalchemy.schema import Table

from iheroes_api.core.accounts import hash_service
from iheroes_api.infra.database.models import Hero, User
from iheroes_api.infra.database.sqlalchemy import (
    database_context,
    init_database,
    truncate_database,
)

logger = logging.getLogger(__name__)


async def _populate_table(
    db: Database, table: Table, values: Iterable[Dict[str, Any]],
):
    name: str = table.name
    query = table.insert()

    logger.info(f"Seeding table {name}")
    await db.execute_many(query, list(values))
    logger.info(f"Seeded table {name} successfully")


# Seeds
async def _populate_user(db: Database) -> None:
    values = [
        {
            "email": "john.doe@gmail.com",
            "password_hash": hash_service.hash_("dev@1234"),
        },
        {
            "email": "jane.doe@gmail.com",
            "password_hash": hash_service.hash_("dev2@1234"),
        },
        {
            "email": "mark.fisher@yahoo.com",
            "password_hash": hash_service.hash_("dev3@1234"),
        },
        {
            "email": "ann.tobias@outlook.com",
            "password_hash": hash_service.hash_("dev4@1234"),
        },
    ]
    await _populate_table(db, User, values)


async def _populate_heroes(db: Database) -> None:
    values = [
        {
            "user_id": 1,
            "name": "Jim Corrigan",
            "nickname": "The Spectre",
            "location": {"lat": 34.0192077, "lng": -118.9722329},
            "power_class": "S",
        },
        {
            "user_id": 1,
            "name": "Clark Kent",
            "nickname": "Superman",
            "location": {"lat": 38.8935128, "lng": -77.1546632},
            "power_class": "A",
        },
        {
            "user_id": 1,
            "name": "Diana of Themyscira",
            "nickname": "Wonder Woman",
            "location": {"lat": 33.7675912, "lng": -92.2641579},
            "power_class": "A",
        },
        {
            "user_id": 1,
            "name": "Barry Allen",
            "nickname": "Flash",
            "location": {"lat": 39.9826141, "lng": -83.2710256},
            "power_class": "A",
        },
        {
            "user_id": 1,
            "name": "Billy Batson",
            "nickname": "Shazam",
            "location": {"lat": 42.9784063, "lng": -109.7983399},
            "power_class": "A",
        },
        {
            "user_id": 1,
            "name": "Bruce Wayne",
            "nickname": "Batman",
            "location": {"lat": 40.6971494, "lng": -74.2598771},
            "power_class": "B",
        },
        {
            "user_id": 1,
            "name": "Jason Todd",
            "nickname": "Robin",
            "location": {"lat": 40.6451594, "lng": -74.0850845},
            "power_class": "B",
        },
        {
            "user_id": 1,
            "name": "Oliver Jonas Queen",
            "nickname": "Green Arrow",
            "location": {"lat": 37.7576793, "lng": -122.5076408},
            "power_class": "C",
        },
        {
            "user_id": 2,
            "name": "Jonathan Osterman",
            "nickname": "Doctor Manhattan",
            "location": {"lat": 40.7590403, "lng": -74.0392717},
            "power_class": "S",
        },
        {
            "user_id": 2,
            "name": "Adrian Alexander Veidt",
            "nickname": "Ozymandias",
            "location": {"lat": 40.7664046, "lng": -74.2168404},
            "power_class": "B",
        },
        {
            "user_id": 2,
            "name": "Walter Kovacs",
            "nickname": "Rorschach",
            "location": {"lat": 40.0513886, "lng": -76.9683128},
            "power_class": "C",
        },
        {
            "user_id": 2,
            "name": "Daniel Dreiberg",
            "nickname": "Nite Owl",
            "location": {"lat": 40.6506794, "lng": -74.1513882},
            "power_class": "C",
        },
        {
            "user_id": 2,
            "name": "Laurel Jane Juspeczyk",
            "nickname": "Silk Spectre",
            "location": {"lat": 40.7029282, "lng": -73.6558511},
            "power_class": "C",
        },
        {
            "user_id": 2,
            "name": "Edward Morgan Blake",
            "nickname": "The Comedian",
            "location": {"lat": 40.8516388, "lng": -73.9109746},
            "power_class": "C",
        },
    ]
    await _populate_table(db, Hero, values)


# Runner
seeds = [_populate_user, _populate_heroes]


async def run() -> None:
    logger.info("Initializing databases")
    init_database()
    async with database_context() as database:
        logger.info("Truncating database")
        await truncate_database()
        logger.info("Populating database")
        for fn in seeds:
            await fn(database)
        logger.info("Finished populating PostgreSQL database")
