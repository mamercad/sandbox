#!/usr/bin/env python3


class A:
    def __init__(self: object) -> None:
        self.data = dict(a="a", b="b", c="c")

    def get(self: object) -> dict:
        return self.data


class B:
    def __init__(self: object) -> None:
        self.data = dict(a="a", b="b", c="c")

    def get(self: object) -> dict:
        return self.data


class C:
    def __init__(self: object) -> None:
        self.a = A()
        self.b = B()

    def get(self: object) -> bool:
        print(self.a.get().get("a"))
        if self.a.get().get("a") == "a":
            return True
        else:
            return False
