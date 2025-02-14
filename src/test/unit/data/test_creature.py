import pytest

from src.errors import Duplicate, Missing, Validation
from src.model.creature import Creature


from src.data import creature as data


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="test_creature_name",
        country="*",
        area="test_creature_areas",
        description="test_creature_description",
        aka="test_creature_aka",
    )


@pytest.fixture
def sample2() -> Creature:
    return Creature(
        name="test_creature_name2",
        country="*",
        area="test_creature_areas",
        description="test_creature_description",
        aka="test_creature_aka",
    )


@pytest.fixture
def sample_dict_(sample) -> dict:
    result = sample.model_dump()
    result['name'] += '_'
    return result


@pytest.fixture
def sample_dict(sample) -> dict:
    return sample.model_dump()


@pytest.fixture
def sample_dict_bad(sample) -> dict:
    result = sample.model_dump()
    result['country'] = '***'
    return result


@pytest.fixture
def sample_dict_duplicate(sample) -> dict:
    result = sample.model_dump()
    result['name'] += '2'
    return result


@pytest.fixture
def sample_dict_not_full(sample) -> dict:
    result = sample.model_dump()
    del result['country']
    result['aka'] += '_'
    return result


@pytest.fixture
def sample_dict_not_full_bad(sample) -> dict:
    result = sample.model_dump()
    result['country'] = '***'
    del result['aka']
    return result


@pytest.fixture
def sample_dict_extended(sample) -> dict:
    result = sample.model_dump()
    result['added'] = 'added'
    result['added2'] = 'added2'
    return result


def test_data_creature_create(sample):
    try:
        resp = data.create(sample)
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample


def test_data_creature_create2(sample2):
    try:
        resp = data.create(sample2)
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample2


def test_data_creature_create_duplicate(sample):
    try:
        resp = data.create(sample)
    except Duplicate as exc:
        resp = exc.msg
    assert resp == f"Creature {sample.name} already exists"


def test_data_creature_get_one(sample):
    try:
        resp = data.get_one(sample.name)
    except Missing as exc:
        resp = exc.msg
    assert resp == sample


def test_data_creature_get_one_missing(sample):
    try:
        resp = data.get_one(sample.name + '_test_preffix')
    except Missing as exc:
        resp = exc.msg
    assert resp == f"Creature {sample.name + '_test_preffix'} not found"


def test_data_creature_get_all(sample):
    resp = data.get_all()
    assert resp is not None
    assert type(resp) is list


def test_data_creature_modify(sample, sample_dict_):
    try:
        resp = data.modify(sample.name, sample_dict_)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert type(resp) is Creature
    assert resp.name == sample.name + '_'


def test_data_creature_modify_back(sample, sample_dict):
    try:
        resp = data.modify(sample.name + '_', sample_dict)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample


def test_data_creature_modify_bad(sample, sample_dict_bad):
    try:
        resp = data.modify(sample.name, sample_dict_bad)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp[0]['type'] == 'string_too_long'


def test_data_creature_modify_not_full(sample, sample_dict_not_full):
    try:
        resp = data.modify(sample.name, sample_dict_not_full)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp.name == sample.name
    assert resp.country == sample.country
    assert resp.area == sample.area
    assert resp.aka == sample.aka + '_'


def test_data_creature_modify_not_full_bad(sample, sample_dict_not_full_bad):
    try:
        resp = data.modify(sample.name, sample_dict_not_full_bad)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp[0]['type'] == 'string_too_long'


def test_data_creature_modify_extended(sample, sample_dict_extended):
    try:
        resp = data.modify(sample.name, sample_dict_extended)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample


def test_data_creature_modify_duplicate(sample, sample_dict_duplicate):
    try:
        resp = data.modify(sample.name, sample_dict_duplicate)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp == f"Creature {sample_dict_duplicate['name']} already exists"


def test_data_creature_put_back(sample):
    try:
        resp = data.replace(sample)
    except Missing as exc:
        resp = exc.msg
    assert resp == sample


def test_data_creature_delete(sample):
    try:
        resp = data.delete(sample.name)
    except Missing as exc:
        resp = None
    assert resp is True


def test_data_creature_delete2(sample2):
    try:
        resp = data.delete(sample2.name)
    except Missing as exc:
        resp = None
    assert resp is True


def test_data_creature_delete_duplicate(sample):
    try:
        resp = data.delete(sample.name)
    except Missing as exc:
        resp = exc.msg
    assert resp == f"Creature {sample.name} not found"


def test_data_creature_put_missing(sample):
    try:
        resp = data.replace(sample)
    except Missing as exc:
        resp = exc.msg
    assert resp == f"Creature {sample.name} not found"
