from fastapi import APIRouter
from src.model.explorer import Explorer
import src.fake.explorer as service

router = APIRouter(prefix='/explorer')


@router.get("")
@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{name}")
@router.get("/{name}/")
def get_one(name) -> Explorer | None:
    return service.get_one(name)


@router.post("")
@router.post("/")
def create(explorer: Explorer) -> Explorer:
    return service.create(explorer)


@router.patch("")
@router.patch("/")
def modify(explorer: Explorer) -> Explorer:
    return service.modify(explorer)


@router.put("")
@router.put("/")
def replace(explorer: Explorer) -> Explorer:
    return service.replace(explorer)


@router.delete("/{name}")
@router.delete("/{name}/")
def delete(name: str):
    return None
