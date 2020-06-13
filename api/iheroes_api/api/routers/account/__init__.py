from fastapi.routing import APIRouter

from iheroes_api.api.container import Dependencies

from . import user


def build_router(deps: Dependencies) -> APIRouter:
    rt = APIRouter()
    rt.include_router(user.build_router(deps), prefix="/user", tags=["User"])

    return rt
