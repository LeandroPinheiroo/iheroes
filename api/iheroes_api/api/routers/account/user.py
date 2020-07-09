from operator import attrgetter

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
    class EmailNotUniqueDetail(BaseModel):
        msg: str
        email: str

    detail: EmailNotUniqueDetail


def build_router(deps: Dependencies) -> APIRouter:
    router = APIRouter(default_response_class=JSONResponse)
    database, user_repo = attrgetter("database", "user_repo")(deps)

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
    async def post(credentials: Credentials,) -> UserRegistry:
        try:
            result = await user_service.register(user_repo, credentials)
        except EmailNotUniqueError as err:
            raise HTTPException(409, detail=err.as_dict())
        return result

    return router
