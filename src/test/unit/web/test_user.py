import json

from src.utils.errors import Missing
from src.mock.user import _users as mock_users
from src.test.fixtures.user import (
    sample2, sample_dict, sample_dict_, sample_dict_extended, sample_dict_duplicate,
    sample_dict_bad, sample_dict_not_full, sample_dict_not_full_bad, oauth2data,
)
from src.test.fixtures.glob import (
    test_client, test_app, sample
)
import src.service.user as service


TEST_TOKENS = []
TEST_REFRESH_TOKENS = []


def test_clear_test_tokens():
    TEST_TOKENS.clear()
    TEST_REFRESH_TOKENS.clear()
    assert TEST_TOKENS == []
    assert TEST_REFRESH_TOKENS == []


def test_get_all_users_mocked(test_client, mocker):
    mock = mocker.patch.object(service, 'get_all', return_value=mock_users)
    response = test_client.get("/user")
    assert mock.called
    assert response.status_code == 200
    assert response.json() == [item.model_dump() for item in mock_users]


def test_get_all_users(test_client):
    response = test_client.get("/user/")
    assert response.status_code == 200
    assert type(json.loads(response.text)) is list


def test_get_one_user_success_mocked(test_client, mocker):
    mock_user = mock_users[0]
    mock = mocker.patch.object(service, 'get_one', return_value=mock_user)
    assertion_result = mock_user.model_dump()

    response = test_client.get(f"/user/{mock_user.name}/")
    assert mock.called
    assert response.status_code == 200
    assert response.json() == mock_user.model_dump()


def test_get_one_user_missing_mocked(test_client, mocker):
    mock_user = mock_users[0]
    bad_name = mock_user.name + '_bad'
    mock = mocker.patch.object(service, 'get_one', side_effect=Missing(f"User {bad_name} not found"))

    response = test_client.get(f"/user/{bad_name}/")
    assert mock.called
    assert response.status_code == 404
    assert response.json() == {"detail": f"User {bad_name} not found"}


def test_create_user_success(test_client, sample):
    response = test_client.post("/user/", json=sample.model_dump())
    assert response.status_code == 201
    assert json.loads(response.text)['name'] == sample.model_dump()['name']


def test_create_user_failure(test_client, sample):
    response = test_client.post("/user/", json=sample.model_dump())
    assert response.status_code == 400
    assert json.loads(response.text) == {'detail': f"User {sample.name} already exists"}


def test_create_user2_success(test_client, sample2):
    response = test_client.post("/user/", json=sample2.model_dump())
    assert response.status_code == 201
    assert json.loads(response.text)['name'] == sample2.model_dump()['name']


def test_create_access_token(test_client, sample, oauth2data):
    response = test_client.post(
        "/user/token",
        data=oauth2data
    )
    assert response.status_code == 200
    response_text = json.loads(response.text)
    assert response_text['token_type'] == 'bearer'
    TEST_TOKENS.append("Bearer " + response_text['access_token'])
    TEST_REFRESH_TOKENS.append("Bearer " + response_text['refresh_token'])


def test_create_access_token_bad(test_client, sample, oauth2data):
    oauth2data['password'] = '********'
    response = test_client.post(
        "/user/token",
        data=oauth2data
    )
    assert response.status_code == 401


def test_create_access_token_nouser(test_client, sample, oauth2data):
    oauth2data['username'] += '_bad'
    response = test_client.post(
        "/user/token",
        data=oauth2data
    )
    assert response.status_code == 404


def test_create_access_token_random():
    TEST_TOKENS.append('Bearer ' + 'dddddddddddddd'*3)
    assert len(TEST_TOKENS) == 2


def test_get_access_token(test_client, sample):
    response = test_client.get(
        "/user/token",
        headers={
            "Authorization": TEST_TOKENS[0],
        }
    )
    assert response.status_code == 200
    response_text = json.loads(response.text)
    assert response_text['data']['user']['name'] == sample.name


def test_get_access_token_bad(test_client):
    response = test_client.get(
        "/user/token",
        headers={
            "Authorization": TEST_TOKENS[1],
        }
    )
    assert response.status_code == 401
    assert json.loads(response.text) == {"detail": f"Not enough segments"}


def test_refresh_access_token(test_client):
    response = test_client.post(
        "/user/refresh",
        headers={
            "Authorization": TEST_REFRESH_TOKENS[0],
        }
    )
    assert response.status_code == 200
    assert 'access_token' in json.loads(response.text)


def test_refresh_access_token_with_access(test_client):
    response = test_client.post(
        "/user/refresh",
        headers={
            "Authorization": TEST_TOKENS[0],
        }
    )
    assert response.status_code == 401
    assert json.loads(response.text)['detail'].startswith("Invalid token type")


