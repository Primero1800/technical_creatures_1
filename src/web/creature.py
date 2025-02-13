from fastapi import APIRouter
from src.model.creature import Creature
# import src.fake.creature as service
import src.service.creature as service


router = APIRouter(prefix='/creature')


@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> Creature | None:
    return service.get_one(name)


@router.post("/")
def create(creature: Creature) -> Creature:
    return service.create(creature)


@router.patch("/")
def modify(creature: Creature) -> Creature:
    return service.modify(creature)


@router.put("/")
def replace(creature: Creature) -> Creature:
    return service.replace(creature)


@router.delete("/{name}")
def delete(name: str):
    return None
