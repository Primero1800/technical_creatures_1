from src.errors import Missing, Duplicate, Validation
from src.mock.user import _users as mock_users
from src.model.user import User
from src.test.fixtures.user import (
    sample, sample2, sample_dict, sample_dict_, sample_dict_extended, sample_dict_duplicate,
    sample_dict_bad, sample_dict_not_full, sample_dict_not_full_bad
)
from src.service import user as code


def test_get_all_users_mocked(mocker):
    mock = mocker.patch.object(code, 'get_all', return_value=mock_users)
    result = code.get_all()
    assert mock.called
    assert result == mock_users


def test_get_all_users():
    result = code.get_all()
    assert type(result) is list


def test_get_one_user_success_mocked(mocker):
    mock_user = mock_users[0]
    mock = mocker.patch.object(code, 'get_one', return_value=mock_user)
    result = code.get_one(mock_user.name)
    assert mock.called
    assert result == mock_user


def test_get_one_user_missing_mocked(mocker):
    mock_user = mock_users[0]
    bad_name = mock_user.name + '_bad'
    mock = mocker.patch.object(code, 'get_one', side_effect=Missing(f"User {bad_name} not found"))
    try:
        result = code.get_one(bad_name)
    except Missing as exc:
        result = exc.msg
    assert mock
    assert result == f"User {bad_name} not found"


def test_service_user_create(sample):
    try:
        resp = code.create(sample)
    except Duplicate as exc:
        resp = exc.msg
    assert resp.name == sample.name


def test_service_user_create2(sample2):
    try:
        resp = code.create(sample2)
    except Duplicate as exc:
        resp = exc.msg
    assert resp.name == sample2.name


def test_service_user_create_duplicate(sample):
    try:
        resp = code.create(sample)
    except Duplicate as exc:
        resp = exc.msg
    assert resp == f"User {sample.name} already exists"


def test_service_lookup_user(sample):
    try:
        user = code.lookup_user(sample.name)
    except Missing as exc:
        user = exc.msg
    assert user.name == sample.name


def test_service_lookup_user_bad(sample):
    try:
        user = code.lookup_user(sample.name + '_bad')
    except Missing as exc:
        user = exc.msg
    assert user == f"User {sample.name}_bad not found"


def test_service_auth_user(sample):
    try:
        result = code.auth_user(sample.name, sample.hash)
    except Missing as exc:
        result = exc.msg
    assert result .name == sample.name


def test_service_auth_user_bad(sample):
    try:
        result = code.auth_user(sample.name + '_bad', sample.hash)
    except Missing as exc:
        result = exc.msg
    assert result == f"User {sample.name}_bad not found"


def test_service_verify_user(sample):
    try:
        result = code.verify_password(sample.hash, code.get_one(sample.name).hash)
    except Missing as exc:
        result = exc.msg
    assert result is True


def test_service_verify_user_bad_hash(sample):
    try:
        result = code.verify_password(sample.hash + '_bad', code.get_one(sample.name).hash)
    except Missing as exc:
        result = exc.msg
    assert result is False


def test_service_verify_user_missing(sample):
    try:
        result = code.verify_password(sample.hash, code.get_one(sample.name + '_bad').hash)
    except Missing as exc:
        result = exc.msg
    assert result == f"User {sample.name}_bad not found"


def test_service_user_get_one(sample):
    try:
        resp = code.get_one(sample.name)
    except Missing as exc:
        resp = exc.msg
    assert resp.name == sample.name


def test_service_user_get_one_missing(sample):
    try:
        resp = code.get_one(sample.name + '_test_preffix')
    except Missing as exc:
        resp = exc.msg
    assert resp == f"User {sample.name + '_test_preffix'} not found"


def test_service_user_get_all(sample):
    resp = code.get_all()
    assert resp is not None
    assert type(resp) is list


def test_service_user_modify(sample, sample_dict_):
    try:
        resp = code.modify(sample.name, sample_dict_)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert type(resp) is User
    assert resp.name == sample.name + '_'


def test_service_user_modify_back(sample, sample_dict):
    try:
        resp = code.modify(sample.name + '_', sample_dict)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample


def test_service_user_modify_bad(sample, sample_dict_bad):
    try:
        resp = code.modify(sample.name, sample_dict_bad)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp[0]['type'] == 'string_too_short'


def test_service_user_modify_not_full(sample, sample_dict_not_full):
    try:
        resp = code.modify(sample.name, sample_dict_not_full)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp.name == sample.name


def test_service_user_modify_not_full_bad(sample, sample_dict_not_full_bad):
    try:
        resp = code.modify(sample.name, sample_dict_not_full_bad)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp[0]['type'] == 'string_too_short'


def test_service_user_modify_extended(sample, sample_dict_extended):
    try:
        resp = code.modify(sample.name, sample_dict_extended)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample


def test_service_user_modify_duplicate(sample, sample_dict_duplicate):
    try:
        resp = code.modify(sample.name, sample_dict_duplicate)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp == f"User {sample_dict_duplicate['name']} already exists"


def test_service_user_put_back(sample):
    try:
        resp = code.replace(sample)
    except Missing as exc:
        resp = exc.msg
    assert resp == sample


def test_service_user_delete(sample):
    try:
        resp = code.delete(sample.name)
    except Missing as exc:
        resp = None
    assert resp is True


def test_service_user_delete2(sample2):
    try:
        resp = code.delete(sample2.name)
    except Missing as exc:
        resp = None
    assert resp is True


def test_service_user_delete_duplicate(sample):
    try:
        resp = code.delete(sample.name)
    except Missing as exc:
        resp = exc.msg
    assert resp == f"User {sample.name} not found"


def test_service_user_put_missing(sample):
    try:
        resp = code.replace(sample)
    except Missing as exc:
        resp = exc.msg
    assert resp == f"User {sample.name} not found"
