from operator import attrgetter
from typing import List, Union

from fastapi import Depends  # type: ignore
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse  # type: ignore
from fastapi.routing import APIRouter
from pydantic import BaseModel
from toolz import partial, pipe

from iheroes_api.api.container import Dependencies
from iheroes_api.core.accounts.user import UserRegistry
from iheroes_api.core.heroes import hero_service
from iheroes_api.core.heroes.exceptions import HeroNotUniqueError
from iheroes_api.core.heroes.hero import CreateHeroDto, Hero, UpdateHeroDto


# View models
class HeroNotUniqueResponse(BaseModel):
    class HeroNotUniqueDetail(BaseModel):
        type: str  # noqa: A003
        msg: str

    detail: HeroNotUniqueDetail


_get_dependencies = attrgetter("auth_module", "database", "hero_repo")


def _register_create_actions(deps: Dependencies, router: APIRouter) -> APIRouter:
    auth, database, hero_repo = _get_dependencies(deps)

    @router.post(
        "",
        status_code=201,
        response_model=Hero,
        responses={
            201: {"description": "User registered"},
            409: {
                "description": "Hero already registered",
                "model": HeroNotUniqueResponse,
            },
        },
    )
    @database.transaction()
    async def create(
        dto: CreateHeroDto, user: UserRegistry = Depends(auth.get_current_user)
    ) -> Hero:
        try:
            result = await hero_service.create(hero_repo, user, dto)
        except HeroNotUniqueError as err:
            raise HTTPException(409, detail=err.as_dict())
        return result

    return router


def _register_delete_actions(deps: Dependencies, router: APIRouter) -> APIRouter:
    auth, database, hero_repo = _get_dependencies(deps)

    @router.delete(
        "/{hero_id}",
        status_code=204,
        responses={
            204: {"description": "Hero deleted"},
            404: {"description": "Hero not found"},
        },
    )
    @database.transaction()
    async def delete(
        hero_id: int, user: UserRegistry = Depends(auth.get_current_user)
    ) -> JSONResponse:
        result = await hero_service.delete(hero_repo, user, hero_id)
        status_code = 204 if result else 404
        return JSONResponse(status_code=status_code)

    return router


def _register_read_actions(deps: Dependencies, router: APIRouter) -> APIRouter:
    auth, database, hero_repo = _get_dependencies(deps)

    @router.get(
        "",
        status_code=200,
        response_model=List[Hero],
        responses={200: {"description": "Heroes found"}},
    )
    @database.transaction()
    async def index(user: UserRegistry = Depends(auth.get_current_user),) -> List[Hero]:
        return list(await hero_service.get_all(hero_repo))

    @router.get(
        "/me",
        status_code=200,
        response_model=List[Hero],
        responses={200: {"description": "Heroes found"}},
    )
    @database.transaction()
    async def index_by_user(
        user: UserRegistry = Depends(auth.get_current_user),
    ) -> List[Hero]:
        return list(await hero_service.get_all_by_user(hero_repo, user))

    @router.get(
        "/{hero_id}",
        status_code=200,
        response_model=Hero,
        responses={
            200: {"description": "Hero found"},
            404: {"description": "Hero not found"},
        },
    )
    @database.transaction()
    async def show(
        hero_id: int, user: UserRegistry = Depends(auth.get_current_user)
    ) -> Union[Hero, JSONResponse]:
        hero = await hero_service.get(hero_repo, user, hero_id)
        if not hero:
            return JSONResponse(status_code=404)
        return hero

    return router


def _register_update_actions(deps: Dependencies, router: APIRouter) -> APIRouter:
    auth, database, hero_repo = _get_dependencies(deps)

    @router.put(
        "/{hero_id}",
        status_code=200,
        response_model=Hero,
        responses={
            200: {"description": "Hero updated"},
            404: {"description": "Hero not found"},
            409: {
                "description": "Hero already registered",
                "model": HeroNotUniqueResponse,
            },
        },
    )
    @database.transaction()
    async def update(
        hero_id: int,
        dto: UpdateHeroDto,
        user: UserRegistry = Depends(auth.get_current_user),
    ) -> Union[Hero, JSONResponse]:
        try:
            hero = await hero_service.update(hero_repo, user, dto, hero_id)
        except HeroNotUniqueError as err:
            raise HTTPException(409, detail=err.as_dict())
        return hero or JSONResponse(status_code=404)

    return router


def build_router(deps: Dependencies) -> APIRouter:
    router: APIRouter = pipe(
        APIRouter(default_response_class=JSONResponse),
        partial(_register_create_actions, deps),
        partial(_register_delete_actions, deps),
        partial(_register_read_actions, deps),
        partial(_register_update_actions, deps),
    )
    return router
