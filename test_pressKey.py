import pytest
from eventsKey import eventkeyUp


"""
    pygameKeyUp = 3
    pygame.K_RIGHT = 275
    pygame.K_d = 100
    pygame.K_LEFT = 276
    pygame.K_a = 97
"""


class phatom():
    def __init__(self):
        self.type = 2
        self.key = 275

    def set(self, t, k):
        self.type = t
        self.key = k


p = phatom()


def test_Way124_1():
    p.set(3, 275)
    assert eventkeyUp(p) == 1


def test_Way124_2():
    p.set(3, 100)
    assert eventkeyUp(p) == 1


def test_Way125_1():
    p.set(3, 276)
    assert eventkeyUp(p) == -1


def test_Way125_2():
    p.set(3, 97)
    assert eventkeyUp(p) == -1


def test_Way126_1():
    p.set(3, -276)
    assert eventkeyUp(p) == 0


def test_Way126_2():
    p.set(3, 0)
    assert eventkeyUp(p) == 0


def test_Way126_3():
    p.set(3, 576)
    assert eventkeyUp(p) == 0


def test_Way126_4():
    p.set(3, 101)
    assert eventkeyUp(p) == 0


def test_Way13_1():
    p.set(-3, 275)
    assert eventkeyUp(p) == 0


def test_Way13_2():
    p.set(-3, 276)
    assert eventkeyUp(p) == 0


def test_Way13_3():
    p.set(-3, 100)
    assert eventkeyUp(p) == 0


def test_Way13_4():
    p.set(-3, 97)
    assert eventkeyUp(p) == 0


def test_Way13_5():
    p.set(0, 276)
    assert eventkeyUp(p) == 0


def test_Way13_6():
    p.set(33, 276)
    assert eventkeyUp(p) == 0


def test_obviusError_1():
    p.set('a', 276)
    assert eventkeyUp(p) == 0


def test_obviusError_2():
    p.set(0, 'f')
    assert eventkeyUp(p) == 0


def test_obviusError_3():
    p.set(3,True)
    assert eventkeyUp(p) == 0


def test_obviusError_3():
    p.set(True, 276)
    assert eventkeyUp(p) == 0
