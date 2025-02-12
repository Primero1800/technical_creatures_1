from fastapi import APIRouter
from src.model.creature import Creature
import src.fake.creature as service


router = APIRouter(prefix='/creature')


@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> Creature | None:
    return service.get_one(name)


@router.post("/")
def create(explorer: Creature) -> Creature:
    return service.create(explorer)


@router.patch("/")
def modify(explorer: Creature) -> Creature:
    return service.modify(explorer)


@router.put("/")
def replace(explorer: Creature) -> Creature:
    return service.replace(explorer)


@router.delete("/{name}")
def delete(name: str):
    return None
