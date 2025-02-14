from src.model.creature import Creature

_creatures = [
    Creature(
        name="Yeti",
        aka="Abominable Snowman",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan"),
    Creature(
        name="Bigfoot",
        description="Yeti's Cousin Eddie",
        country="US",
        area="*",
        aka="Sasquatch"),
    Creature(
        name="Grandma Yaga",
        aka="Bone Leg",
        country="RU",
        area="Slavic Woods",
        description="Eats children"),
    Creature(
        name="Koshchey the Immortal",
        description="Old immortal count, rich, has own death inside egg",
        country="RU",
        area="*",
        aka="Immortal Count"),
    Creature(
        name="Zmey Gorynychi",
        aka="Zmey poganyi",
        country="RU",
        area="Golden Hord",
        description="Has three heads, breathes with fire"),
    Creature(
        name="Solovey the Rogue",
        description="Whist very load",
        country="RU",
        area="the ukraine",
        aka="Morda Blackassed"),
    Creature(
        name="Kolobok",
        aka="Rumyanyi back",
        country="RU",
        area="Villages, Woods",
        description="Had gone from Granddad, grandma, bear, wolf"),
    Creature(
        name="Kikimora",
        description="Lives in swamps, very hair and dirty",
        country="RU",
        area="Swamps",
        aka="Kikimora Bolotnaya"),
]

_sample_creatures = [
    Creature(
        name="test_creature_name",
        country="*",
        area="test_creature_areas",
        description="test_creature_description",
        aka="test_creature_aka",
    ),
    Creature(
        name="test_creature_name2",
        country="*",
        area="test_creature_areas",
        description="test_creature_description",
        aka="test_creature_aka",
    )
]

def get_all() -> list[Creature]:
    """Возврат всех существ"""
    return _creatures


def get_one(name: str) -> Creature | None:
    """Возврат одного существа"""
    name = str(name).lower()
    for _creature in _creatures:
        if _creature.name.lower() in name or name in _creature.name.lower():
            return _creature
    return None


def create(creature: Creature) -> Creature:
    """Добавление существа"""
    return creature


def modify(creature: Creature) -> Creature:
    """Частичное изменение записи существа"""
    return creature


def replace(creature: Creature) -> Creature:
    """Полная замена записи существа"""
    return creature


def delete(name: str):
    """Удаление записи существа; возврат значения None,
    если запись существовала"""
    return None
