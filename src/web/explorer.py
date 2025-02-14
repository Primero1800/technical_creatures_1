from fastapi import APIRouter
from fastapi.params import Body
from starlette import status

from src.model.explorer import Explorer, ExplorerUpdate
import src.service.explorer as service

router = APIRouter(prefix='/explorer')


@router.get("", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.get("/", status_code=status.HTTP_200_OK)
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{name}", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.get("/{name}/", status_code=status.HTTP_200_OK)
def get_one(name) -> Explorer | None:
    return service.get_one(name)


@router.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(explorer: Explorer) -> Explorer:
    return service.create(explorer)


@router.patch("", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.patch("/", status_code=status.HTTP_200_OK)
def modify(name: str, explorer: ExplorerUpdate) -> Explorer:
    return service.modify(name, explorer.model_dump(exclude_unset=True))


@router.put("", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.put("/", status_code=status.HTTP_200_OK)
def replace(explorer: Explorer) -> Explorer:
    return service.replace(explorer)


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
@router.delete("/{name}/", status_code=status.HTTP_204_NO_CONTENT)
def delete(name: str):
    return service.delete(name)
