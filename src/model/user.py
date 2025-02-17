from typing import Annotated

from pydantic import BaseModel, Field, SecretStr


class User(BaseModel):
    name: Annotated[str, Field(min_length=2, default='username')]
    hash: Annotated[SecretStr, Field(min_length=8, )]
