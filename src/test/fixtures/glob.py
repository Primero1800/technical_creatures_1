import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from src.model.user import User
from src.web import user
from src.mock.user import _sample_users as sample_users


@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(user.router)
    return app


@pytest.fixture
def test_client(test_app):
    return TestClient(test_app)


@pytest.fixture
def sample() -> User:
    return sample_users[0]


@pytest.fixture
def custom_request_class():
    class CustomRequest:
        headers = {}
    return CustomRequest
