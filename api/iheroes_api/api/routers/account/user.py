from functools import partial

from fastapi import Depends  # type: ignore
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse  # type: ignore
from fastapi.routing import APIRouter
from pydantic import BaseModel

from iheroes_api.api.container import Dependencies
from iheroes_api.core.accounts import user_service
from iheroes_api.core.accounts.exceptions import EmailNotUniqueError
from iheroes_api.core.accounts.user import Credentials, UserRegistry


# View models
class EmailNotUniqueResponse(BaseModel):
    class Detail(BaseModel):
        msg: str
        email: str

    detail: Detail


def build_router(deps: Dependencies) -> APIRouter:
    router = APIRouter(default_response_class=JSONResponse)
    database = deps.database

    @router.post(
        "",
        status_code=201,
        response_model=UserRegistry,
        responses={
            201: {"description": "User registered", "model": UserRegistry},
            409: {
                "description": "User already registered",
                "model": EmailNotUniqueResponse,
            },
        },
    )
    @database.transaction()
    async def post(
        credentials: Credentials,
        service=Depends(lambda: partial(user_service.register, deps.user_repo)),
    ) -> UserRegistry:
        try:
            result: UserRegistry = await service(credentials)
            return result
        except EmailNotUniqueError as err:
            raise HTTPException(409, detail=err.as_dict())

    return router
