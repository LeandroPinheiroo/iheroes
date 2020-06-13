from fastapi.routing import APIRouter

from iheroes_api.api.container import Dependencies
from iheroes_api.config.environment import Settings

from . import auth, user


def build_router(setts: Settings, deps: Dependencies) -> APIRouter:
    rt = APIRouter()
    rt.include_router(auth.build_router(setts, deps), prefix="/oauth2", tags=["Auth"])
    rt.include_router(user.build_router(deps), prefix="/user", tags=["User"])

    return rt
