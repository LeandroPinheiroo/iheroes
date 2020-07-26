from functools import partial

from fastapi.applications import FastAPI
from toolz import pipe

from iheroes_api.api.container import Dependencies, get_dependencies
from iheroes_api.api.listener import init_sio_client
from iheroes_api.api.routers import register_routers as register_routers
from iheroes_api.config.environment import Settings
from iheroes_api.infra.database.sqlalchemy import connect_database, disconnect_database
from iheroes_api.infra.database.sqlalchemy import init_database as init_pgsql_db


def create_instance(settings: Settings) -> FastAPI:
    return FastAPI(
        debug=settings.WEB_APP_DEBUG,
        title=settings.WEB_APP_TITLE,
        description=settings.WEB_APP_DESCRIPTION,
        version=settings.WEB_APP_VERSION,
    )


def init_databases(app: FastAPI) -> FastAPI:
    init_pgsql_db()
    return app


def init_listener(settings: Settings, deps: Dependencies, app: FastAPI) -> FastAPI:
    return init_sio_client(settings, deps, app)


def register_events(app: FastAPI) -> FastAPI:
    app.on_event("startup")(connect_database)
    app.on_event("shutdown")(disconnect_database)

    return app


def register_middlewares(app: FastAPI) -> FastAPI:
    return app


def init_app(settings: Settings) -> FastAPI:
    deps = get_dependencies()
    app: FastAPI = pipe(
        settings,
        create_instance,
        init_databases,
        register_events,
        register_middlewares,
        partial(init_listener, settings, deps),
        partial(register_routers, settings, deps),
    )

    return app
