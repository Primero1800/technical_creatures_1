from fastapi import APIRouter, HTTPException
from starlette import status

from src.errors import Duplicate, Missing
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
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(explorer: Explorer) -> Explorer:
    try:
        return service.create(explorer)
    except Duplicate as exc:
        raise HTTPException(status_code=403, detail=exc.msg)



@router.patch("", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.patch("/", status_code=status.HTTP_200_OK)
def modify(name: str, explorer: ExplorerUpdate) -> Explorer:
    try:
        return service.modify(name, explorer)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    except Exception as exc:
        raise HTTPException(status_code=403, detail=exc)


@router.put("", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.put("/", status_code=status.HTTP_200_OK)
def replace(explorer: Explorer) -> Explorer:
    try:
        return service.replace(explorer)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
@router.delete("/{name}/", status_code=status.HTTP_204_NO_CONTENT)
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
