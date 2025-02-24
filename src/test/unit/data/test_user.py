from src.utils.errors import Duplicate, Missing, Validation
from src.model.user import User
from src.data import user as data

from src.test.fixtures.user import (
    sample, sample2, sample_dict, sample_dict_, sample_dict_extended, sample_dict_duplicate,
    sample_dict_bad, sample_dict_not_full, sample_dict_not_full_bad
)


def test_data_user_create(sample):
    try:
        resp = data.create(sample)
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample


def test_data_user_create2(sample2):
    try:
        resp = data.create(sample2)
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample2


def test_data_user_create_duplicate(sample):
    try:
        resp = data.create(sample)
    except Duplicate as exc:
        resp = exc.msg
    assert resp == f"User {sample.name} already exists"


def test_data_user_get_one(sample):
    try:
        resp = data.get_one(sample.name)
    except Missing as exc:
        resp = exc.msg
    assert resp == sample


def test_data_user_get_one_missing(sample):
    try:
        resp = data.get_one(sample.name + '_test_preffix')
    except Missing as exc:
        resp = exc.msg
    assert resp == f"User {sample.name + '_test_preffix'} not found"


def test_data_user_get_all(sample):
    resp = data.get_all()
    assert resp is not None
    assert type(resp) is list


def test_data_user_modify(sample, sample_dict_):
    try:
        resp = data.modify(sample.name, sample_dict_)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert type(resp) is User
    assert resp.name == sample.name + '_'


def test_data_user_modify_back(sample, sample_dict):
    try:
        resp = data.modify(sample.name + '_', sample_dict)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample


def test_data_user_modify_bad(sample, sample_dict_bad):
    try:
        resp = data.modify(sample.name, sample_dict_bad)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp[0]['type'] == 'string_too_short'


def test_data_user_modify_not_full(sample, sample_dict_not_full):
    try:
        resp = data.modify(sample.name, sample_dict_not_full)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp.name == sample.name


def test_data_user_modify_not_full_bad(sample, sample_dict_not_full_bad):
    try:
        resp = data.modify(sample.name, sample_dict_not_full_bad)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp[0]['type'] == 'string_too_short'


def test_data_user_modify_extended(sample, sample_dict_extended):
    try:
        resp = data.modify(sample.name, sample_dict_extended)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample


def test_data_user_modify_duplicate(sample, sample_dict_duplicate):
    try:
        resp = data.modify(sample.name, sample_dict_duplicate)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp == f"User {sample_dict_duplicate['name']} already exists"


def test_data_user_put_back(sample):
    try:
        resp = data.replace(sample)
    except Missing as exc:
        resp = exc.msg
    assert resp == sample


def test_data_user_delete(sample):
    try:
        resp = data.delete(sample.name)
    except Missing as exc:
        resp = None
    assert resp is True


def test_data_user_delete2(sample2):
    try:
        resp = data.delete(sample2.name)
    except Missing as exc:
        resp = None
    assert resp is True


def test_data_user_delete_duplicate(sample):
    try:
        resp = data.delete(sample.name)
    except Missing as exc:
        resp = exc.msg
    assert resp == f"User {sample.name} not found"


def test_data_user_put_missing(sample):
    try:
        resp = data.replace(sample)
    except Missing as exc:
        resp = exc.msg
    assert resp == f"User {sample.name} not found"
