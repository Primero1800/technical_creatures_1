from pydantic import ValidationError
from sqlalchemy import text
from src.data.init import Session, IntegrityError
from src.errors import Missing, Duplicate, Validation
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
        row = session.execute(text(query), params).fetchone()
        if row:
            return row_to_model(row)
        else:
            raise Missing(msg=f"Creature {name} not found")


def get_all() -> list[Creature]:
    with Session() as session:
        query = "select * from creature"
        rows = session.execute(text(query)).fetchall()
    return [row_to_model(row) for row in rows]


def create(creature: Creature) -> Creature:
    with Session() as session:
        query = """
            insert into creature values
            (:name, :description, :country, :area, :aka)
        """
        params = model_to_dict(creature)
        try:
            session.execute(text(query), params)
            session.commit()
        except IntegrityError:
            raise Duplicate(msg=f"Creature {creature.name} already exists")
    return get_one(creature.name)


def modify(name: str, params: dict):
    creature = get_one(name)
    if not params:
        raise Missing(msg=f"Explorer {creature.name}: changes not found")

    params = {key:params[key] if key in params else val for key, val in model_to_dict(creature).items()}
    try:
        creature = Creature(**params)
    except ValidationError as exc:
        raise Validation(msg=exc.errors())

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
        params["name_orig"] = name
        try:
            result = session.execute(text(query), params)
        except IntegrityError:
            raise Duplicate(msg=f"Creature {creature.name} already exists")
        if result.rowcount > 0:
            session.commit()
            return get_one(params['name'])
        else:
            raise Missing(msg=f"Creature {params['name']} not found")


def replace(creature: Creature):
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
        result = session.execute(text(query), params)
        if result.rowcount > 0:
            session.commit()
            return get_one(creature.name)
        else:
            raise Missing(msg=f"Creature {creature.name} not found")


def delete(name: str) -> bool:
    with Session() as session:
        query = "delete from creature where name = :name"
        params = {"name": name}
        result = session.execute(text(query), params)
        session.commit()
        if result.rowcount > 0:
            return True
        else:
            raise Missing(msg=f"Creature {name} not found")
