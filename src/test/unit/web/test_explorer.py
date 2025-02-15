import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.errors import Missing
from src.mock.explorer import _explorers as mock_explorers
from src.test.fixtures.explorer import (
    sample, sample2, sample_dict, sample_dict_, sample_dict_extended, sample_dict_duplicate,
    sample_dict_bad, sample_dict_not_full, sample_dict_not_full_bad
)
from src.web import explorer
import src.service.explorer as service


@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(explorer.router)
    return app


@pytest.fixture
def test_client(test_app):
    return TestClient(test_app)


def test_get_all_explorers_mocked(test_client, mocker):
    mock = mocker.patch.object(service, 'get_all', return_value=mock_explorers)
    response = test_client.get("/explorer")
    assert mock.called
    assert response.status_code == 200
    assert response.json() == [item.model_dump() for item in mock_explorers]


def test_get_all_explorers(test_client):
    response = test_client.get("/explorer/")
    assert response.status_code == 200
    assert type(json.loads(response.text)) is list


def test_get_one_explorer_success_mocked(test_client, mocker):
    mock_explorer = mock_explorers[0]
    mock = mocker.patch.object(service, 'get_one', return_value=mock_explorer)

    response = test_client.get(f"/explorer/{mock_explorer.name}/")
    assert mock.called
    assert response.status_code == 200
    assert response.json() == mock_explorer.model_dump()


def test_get_one_explorer_missing_mocked(test_client, mocker):
    mock_explorer = mock_explorers[0]
    bad_name = mock_explorer.name + '_bad'
    mock = mocker.patch.object(service, 'get_one', side_effect=Missing(f"Explorer {bad_name} not found"))

    response = test_client.get(f"/explorer/{bad_name}/")
    assert mock.called
    assert response.status_code == 404
    assert response.json() == {"detail": f"Explorer {bad_name} not found"}


def test_create_explorer_success(test_client, sample):
    response = test_client.post("/explorer/", json=sample.model_dump())
    assert response.status_code == 201
    assert json.loads(response.text) == sample.model_dump()


def test_create_explorer_failure(test_client, sample):
    response = test_client.post("/explorer/", json=sample.model_dump())
    assert response.status_code == 400
    assert json.loads(response.text) == {'detail': f"Explorer {sample.name} already exists"}


def test_create_explorer2_success(test_client, sample2):
    response = test_client.post("/explorer/", json=sample2.model_dump())
    assert response.status_code == 201
    assert json.loads(response.text) == sample2.model_dump()


def test_get_one_success(test_client, sample):
    response = test_client.get(f"/explorer/{sample.name}")
    assert response.status_code == 200
    assert json.loads(response.text) == sample.model_dump()


def test_get_one_failure(test_client, sample):
    response = test_client.get(f"/explorer/{sample.name}_bad")
    assert response.status_code == 404
    assert json.loads(response.text) == {"detail": f"Explorer {sample.name}_bad not found"}


def test_get_all(test_client):
    response = test_client.get(f"/explorer/")
    assert response.status_code == 200
    assert type(json.loads(response.text)) is list


def test_modify(test_client, sample, sample_dict_):
    response = test_client.patch(f"/explorer/?name={sample.name}", json=sample_dict_)
    assert response.status_code == 200
    assert json.loads(response.text)['name'] == sample.name + '_'


def test_modify_back(test_client, sample, sample_dict):
    response = test_client.patch(f"/explorer/?name={sample.name}_", json=sample_dict)
    assert response.status_code == 200
    assert json.loads(response.text) == sample.model_dump()


def test_modify_bad(test_client, sample, sample_dict_bad):
    response = test_client.patch(f"/explorer/?name={sample.name}", json=sample_dict_bad)
    assert response.status_code == 400
    assert json.loads(response.text)['detail'][0]['msg'] == f"String should have at most 2 characters"


def test_modify_duplicate(test_client, sample, sample_dict_duplicate):
    response = test_client.patch(f"/explorer/?name={sample.name}", json=sample_dict_duplicate)
    assert response.status_code == 400
    assert json.loads(response.text)['detail'] == f"Explorer {sample_dict_duplicate['name']} already exists"


def test_modify_not_full(test_client, sample, sample_dict_not_full):
    response = test_client.patch(f"/explorer/?name={sample.name}", json=sample_dict_not_full)
    assert response.status_code == 200
    assert json.loads(response.text)['name'] == sample.name
    assert json.loads(response.text)['country'] == sample.country
    assert json.loads(response.text)['description'] == sample.description + '_'


def test_modify_not_full_bad(test_client, sample, sample_dict_not_full_bad):
    response = test_client.patch(f"/explorer/?name={sample.name}", json=sample_dict_not_full_bad)
    assert response.status_code == 400
    assert json.loads(response.text)['detail'][0]['msg'] == f"String should have at most 2 characters"


def test_modify_extended(test_client, sample, sample_dict_extended):
    response = test_client.patch(f"/explorer/?name={sample.name}", json=sample_dict_extended)
    assert response.status_code == 200
    assert json.loads(response.text) == sample.model_dump()


def test_put_back(test_client, sample):
    response = test_client.put(f"/explorer/", json=sample.model_dump())
    assert response.status_code == 200
    assert json.loads(response.text) == sample.model_dump()


def test_delete_explorer_success(test_client, sample):
    response = test_client.delete(f"/explorer/{sample.name}")
    assert response.status_code == 204


def test_delete_explorer2_success(test_client, sample2):
    response = test_client.delete(f"/explorer/{sample2.name}")
    assert response.status_code == 204


def test_delete_explorer_failure(test_client, sample):
    response = test_client.delete(f"/explorer/{sample.name}")
    assert response.status_code == 404


def test_put_missing(test_client, sample):
    response = test_client.put(f"/explorer/", json=sample.model_dump())
    assert response.status_code == 404
    assert json.loads(response.text) == {"detail": f"Explorer {sample.name} not found"}
