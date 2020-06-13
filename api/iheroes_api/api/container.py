from dataclasses import dataclass
from typing import Callable, cast

from databases import Database

from iheroes_api.api.auth import build_auth_module
from iheroes_api.api.protocols import AuthModule
from iheroes_api.config.environment import get_settings
from iheroes_api.core.protocols import UserRepo
from iheroes_api.infra.database.repositories import user_repository
from iheroes_api.infra.database.sqlalchemy import database

_settings = get_settings()


@dataclass(frozen=True)
class Dependencies:
    auth_module: AuthModule
    database: Database
    user_repo: UserRepo


def _build_dependencies() -> Callable[[], Dependencies]:
    deps = Dependencies(
        auth_module=build_auth_module(_settings, cast(UserRepo, user_repository)),
        database=database,
        user_repo=cast(UserRepo, user_repository),
    )

    def fn() -> Dependencies:
        return deps

    return fn


get_dependencies = _build_dependencies()
