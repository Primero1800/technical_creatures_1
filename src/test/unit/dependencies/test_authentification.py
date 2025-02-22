import asyncio
import json

import pytest
from fastapi import HTTPException
from starlette.requests import Request

from src.errors import Missing
from src.service import user as service_user
from src.mock.user import _sample_users as mock_users
from src.dependencies import authentification as auth_deps
from src.test.fixtures.glob import (
    test_client, test_app, sample, custom_request_class,
)


USER1 = mock_users[0]
TEST_TOKENS = []


def test_clear_test_tokens():
    TEST_TOKENS.clear()


def test_create_user_success(test_client, sample):
    response = test_client.post("/user/", json=sample.model_dump())
    assert response.status_code == 201
    assert json.loads(response.text)['name'] == sample.model_dump()['name']


@pytest.mark.asyncio
async def test_generate_token_for_user_mocked(mocker):
    mock = mocker.patch.object(service_user, 'auth_user', return_value=USER1)
    result = await auth_deps.generate_token_for_user(USER1.name, USER1.hash)
    assert isinstance(result, dict)
    assert result['token_type'] == 'bearer'
    assert 'access_token' in result.keys()
    TEST_TOKENS.append(result['access_token'])


@pytest.mark.asyncio
async def test_generate_token_for_user_bad_username_mocked(mocker):
    mock = mocker.patch.object(service_user, 'auth_user', side_effect=Missing(f"User {USER1.name} not found"))
    try:
        result = await auth_deps.generate_token_for_user(USER1.name, USER1.hash)
    except HTTPException as exc:
        result = exc
    assert result.status_code == 404
    assert result.detail == f"User {USER1.name} not found"


@pytest.mark.asyncio
async def test_generate_token_for_user_bad_password_mocked(mocker):
    def side_effect_function(*args, **kwargs):
        return None

    mock = mocker.patch.object(service_user, 'auth_user', side_effect=side_effect_function)
    try:
        assert mock.mocked
        result = await auth_deps.generate_token_for_user(USER1.name, USER1.hash)
    except HTTPException as exc:
        result = exc
    assert result.status_code == 401
    assert result.detail == "Incorrect username or password"


@pytest.mark.asyncio
async def test_generate_token_for_user(sample, test_client):
    result = await auth_deps.generate_token_for_user(USER1.name, USER1.hash)
    assert isinstance(result, dict)
    assert result['token_type'] == 'bearer'
    assert 'access_token' in result.keys()
    TEST_TOKENS.append(result['access_token'])


@pytest.mark.asyncio
async def test_generate_token_for_user_bad_name(sample, test_client):
    try:
        result = await auth_deps.generate_token_for_user(USER1.name + "_bad", USER1.hash)
    except HTTPException as exc:
        result = exc
    assert result.status_code == 404
    assert result.detail == f"User {sample.name}_bad not found"


@pytest.mark.asyncio
async def test_generate_token_for_user_bad_password(sample, test_client):
    try:
        result = await auth_deps.generate_token_for_user(USER1.name, USER1.hash + "_bad")
    except HTTPException as exc:
        result = exc
    assert result.status_code == 401
    assert result.detail == f"Incorrect username or password"


@pytest.mark.asyncio
async def test_get_token_from_request(sample, test_client, custom_request_class):
    request = custom_request_class()
    request.headers = {
        "Authorization": f"Bearer {TEST_TOKENS[1]}"
    }
    try:
        result = await auth_deps.get_token_from_request(request)
    except HTTPException as exc:
        result = exc
    assert isinstance(result, str)


@pytest.mark.asyncio
async def test_get_token_from_request_bad_token(sample, test_client, custom_request_class):
    request = custom_request_class()
    request.headers = {
        "Authorization": f"arer {TEST_TOKENS[0]}"
    }
    try:
        result = await auth_deps.get_token_from_request(request)
    except HTTPException as exc:
        result = exc
    assert result.status_code == 401
    assert result.detail == "Not authenticated"


@pytest.mark.asyncio
async def test_get_token_from_request_no_token(sample, test_client, custom_request_class):
    request = custom_request_class()
    request.headers = {}
    try:
        result = await auth_deps.get_token_from_request(request)
    except HTTPException as exc:
        result = exc
    assert result.status_code == 401
    assert result.detail == "Not authenticated"


@pytest.mark.asyncio
async def test_login_required(sample):
    try:
        result = await auth_deps.login_required(TEST_TOKENS[1])
    except Missing as exc:
        result = exc.msg
    except HTTPException as exc:
        result = exc
    assert result.name == sample.name


@pytest.mark.asyncio
async def test_login_required_bad(sample):
    try:
        result = await auth_deps.login_required('bad_token')
    except Missing as exc:
        result = exc.msg
    except HTTPException as exc:
        result = exc
    assert result.status_code == 401
    assert result.detail == 'Not authenticated'



def test_delete_user_success(test_client, sample):
    response = test_client.delete(f"/user/{sample.name}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_login_required_after_user_deleting(sample):
    try:
        result = await auth_deps.login_required(TEST_TOKENS[0])
    except Missing as exc:
        result = exc.msg
    except HTTPException as exc:
        result = exc
    assert result == f"User {sample.name} not found"
