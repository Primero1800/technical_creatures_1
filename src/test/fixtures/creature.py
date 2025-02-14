import pytest
from src.mock.creature import _sample_creatures as sample_creatures
from src.model.creature import Creature


@pytest.fixture
def sample() -> Creature:
    return sample_creatures[0]


@pytest.fixture
def sample2() -> Creature:
    return sample_creatures[1]


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
