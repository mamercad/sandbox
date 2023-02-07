#!/usr/bin/env python3
from unittest.mock import patch
from t1 import C

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
