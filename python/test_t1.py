#!/usr/bin/env python3
# import pytest
from unittest.mock import patch
from t1 import C
# from t1 import A, B, C

def test1():
    c = C()
    assert c.get()

@patch("t1.A.get")
def test2(aget):
    aget.get.return_value = dict(a="b", b="c", c="a")
    c = C()
    assert not c.get()
