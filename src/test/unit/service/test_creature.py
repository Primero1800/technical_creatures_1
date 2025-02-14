from src.errors import Duplicate, Missing
from src.service import creature as code
from src.mock.creature import _creatures as sample_creatures

sample = sample_creatures[0]


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
