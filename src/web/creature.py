from fastapi import APIRouter, HTTPException
from starlette import status

from src.errors import Missing, Duplicate, Validation
from src.model.creature import Creature, CreatureUpdate
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
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(creature: Creature) -> Creature:
    try:
        return service.create(creature)
    except Duplicate as exc:
        raise HTTPException(status_code=400, detail=exc.msg)


@router.patch("", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.patch("/", status_code=status.HTTP_200_OK)
def modify(name: str, creature: CreatureUpdate) -> Creature:
    try:
        return service.modify(name, creature.model_dump(exclude_unset=True))
    except (Missing, Duplicate) as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    except Validation as exc:
        raise HTTPException(status_code=400, detail=exc.msg)


@router.put("", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.put("/", status_code=status.HTTP_200_OK)
def replace(creature: Creature) -> Creature:
    try:
        return service.replace(creature)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
@router.delete("/{name}/", status_code=status.HTTP_204_NO_CONTENT)
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