def test_refresh_access_token_bad(test_client):
    response = test_client.post(
        "/user/refresh",
        headers={
            "Authorization": TEST_TOKENS[1],
        }
    )
    assert response.status_code == 401
    assert json.loads(response.text)['detail'].startswith("Not enough segments")


def test_get_user_info_from_any_token(test_client, sample):
    response = test_client.get(
        "/user/user_by_token",
        headers={
            "Authorization": TEST_TOKENS[0],
        }
    )
    assert response.status_code == 200
    assert json.loads(response.text)['type'] == 'access'
    assert json.loads(response.text)['user']['name'] == sample.name


def test_get_user_info_from_any_token_refresh(test_client, sample):
    response = test_client.get(
        "/user/user_by_token",
        headers={
            "Authorization": TEST_REFRESH_TOKENS[0],
        }
    )
    assert response.status_code == 200
    assert json.loads(response.text)['type'] == 'refresh'
    assert json.loads(response.text)['user']['name'] == sample.name


def test_get_user_info_from_any_token_bad(test_client, sample):
    response = test_client.get(
        "/user/user_by_token",
        headers={
            "Authorization": TEST_TOKENS[1],
        }
    )
    assert response.status_code == 400
    assert json.loads(response.text)['detail'] == 'Not enough segments'


def test_get_one_success(test_client, sample):
    response = test_client.get(f"/user/{sample.name}")
    assert response.status_code == 200
    assert json.loads(response.text)['name'] == sample.model_dump()['name']


def test_get_one_failure(test_client, sample):
    response = test_client.get(f"/user/{sample.name}_bad")
    assert response.status_code == 404
    assert json.loads(response.text) == {"detail": f"User {sample.name}_bad not found"}


def test_get_all(test_client):
    response = test_client.get(f"/user/")
    assert response.status_code == 200
    assert type(json.loads(response.text)) is list


def test_modify(test_client, sample, sample_dict_):
    response = test_client.patch(f"/user/?name={sample.name}", json=sample_dict_)
    assert response.status_code == 200
    assert json.loads(response.text)['name'] == sample.name + '_'


def test_modify_back(test_client, sample, sample_dict):
    response = test_client.patch(f"/user/?name={sample.name}_", json=sample_dict)
    assert response.status_code == 200
    assert json.loads(response.text) == sample.model_dump()


def test_modify_bad(test_client, sample, sample_dict_bad):
    response = test_client.patch(f"/user/?name={sample.name}", json=sample_dict_bad)
    assert response.status_code == 400
    assert json.loads(response.text)['detail'][0]['msg'] == f"String should have at least 2 characters"


def test_modify_duplicate(test_client, sample, sample_dict_duplicate):
    response = test_client.patch(f"/user/?name={sample.name}", json=sample_dict_duplicate)
    assert response.status_code == 400
    assert json.loads(response.text)['detail'] == f"User {sample_dict_duplicate['name']} already exists"


def test_modify_not_full(test_client, sample, sample_dict_not_full):
    response = test_client.patch(f"/user/?name={sample.name}", json=sample_dict_not_full)
    assert response.status_code == 200
    assert json.loads(response.text)['name'] == sample.name


def test_modify_not_full_bad(test_client, sample, sample_dict_not_full_bad):
    response = test_client.patch(f"/user/?name={sample.name}", json=sample_dict_not_full_bad)
    assert response.status_code == 400
    assert json.loads(response.text)['detail'][0]['msg'] == f"String should have at least 2 characters"


def test_modify_extended(test_client, sample, sample_dict_extended):
    response = test_client.patch(f"/user/?name={sample.name}", json=sample_dict_extended)
    assert response.status_code == 200
    assert json.loads(response.text) == sample.model_dump()


def test_put_back(test_client, sample):
    response = test_client.put(f"/user/", json=sample.model_dump())
    assert response.status_code == 200
    assert json.loads(response.text) == sample.model_dump()


def test_delete_user_success(test_client, sample):
    response = test_client.delete(f"/user/{sample.name}")
    assert response.status_code == 204


def test_delete_user2_success(test_client, sample2):
    response = test_client.delete(f"/user/{sample2.name}")
    assert response.status_code == 204


def test_delete_user_failure(test_client, sample):
    response = test_client.delete(f"/user/{sample.name}")
    assert response.status_code == 404


def test_put_missing(test_client, sample):
    response = test_client.put(f"/user/", json=sample.model_dump())
    assert response.status_code == 404
    assert json.loads(response.text) == {"detail": f"User {sample.name} not found"}



