from src.utils.errors import Missing, Duplicate, Validation
from src.mock.creature import _creatures as mock_creatures
from src.model.creature import Creature
from src.test.fixtures.creature import (
    sample, sample2, sample_dict, sample_dict_, sample_dict_extended, sample_dict_duplicate,
    sample_dict_bad, sample_dict_not_full, sample_dict_not_full_bad
)
from src.service import creature as code


def test_get_all_creatures_mocked(mocker):
    mock = mocker.patch.object(code, 'get_all', return_value=mock_creatures)
    result = code.get_all()
    assert mock.called
    assert result == mock_creatures


def test_get_all_creatures():
    result = code.get_all()
    assert type(result) is list


def test_get_one_creature_success_mocked(mocker):
    mock_creature = mock_creatures[0]
    mock = mocker.patch.object(code, 'get_one', return_value=mock_creature)
    result = code.get_one(mock_creature.name)
    assert mock.called
    assert result == mock_creature


def test_get_one_creature_missing_mocked(mocker):
    mock_creature = mock_creatures[0]
    bad_name = mock_creature.name + '_bad'
    mock = mocker.patch.object(code, 'get_one', side_effect=Missing(f"Creature {bad_name} not found"))
    try:
        result = code.get_one(bad_name)
    except Missing as exc:
        result = exc.msg
    assert mock
    assert result == f"Creature {bad_name} not found"


def test_service_creature_create(sample):
    try:
        resp = code.create(sample)
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample


def test_service_creature_create2(sample2):
    try:
        resp = code.create(sample2)
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample2


def test_service_creature_create_duplicate(sample):
    try:
        resp = code.create(sample)
    except Duplicate as exc:
        resp = exc.msg
    assert resp == f"Creature {sample.name} already exists"


def test_service_creature_get_one(sample):
    try:
        resp = code.get_one(sample.name)
    except Missing as exc:
        resp = exc.msg
    assert resp == sample


def test_service_creature_get_one_missing(sample):
    try:
        resp = code.get_one(sample.name + '_test_preffix')
    except Missing as exc:
        resp = exc.msg
    assert resp == f"Creature {sample.name + '_test_preffix'} not found"


def test_service_creature_get_all(sample):
    resp = code.get_all()
    assert resp is not None
    assert type(resp) is list


def test_service_creature_modify(sample, sample_dict_):
    try:
        resp = code.modify(sample.name, sample_dict_)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert type(resp) is Creature
    assert resp.name == sample.name + '_'


def test_service_creature_modify_back(sample, sample_dict):
    try:
        resp = code.modify(sample.name + '_', sample_dict)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample


def test_service_creature_modify_bad(sample, sample_dict_bad):
    try:
        resp = code.modify(sample.name, sample_dict_bad)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp[0]['type'] == 'string_too_long'


def test_service_creature_modify_not_full(sample, sample_dict_not_full):
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
    assert resp.area == sample.area
    assert resp.aka == sample.aka + '_'


def test_service_creature_modify_not_full_bad(sample, sample_dict_not_full_bad):
    try:
        resp = code.modify(sample.name, sample_dict_not_full_bad)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp[0]['type'] == 'string_too_long'


def test_service_creature_modify_extended(sample, sample_dict_extended):
    try:
        resp = code.modify(sample.name, sample_dict_extended)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp == sample


def test_service_creature_modify_duplicate(sample, sample_dict_duplicate):
    try:
        resp = code.modify(sample.name, sample_dict_duplicate)
    except Missing as exc:
        resp = exc.msg
    except Validation as exc:
        resp = exc.msg
    except Duplicate as exc:
        resp = exc.msg
    assert resp == f"Creature {sample_dict_duplicate['name']} already exists"


def test_service_creature_put_back(sample):
    try:
        resp = code.replace(sample)
    except Missing as exc:
        resp = exc.msg
    assert resp == sample


def test_service_creature_delete(sample):
    try:
        resp = code.delete(sample.name)
    except Missing as exc:
        resp = None
    assert resp is True


def test_service_creature_delete2(sample2):
    try:
        resp = code.delete(sample2.name)
    except Missing as exc:
        resp = None
    assert resp is True


def test_service_creature_delete_duplicate(sample):
    try:
        resp = code.delete(sample.name)
    except Missing as exc:
        resp = exc.msg
    assert resp == f"Creature {sample.name} not found"


def test_service_creature_put_missing(sample):
    try:
        resp = code.replace(sample)
    except Missing as exc:
        resp = exc.msg
    assert resp == f"Creature {sample.name} not found"
