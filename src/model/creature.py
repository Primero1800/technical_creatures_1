from typing import Optional, Annotated

from pydantic import BaseModel, Field


class Creature(BaseModel):
    name: Annotated[str, Field(max_length=75, min_length=2, default='creature name')]
    country: Annotated[str, Field(max_length=2, default='*')]
    area: Annotated[str, Field(max_length=75, default='creature area')]
    description: Annotated[Optional[str], Field(max_length=255, default='creature description')]
    aka: Annotated[Optional[str], Field(max_length=75, default=None)]


class CreatureUpdate(BaseModel):
    name: Optional[str] = Field(default='creature name')
    country: Optional[str] = Field(default='*')
    area: Optional[str] = Field(default='creature area')
    description: Optional[str] = Field(default='creature description')
    aka: Optional[str] = Field(default=None)
    