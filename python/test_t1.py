#!/usr/bin/env python3
import pytest
from unittest.mock import patch
from t1 import C

class FakeA:
    def __init__(self, data):
        self.data = data


def test1():
    c = C()
    assert c.get()


@patch("t1.A.get")
def test2(aget):
    aget.get.return_value = dict(a="b", b="c", c="a")
    c = C()
    assert not c.get()


@patch("t1.A.get", return_value=dict(a="b", b="c", c="a"), autospec=True)
def test3(aget):
    c = C()
    assert not c.get()


@pytest.mark.parametrize(
    "output, expected",
    [
        (dict(a="a", b="c", c="a"), True),
        (dict(a="b", b="c", c="a"), False),
    ]
)
@patch("t1.A.get")
def test4(aget, output, expected):
    aget.return_value = output
    c = C()
    assert c.get() == expected
