from typing import Optional, Annotated

from pydantic import BaseModel, Field


class Explorer(BaseModel):
    name: Annotated[str, Field(max_length=75, min_length=2, default='explorer name')]
    country: Annotated[str, Field(max_length=2, default='*')]
    description: Annotated[Optional[str], Field(max_length=255, default='explorer description')]


class ExplorerUpdate(BaseModel):
    name: Optional[str] = Field(default='explorer name')
    country: Optional[str] = Field(default='*')
    description: Optional[str] = Field(default='explorer description')
    