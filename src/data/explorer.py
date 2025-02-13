from sqlalchemy import text
from src.data.init import Session
from src.model.explorer import Explorer


def row_to_model(row: tuple) -> Explorer:
    name, country, description = row
    return Explorer(name=name, description=description, country=country)


def model_to_dict(explorer: Explorer) -> dict:
    return explorer.model_dump()


def get_one(name: str) -> Explorer:
    with Session() as session:
        query = "select * from explorer where name=:name"
        params = {"name": name}
        row = session.execute(text(query), params).fetchone()
    return row_to_model(row)


def get_all(name: str) -> list[Explorer]:
    with Session() as session:
        query = "select * from explorer"
        rows = session.execute(text(query)).fetchall()
    return [row_to_model(row) for row in rows]


def create(explorer: Explorer) -> Explorer:
    with Session() as session:
        query = """
            insert into explorer values
            (:name, :country, :description)
        """
        params = model_to_dict(explorer)
        session.execute(text(query), params)
    return get_one(explorer.name)


def modify(explorer: Explorer):
    with Session() as session:
        query = """
            update explorer
            set country=:country,
            name=:name,
            description=:description
            where name=:name_orig
        """
        params = model_to_dict(explorer)
        params["name_orig"] = explorer.name
        session.execute(text(query), params)
    return get_one(explorer.name)


def replace(explorer: Explorer):
    return explorer


def delete(explorer: Explorer) -> bool:
    with Session() as session:
        query = "delete from explorer where name = :name"
        params = {"name": explorer.name}
        result = session.execute(text(query), params)
        return bool(result)
