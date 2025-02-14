from src.model.explorer import Explorer

_explorers = [
    Explorer(name="Claude Hande",
        country="FR",
        description="Scarce during full moons"),
    Explorer(name="Noah Weiser",
        country="DE",
        description="Myopic machete man"),
    Explorer(name="Ivan Susanin",
             country="RU",
             description="Best worker ever"),
    Explorer(name="Ded Mazai",
             country="RU",
             description="Best friend of hears and other animals"),
]

_sample_explorers = [
    Explorer(
        name="test_explorer_name",
        country="*",
        description="test_explorer_description"),
    Explorer(
        name="test_explorer_name2",
        country="*",
        description="test_explorer_description"),
]


def get_all() -> list[Explorer]:
    return _explorers


def get_one(name: str) -> Explorer | None:
    name = str(name).lower()
    for _explorer in _explorers:
        if _explorer.name.lower() in name or name in _explorer.name.lower():
            return _explorer
    return None


def create(explorer: Explorer) -> Explorer:
    """Добавление исследователя"""
    return explorer


def modify(explorer: Explorer) -> Explorer:
    """Частичное изменение записи исследователя"""
    return explorer


def replace(explorer: Explorer) -> Explorer:
    """Полная замена записи исследователя"""
    return explorer


def delete(name: str) -> bool | None:
    """Удаление записи исследователя; возврат значения None,
    если запись существовала"""
    return None
