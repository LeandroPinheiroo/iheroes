from dataclasses import dataclass
from typing import Callable, cast

from databases import Database

from iheroes_api.core.protocols import UserRepo
from iheroes_api.infra.database.repositories import user_repository
from iheroes_api.infra.database.sqlalchemy import database


@dataclass(frozen=True)
class Dependencies:
    database: Database
    user_repo: UserRepo


def _build_dependencies() -> Callable[[], Dependencies]:
    deps = Dependencies(database=database, user_repo=cast(UserRepo, user_repository))

    def fn() -> Dependencies:
        return deps

    return fn


get_dependencies = _build_dependencies()
