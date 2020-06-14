from datetime import timedelta
from operator import attrgetter
from typing import Literal

from fastapi import Depends  # type: ignore
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse  # type: ignore
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm  # type: ignore
from pydantic import BaseModel

from iheroes_api.api.container import Dependencies
from iheroes_api.config.environment import Settings
from iheroes_api.core.accounts import user_service
from iheroes_api.core.accounts.user import Credentials, UserRegistry


class Token(BaseModel):
    token_type: Literal["bearer"] = "bearer"
    access_token: str
    expire: int


def build_router(setts: Settings, deps: Dependencies) -> APIRouter:
    router = APIRouter(default_response_class=JSONResponse)
    access_expire = attrgetter("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")(setts)
    auth, repo = attrgetter("auth_module", "user_repo")(deps)

    @router.post(
        "/token",
        response_model=Token,
        responses={
            200: {"description": "User authenticated"},
            401: {"description": "User unauthenticated"},
        },
    )
    async def token(form_data: OAuth2PasswordRequestForm = Depends()):
        username, password = attrgetter("username", "password")(form_data)
        credentials = Credentials(email=username, password=password)

        user = await user_service.get_by_credentials(repo, credentials)
        if not user:
            raise HTTPException(
                status_code=401, detail="invalid authentication credentials",
            )

        at, exp_at = auth.encode_token(
            data={"sub": f"userid:{user.id}", "grant_type": "access"},
            expires_delta=timedelta(minutes=access_expire),
        )

        return Token(access_token=at, expire=exp_at)

    @router.get(
        "/introspect",
        response_model=UserRegistry,
        responses={
            200: {"description": "User registry"},
            401: {"description": "User unauthorized"},
        },
    )
    def introspect(user: UserRegistry = Depends(auth.get_current_user)):
        return user

    return router
