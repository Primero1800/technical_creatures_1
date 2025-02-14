from typing import Optional

from pydantic import BaseModel, Field


class Creature(BaseModel):
    name: str
    country: str
    area: str
    description: str
    aka: str


class CreatureUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    area: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    aka: Optional[str] = Field(default=None)
    