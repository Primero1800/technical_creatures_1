from pydantic import ValidationError
from sqlalchemy import text
from src.data.init import Session, IntegrityError
from src.errors import Missing, Duplicate, Validation
from src.model.user import User


def row_to_model(row: tuple) -> User:
    name, hash = row
    return User(name=name, hash=hash)


def model_to_dict(user: User) -> dict:
    return user.model_dump()


def get_one(name: str) -> User:
    with Session() as session:
        query = "select * from user_active where name=:name"
        params = {"name": name}
        row = session.execute(text(query), params).fetchone()
        if row:
            return row_to_model(row)
        else:
            raise Missing(msg=f"User {name} not found")


def get_all() -> list[User]:
    with Session() as session:
        query = "select * from user_active"
        rows = session.execute(text(query)).fetchall()
    return [row_to_model(row) for row in rows]


def create(user: User, table: str = "user_active") -> User:
    with Session() as session:
        query = f"""
            insert into {table} values
            (:name, :hash)
        """
        params = model_to_dict(user)
        try:
            session.execute(text(query), params)
            session.commit()
        except IntegrityError:
            raise Duplicate(msg=f"User {user.name} already exists")
    return get_one(user.name)


def modify(name: str, params: dict):
    user = get_one(name)
    if not params:
        raise Missing(msg=f"User {user.name}: changes not found")

    params = {key:params[key] if key in params else val for key, val in model_to_dict(user).items()}
    try:
        user = User(**params)
    except ValidationError as exc:
        raise Validation(msg=exc.errors())

    with Session() as session:
        query = """
            update user_active
            set name=:name,
            hash=:hash
            where name=:name_orig
        """
        params["name_orig"] = name
        try:
            result = session.execute(text(query), params)
        except IntegrityError:
            raise Duplicate(msg=f"User {user.name} already exists")
        if result.rowcount > 0:
            session.commit()
            return get_one(params['name'])
        else:
            raise Missing(msg=f"User {params['name']} not found")


def delete(name: str) -> bool:
    with Session() as session:
        user = get_one(name)
        query = "delete from user_active where name = :name"
        params = {"name": name}
        result = session.execute(text(query), params)
        session.commit()
        if result.rowcount > 0:
            create(user, table="user_deleted")
            return True
        else:
            raise Missing(msg=f"User {name} not found")
