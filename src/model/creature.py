from typing import Optional, Annotated

from pydantic import BaseModel, Field


class Creature(BaseModel):
    name: Annotated[str, Field(max_length=75, min_length=2)]
    country: Annotated[str, Field(max_length=2, default='*')]
    area: Annotated[str, Field(max_length=75, default='')]
    description: Annotated[Optional[str], Field(max_length=255)]
    aka: Annotated[Optional[str], Field(max_length=75)]


class CreatureUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    area: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    aka: Optional[str] = Field(default=None)
    