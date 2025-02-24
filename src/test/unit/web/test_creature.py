import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.utils.errors import Missing
from src.mock.creature import _creatures as mock_creatures
from src.test.fixtures.creature import (
    sample, sample2, sample_dict, sample_dict_, sample_dict_extended, sample_dict_duplicate,
    sample_dict_bad, sample_dict_not_full, sample_dict_not_full_bad
)
from src.web import creature
import src.service.creature as service


@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(creature.router)
    return app


@pytest.fixture
def test_client(test_app):
    return TestClient(test_app)


def test_get_all_creatures_mocked(test_client, mocker):
    mock = mocker.patch.object(service, 'get_all', return_value=mock_creatures)
    response = test_client.get("/creature/")
    assert mock.called
    assert response.status_code == 200
    assert response.json() == [item.model_dump() for item in mock_creatures]


def test_get_all_creatures(test_client):
    response = test_client.get("/creature/")
    assert response.status_code == 200
    assert type(json.loads(response.text)) is list


def test_get_one_creature_success_mocked(test_client, mocker):
    mock_creature = mock_creatures[0]
    mock = mocker.patch.object(service, 'get_one', return_value=mock_creature)

    response = test_client.get(f"/creature/{mock_creature.name}/")
    assert mock.called
    assert response.status_code == 200
    assert response.json() == mock_creature.model_dump()


def test_get_one_creature_missing_mocked(test_client, mocker):
    mock_creature = mock_creatures[0]
    bad_name = mock_creature.name + '_bad'
    mock = mocker.patch.object(service, 'get_one', side_effect=Missing(f"Creature {bad_name} not found"))

    response = test_client.get(f"/creature/{bad_name}/")
    assert mock.called
    assert response.status_code == 404
    assert response.json() == {"detail": f"Creature {bad_name} not found"}


def test_create_creature_success(test_client, sample):
    response = test_client.post("/creature/", json=sample.model_dump())
    assert response.status_code == 201
    assert json.loads(response.text) == sample.model_dump()


def test_create_creature_failure(test_client, sample):
    response = test_client.post("/creature/", json=sample.model_dump())
    assert response.status_code == 400
    assert json.loads(response.text) == {'detail': f"Creature {sample.name} already exists"}


def test_create_creature2_success(test_client, sample2):
    response = test_client.post("/creature/", json=sample2.model_dump())
    assert response.status_code == 201
    assert json.loads(response.text) == sample2.model_dump()


def test_get_one_success(test_client, sample):
    response = test_client.get(f"/creature/{sample.name}")
    assert response.status_code == 200
    assert json.loads(response.text) == sample.model_dump()


def test_get_one_failure(test_client, sample):
    response = test_client.get(f"/creature/{sample.name}_bad")
    assert response.status_code == 404
    assert json.loads(response.text) == {"detail": f"Creature {sample.name}_bad not found"}


def test_get_all(test_client):
    response = test_client.get(f"/creature/")
    assert response.status_code == 200
    assert type(json.loads(response.text)) is list


def test_modify(test_client, sample, sample_dict_):
    response = test_client.patch(f"/creature/?name={sample.name}", json=sample_dict_)
    assert response.status_code == 200
    assert json.loads(response.text)['name'] == sample.name + '_'


def test_modify_back(test_client, sample, sample_dict):
    response = test_client.patch(f"/creature/?name={sample.name}_", json=sample_dict)
    assert response.status_code == 200
    assert json.loads(response.text) == sample.model_dump()


def test_modify_bad(test_client, sample, sample_dict_bad):
    response = test_client.patch(f"/creature/?name={sample.name}", json=sample_dict_bad)
    assert response.status_code == 400
    assert json.loads(response.text)['detail'][0]['msg'] == f"String should have at most 2 characters"


def test_modify_duplicate(test_client, sample, sample_dict_duplicate):
    response = test_client.patch(f"/creature/?name={sample.name}", json=sample_dict_duplicate)
    assert response.status_code == 400
    assert json.loads(response.text)['detail'] == f"Creature {sample_dict_duplicate['name']} already exists"


def test_modify_not_full(test_client, sample, sample_dict_not_full):
    response = test_client.patch(f"/creature/?name={sample.name}", json=sample_dict_not_full)
    assert response.status_code == 200
    assert json.loads(response.text)['name'] == sample.name
    assert json.loads(response.text)['country'] == sample.country
    assert json.loads(response.text)['area'] == sample.area
    assert json.loads(response.text)['aka'] == sample.aka + '_'


def test_modify_not_full_bad(test_client, sample, sample_dict_not_full_bad):
    response = test_client.patch(f"/creature/?name={sample.name}", json=sample_dict_not_full_bad)
    assert response.status_code == 400
    assert json.loads(response.text)['detail'][0]['msg'] == f"String should have at most 2 characters"


def test_modify_extended(test_client, sample, sample_dict_extended):
    response = test_client.patch(f"/creature/?name={sample.name}", json=sample_dict_extended)
    assert response.status_code == 200
    assert json.loads(response.text) == sample.model_dump()


def test_put_back(test_client, sample):
    response = test_client.put(f"/creature/", json=sample.model_dump())
    assert response.status_code == 200
    assert json.loads(response.text) == sample.model_dump()


def test_delete_creature_success(test_client, sample):
    response = test_client.delete(f"/creature/{sample.name}")
    assert response.status_code == 204


def test_delete_creature2_success(test_client, sample2):
    response = test_client.delete(f"/creature/{sample2.name}")
    assert response.status_code == 204


def test_delete_creature_failure(test_client, sample):
    response = test_client.delete(f"/creature/{sample.name}")
    assert response.status_code == 404


def test_put_missing(test_client, sample):
    response = test_client.put(f"/creature/", json=sample.model_dump())
    assert response.status_code == 404
    assert json.loads(response.text) == {"detail": f"Creature {sample.name} not found"}
