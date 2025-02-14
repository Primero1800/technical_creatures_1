from typing import Optional

from pydantic import BaseModel, Field


class Explorer(BaseModel):
    name: str
    country: str
    description: str


class ExplorerUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    