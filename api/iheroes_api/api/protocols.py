from typing import Any, Dict, Protocol, Tuple

from iheroes_api.core.accounts.user import UserRegistry


class AuthModule(Protocol):
    def decode_token(self, token: str) -> int:
        ...

    def encode_token(self, *, data: Dict[str, Any]) -> Tuple[bytes, float]:
        ...

    async def get_current_user(self, token: str) -> UserRegistry:
        ...
