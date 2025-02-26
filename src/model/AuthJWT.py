from datetime import timedelta
from pathlib import Path
from pydantic import BaseModel


class AuthJWT(BaseModel):
    private_key: Path = None,
    public_key: Path = None,
    algorithm: str = "RS256",
    access_token_expire_minutes: float | None = float(3),
    refresh_token_expire_minutes: float | None = float(5),
    token_type_field: str = 'type',
    access_token_type: str = 'access',
    refresh_token_type: str = 'refresh',


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
