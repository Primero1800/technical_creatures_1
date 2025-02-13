from sqlalchemy import create_engine, text
from src.data.init import Session
from src.model.creature import Creature


def row_to_model(row: tuple) -> Creature:
    name, description, country, area, aka = row
    return Creature(name=name, description=description, country=country, area=area, aka=aka)


def model_to_dict(creature: Creature) -> dict:
    return creature.model_dump()


def get_one(name: str) -> Creature:
    with Session() as session:
        query = "select * from creature where name=:name"
        params = {"name": name}
        row = session.execute(text(query), params).scalar_one_or_none()
    return row_to_model(row)


def get_all(name: str) -> list[Creature]:
    with Session() as session:
        query = "select * from creature"
        rows = session.execute(text(query)).fetchall()
    return [row_to_model(row[0]) for row in rows]


def create(creature: Creature) -> Creature:
    with Session() as session:
        query = """
            insert into creature values
            (:name, :description, :country, :area, :aka)
        """
        params = model_to_dict(creature)
        session.execute(text(query), params)
    return get_one(creature.name)


def modify(creature: Creature):
    with Session() as session:
        query = """
            update creature
            set country=:country,
            name=:name,
            description=:description,
            area=:area,
            aka=:aka
            where name=:name_orig
        """
        params = model_to_dict(creature)
        params["name_orig"] = creature.name
        session.execute(text(query), params)
    return get_one(creature.name)


def replace(creature: Creature):
    return creature


def delete(creature: Creature) -> bool:
    with Session() as session:
        query = "delete from creature where name = :name"
        params = {"name": creature.name}
        result = session.execute(text(query), params)
        return bool(result)
