from sqlalchemy import text
from src.data.init import Session, IntegrityError
from src.errors import Missing, Duplicate
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
        if row:
            return row_to_model(row)
        else:
            raise Missing(msg=f"Explorer {name} not found")


def get_all() -> list[Explorer]:
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

        try:
            session.execute(text(query), params)
            session.commit()
        except IntegrityError:
            raise Duplicate(msg=f"Explorer {explorer.name} already exists")
    return get_one(explorer.name)


def modify(name: str, explorer: Explorer):
    if not (name and explorer):
        raise Missing(msg=f"Explorer not found")
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
        result= session.execute(text(query), params)
        print("ROWS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", result.rowcount)
        if result.rowcount > 0:
            session.commit()
            return get_one(explorer.name)
        else:
            raise Missing(msg=f"Explorer {explorer.name} not found")


def replace(explorer: Explorer):
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
        result = session.execute(text(query), params)
        if result.rowcount > 0:
            session.commit()
            return get_one(explorer.name)
        else:
            raise Missing(msg=f"Explorer {explorer.name} not found")


def delete(name: str) -> bool:
    with Session() as session:
        query = "delete from explorer where name = :name"
        params = {"name": name}
        result = session.execute(text(query), params)
        session.commit()
        if result.rowcount > 0:
            return True
        else:
            raise Missing(msg=f"Explorer {name} not found")
