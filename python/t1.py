#!/usr/bin/env python3

class A:
    def __init__(self):
        self.data = dict(a="a", b="b", c="c")
    def get(self):
        return self.data

class B:
    def __init__(self):
        self.data = dict(a="a", b="b", c="c")
    def get(self):
        return self.data

class C:
    def __init__(self):
        self.a = A()
        self.b = B()

    def get(self):
        if self.a.get().get("a") == "a":
            return True
        else:
            return False
