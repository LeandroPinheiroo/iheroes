from operator import attrgetter
from typing import List, Union

from fastapi import Depends  # type: ignore
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse  # type: ignore
from fastapi.routing import APIRouter
from pydantic import BaseModel

from iheroes_api.api.container import Dependencies
from iheroes_api.core.accounts.user import UserRegistry
from iheroes_api.core.heroes import hero_service
from iheroes_api.core.heroes.exceptions import HeroNotUniqueError
from iheroes_api.core.heroes.hero import CreateHeroDto, Hero, UpdateHeroDto


# View models
class HeroNotUniqueResponse(BaseModel):
    class HeroNotUniqueDetail(BaseModel):
        msg: str
        user_id: str
        hero_name: str
        hero_nickname: str

    detail: HeroNotUniqueDetail


def build_router(deps: Dependencies) -> APIRouter:
    router = APIRouter(default_response_class=JSONResponse)

    auth, database, hero_repo = attrgetter("auth_module", "database", "hero_repo")(deps)

    # ----- CREATE -----
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

    # ----- READ -----
    @router.get(
        "/index",
        status_code=200,
        response_model=List[Hero],
        responses={200: {"description": "Heroes found"}},
    )
    @database.transaction()
    async def index(user: UserRegistry = Depends(auth.get_current_user),) -> List[Hero]:
        return list(await hero_service.get_all(hero_repo))

    @router.get(
        "",
        status_code=200,
        response_model=List[Hero],
        responses={200: {"description": "Heroes found"}},
    )
    @database.transaction()
    async def list_by_user(
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

    # ----- UPDATE -----
    @router.put(
        "/{hero_id}",
        status_code=200,
        response_model=Hero,
        responses={
            200: {"description": "Hero updated"},
            404: {"description": "Hero not found"},
        },
    )
    @database.transaction()
    async def update(
        hero_id: int,
        dto: UpdateHeroDto,
        user: UserRegistry = Depends(auth.get_current_user),
    ) -> Union[Hero, JSONResponse]:
        hero = await hero_service.update(hero_repo, user, dto, hero_id)
        return hero or JSONResponse(status_code=404)

    # ----- DELETE -----
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
