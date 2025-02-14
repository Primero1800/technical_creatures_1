import pytest
from src.mock.explorer import _sample_explorers as sample_explorers
from src.model.explorer import Explorer


@pytest.fixture
def sample() -> Explorer:
    return sample_explorers[0]


@pytest.fixture
def sample2() -> Explorer:
    return sample_explorers[1]


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
    result['description'] += '_'
    return result


@pytest.fixture
def sample_dict_not_full_bad(sample) -> dict:
    result = sample.model_dump()
    result['country'] = '***'
    del result['description']
    return result


@pytest.fixture
def sample_dict_extended(sample) -> dict:
    result = sample.model_dump()
    result['added'] = 'added'
    result['added2'] = 'added2'
    return result
