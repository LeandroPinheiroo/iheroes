from datetime import datetime, timedelta
from operator import attrgetter
from types import SimpleNamespace
from typing import Any, Dict, Tuple

import jwt
from fastapi import Depends  # type: ignore
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer  # type: ignore

from iheroes_api.api.protocols import AuthModule
from iheroes_api.config.environment import Settings
from iheroes_api.core.accounts import user_service
from iheroes_api.core.accounts.user import UserRegistry
from iheroes_api.core.protocols import UserRepo

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/oauth2/token")


def build_auth_module(setts: Settings, repo: UserRepo) -> AuthModule:
    secret_key, algorithm = attrgetter("JWT_SECRET_KEY", "JWT_ALGORITHM")(setts)

    def decode_token(token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(token, secret_key, algorithms=[algorithm])
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=401,
                detail="invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def encode_token(
        *, data: Dict[str, Any], expires_delta: timedelta
    ) -> Tuple[bytes, float]:
        expire = datetime.utcnow() + expires_delta
        access_token = jwt.encode(
            {**data.copy(), "exp": expire}, secret_key, algorithm=algorithm
        )
        return access_token, expire.timestamp()

    async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserRegistry:
        payload = decode_token(token)
        _, id_ = str(payload.get("sub")).split(":")
        user = await user_service.get_by_id_or_raise(repo, int(id_))
        return user

    return SimpleNamespace(
        decode_token=decode_token,
        encode_token=encode_token,
        get_current_user=get_current_user,
    )
