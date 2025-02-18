import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from src.errors import Duplicate, Missing
from src.service import creature as code
from src.mock.creature import _creatures as sample_creatures

sample = sample_creatures[0]


def test_get_all_users_mocked(test_client, mocker):
    mock = mocker.patch.object(service, 'get_all', return_value=mock_users)
    response = test_client.get("/user")
    assert mock.called
    assert response.status_code == 200
    assert response.json() == [item.model_dump() for item in mock_users]



def test_create():
    try:
        resp = code.create(sample)
    except Duplicate as exc:
        assert exc.msg == "Creature Yeti already exists"


def test_get_exists():
    try:
        resp = code.get_one("Yeti")
    except Missing as exc:
        resp = None
    assert resp == sample


def test_get_missing():
    try:
        resp = code.get_one("boxturtle")
    except Missing as exc:
        assert exc.msg == "Creature boxturtle not found"
