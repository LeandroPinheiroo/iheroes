from fastapi.applications import FastAPI

from iheroes_api.api.container import Dependencies
from iheroes_api.api.routers import account, root
from iheroes_api.config.environment import Settings


def register_routers(settings: Settings, deps: Dependencies, app: FastAPI) -> FastAPI:
    app.include_router(root.build_router(settings))
    app.include_router(account.build_router(settings, deps), prefix="/account")
    return app
