from typing import Annotated, Optional
from pydantic import BaseModel, Field, SecretStr


class User(BaseModel):
    name: Annotated[str, Field(min_length=2, default='username')]
    hash: Annotated[SecretStr, Field(min_length=8, )]


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default='username')
    hash: Optional[str] = Field(default='********')
