from fastapi import APIRouter
from starlette import status

from src.model.creature import Creature
# import src.fake.creature as service
import src.service.creature as service


router = APIRouter(prefix='/creature')


@router.get("", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.get("/", status_code=status.HTTP_200_OK)
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.get("/{name}/", status_code=status.HTTP_200_OK)
def get_one(name) -> Creature | None:
    return service.get_one(name)


@router.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(creature: Creature) -> Creature:
    return service.create(creature)


@router.patch("", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.patch("/", status_code=status.HTTP_200_OK)
def modify(creature: Creature) -> Creature:
    return service.modify(creature)


@router.put("", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.put("/", status_code=status.HTTP_200_OK)
def replace(creature: Creature) -> Creature:
    return service.replace(creature)


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
@router.delete("/{name}/", status_code=status.HTTP_204_NO_CONTENT)
def delete(name: str):
    return None
