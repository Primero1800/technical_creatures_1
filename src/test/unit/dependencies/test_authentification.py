import asyncio

from src.service import user as service_user
from src.mock.user import _sample_users as mock_users
from src.dependencies import authentification as auth_deps


# def test_get_all_users_mocked(mocker):
#     mock = mocker.patch.object(service_user, 'get_all', return_value=mock_users)
#     response = test_client.get("/user")
#     assert mock.called
#     assert response.status_code == 200
#     assert response.json() == [item.model_dump() for item in mock_users]

USER1 = mock_users[0]
TEST_TOKENS = []


def test_clear_test_tokens():
    TEST_TOKENS.clear()


def test_generate_token_for_user(mocker):
    mock = mocker.patch.object(service_user, 'auth_user', return_value=USER1)
    result = auth_deps.generate_token_for_user(USER1.name, USER1.hash)
    assert isinstance(result, dict)
    assert result['token_type'] == 'bearer'
    assert 'access_token' in result.keys()
    TEST_TOKENS.append(result['access_token'])



