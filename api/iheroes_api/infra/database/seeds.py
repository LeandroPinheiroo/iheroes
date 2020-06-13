import logging
from typing import Any, Dict, Iterable

from databases import Database
from sqlalchemy.schema import Table

from iheroes_api.core.accounts import hash_service
from iheroes_api.infra.database.models import User
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


# Runner
seeds = [_populate_user]


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
