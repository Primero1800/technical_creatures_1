import os

import pytest
from src.mock.user import _sample_users as sample_users
from src.model.user import User


@pytest.fixture
def sample() -> User:
    return sample_users[0]


@pytest.fixture
def sample2() -> User:
    return sample_users[1]


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
    result['name'] = 'a'
    return result


@pytest.fixture
def sample_dict_duplicate(sample) -> dict:
    result = sample.model_dump()
    result['name'] += '2'
    return result


@pytest.fixture
def sample_dict_not_full(sample) -> dict:
    result = sample.model_dump()
    del result['hash']
    return result


@pytest.fixture
def sample_dict_not_full_bad(sample) -> dict:
    result = sample.model_dump()
    result['name'] = 'a'
    del result['hash']
    return result


@pytest.fixture
def sample_dict_extended(sample) -> dict:
    result = sample.model_dump()
    result['added'] = 'added'
    result['added2'] = 'added2'
    return result


@pytest.fixture
def oauth2data(sample) -> dict:
    return {
        'grant_type': "password",
        'username': sample.name,
        'password': sample.hash,
        'scope': "",
        'client_id': os.getenv('OAUTH_CLIENT_ID'),
        'client_secret': os.getenv('SECRET_KEY'),
    }
