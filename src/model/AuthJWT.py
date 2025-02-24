from pathlib import Path
from pydantic import BaseModel


class AuthJWT(BaseModel):
    private_key: Path = None,
    public_key: Path = None,
    algorithm: str = "RS256"


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
