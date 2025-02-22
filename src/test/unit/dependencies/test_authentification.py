import asyncio
import json

import pytest
from fastapi import HTTPException

from src.errors import Missing
from src.service import user as service_user
from src.mock.user import _sample_users as mock_users
from src.dependencies import authentification as auth_deps
from src.test.fixtures.glob import (
    test_client, test_app, sample
)


USER1 = mock_users[0]
TEST_TOKENS = []


def test_clear_test_tokens():
    TEST_TOKENS.clear()


@pytest.mark.asyncio
async def test_generate_token_for_user(mocker):
    mock = mocker.patch.object(service_user, 'auth_user', return_value=USER1)
    result = await auth_deps.generate_token_for_user(USER1.name, USER1.hash)
    assert isinstance(result, dict)
    assert result['token_type'] == 'bearer'
    assert 'access_token' in result.keys()
    TEST_TOKENS.append(result['access_token'])


@pytest.mark.asyncio
async def test_generate_token_for_user_bad_username(mocker):
    mock = mocker.patch.object(service_user, 'auth_user', side_effect=Missing(f"User {USER1.name} not found"))
    try:
        result = await auth_deps.generate_token_for_user(USER1.name, USER1.hash)
    except HTTPException as exc:
        result = exc
    assert result.status_code == 404
    assert result.detail == f"User {USER1.name} not found"


@pytest.mark.asyncio
async def test_generate_token_for_user_bad_password(mocker):
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


def test_create_user_success(test_client, sample):
    response = test_client.post("/user/", json=sample.model_dump())
    assert response.status_code == 201
    assert json.loads(response.text)['name'] == sample.model_dump()['name']


# @pytest.mark.asyncio
# async def test_login_required():
#     result = await auth_deps.login_required(TEST_TOKENS[0])
#     print('RESULTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT', result)
#     assert isinstance(result, str)
#     assert result != ''





def test_delete_user_success(test_client, sample):
    response = test_client.delete(f"/user/{sample.name}")
    assert response.status_code == 204
