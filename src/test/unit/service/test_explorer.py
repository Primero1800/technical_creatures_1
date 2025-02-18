import json

from src.errors import Missing, Duplicate, Validation
from src.mock.explorer import _explorers as mock_explorers
from src.model.explorer import Explorer
from src.test.fixtures.explorer import (
    sample, sample2, sample_dict, sample_dict_, sample_dict_extended, sample_dict_duplicate,
    sample_dict_bad, sample_dict_not_full, sample_dict_not_full_bad
)
from src.service import explorer as code


def test_get_all_explorers_mocked(mocker):
    mock = mocker.patch.object(code, 'get_all', return_value=mock_explorers)
    result = code.get_all()
    assert mock.called
    assert result == mock_explorers


def test_get_all_explorers():
    result = code.get_all()
    assert type(result) is list


def test_get_one_explorer_success_mocked(mocker):
    mock_explorer = mock_explorers[0]
    mock = mocker.patch.object(code, 'get_one', return_value=mock_explorer)
    result = code.get_one(mock_explorer.name)
    assert mock.called
    assert result == mock_explorer


def test_get_one_explorer_missing_mocked(mocker):
    mock_explorer = mock_explorers[0]
    bad_name = mock_explorer.name + '_bad'
    mock = mocker.patch.object(code, 'get_one', side_effect=Missing(f"Explorer {bad_name} not found"))
    try:
        result = code.get_one(bad_name)
    except Missing as exc:
        result = exc.msg
    assert mock
    assert result == f"Explorer {bad_name} not found"


def test_service_explorer_create(sample):
    try:
        resp = code.create(sample)
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample


def test_service_explorer_create2(sample2):
    try:
        resp = code.create(sample2)
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample2


def test_service_explorer_create_duplicate(sample):
    try:
        resp = code.create(sample)
    except Duplicate as exc:
        resp = exc.msg
    assert resp == f"Explorer {sample.name} already exists"


def test_service_explorer_get_one(sample):
    try:
        resp = code.get_one(sample.name)
    except Missing as exc:
        resp = exc.msg
    assert resp == sample


def test_service_explorer_get_one_missing(sample):
    try:
        resp = code.get_one(sample.name + '_test_preffix')
    except Missing as exc:
        resp = exc.msg
    assert resp == f"Explorer {sample.name + '_test_preffix'} not found"


def test_service_explorer_get_all(sample):
    resp = code.get_all()
    assert resp is not None
    assert type(resp) is list


def test_service_explorer_modify(sample, sample_dict_):
    try:
        resp = code.modify(sample.name, sample_dict_)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert type(resp) is Explorer
    assert resp.name == sample.name + '_'


def test_service_explorer_modify_back(sample, sample_dict):
    try:
        resp = code.modify(sample.name + '_', sample_dict)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample


def test_service_explorer_modify_bad(sample, sample_dict_bad):
    try:
        resp = code.modify(sample.name, sample_dict_bad)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp[0]['type'] == 'string_too_long'


def test_service_explorer_modify_not_full(sample, sample_dict_not_full):
    try:
        resp = code.modify(sample.name, sample_dict_not_full)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp.name == sample.name
    assert resp.country == sample.country
    assert resp.description == sample.description + '_'


def test_service_explorer_modify_not_full_bad(sample, sample_dict_not_full_bad):
    try:
        resp = code.modify(sample.name, sample_dict_not_full_bad)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp[0]['type'] == 'string_too_long'


def test_service_explorer_modify_extended(sample, sample_dict_extended):
    try:
        resp = code.modify(sample.name, sample_dict_extended)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample


def test_service_explorer_modify_duplicate(sample, sample_dict_duplicate):
    try:
        resp = code.modify(sample.name, sample_dict_duplicate)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp == f"Explorer {sample_dict_duplicate['name']} already exists"


def test_service_explorer_put_back(sample):
    try:
        resp = code.replace(sample)
    except Missing as exc:
        resp = exc.msg
    assert resp == sample


def test_service_explorer_delete(sample):
    try:
        resp = code.delete(sample.name)
    except Missing as exc:
        resp = None
    assert resp is True


def test_service_explorer_delete2(sample2):
    try:
        resp = code.delete(sample2.name)
    except Missing as exc:
        resp = None
    assert resp is True


def test_service_explorer_delete_duplicate(sample):
    try:
        resp = code.delete(sample.name)
    except Missing as exc:
        resp = exc.msg
    assert resp == f"Explorer {sample.name} not found"


def test_service_explorer_put_missing(sample):
    try:
        resp = code.replace(sample)
    except Missing as exc:
        resp = exc.msg
    assert resp == f"Explorer {sample.name} not found"
