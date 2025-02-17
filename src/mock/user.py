from src.model.creature import Creature
from src.model.user import User

_users = [
    Creature(
        name="primero",
        hash="12345678"),
    Creature(
        name="admin",
        hash="23456781"),
    Creature(
        name="abc",
        hash="34567812"),
    Creature(
        name="xyz",
        hash="45678123"),
    Creature(
        name="roto",
        hash="56781234"),
]

_sample_users = [
    Creature(
        name="user",
        hash="password"
    ),
    Creature(
        name="user2",
        hash="password2",
    )
]

def get_all() -> list[User]:
    """Возврат всех существ"""
    return _users


def get_one(name: str) -> User | None:
    """Возврат одного существа"""
    name = str(name).lower()
    for _user in _users:
        if _user.name.lower() in name or name in _user.name.lower():
            return _user
    return None


def create(user: User) -> User:
    """Добавление существа"""
    return user


def modify(user: User) -> User:
    """Частичное изменение записи существа"""
    return user


def replace(user: User) -> User:
    """Полная замена записи существа"""
    return user


def delete(name: str):
    """Удаление записи существа; возврат значения None,
    если запись существовала"""
    return None
