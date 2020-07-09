from fastapi.applications import FastAPI

from iheroes_api.api.container import Dependencies
from iheroes_api.api.routers import account, hero, root
from iheroes_api.config.environment import Settings


def register_routers(settings: Settings, deps: Dependencies, app: FastAPI) -> FastAPI:
    app.include_router(root.build_router(settings), tags=["Health Check"])
    app.include_router(account.build_router(settings, deps), prefix="/account")
    app.include_router(hero.build_router(deps), prefix="/hero", tags=["Hero"])
    return app
