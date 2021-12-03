from random import getrandbits

import pytest

from sapsim.game.state.zone import Zone

#
# Globals
#
L = getrandbits(3) + 2 # zone length
assert L > 1

#
# Utility classes
#
class Cold():
    def __init__(self):
        self.frozen = True

class Warm():
    def __init__(self):
        self.frozen = False

class Gen():
    def random(self):
        return Cold() if getrandbits(1) else Warm()

#
# Fixtures for test setup
#
@pytest.fixture()
def empty():
    ret = Zone(L)
    return ret

@pytest.fixture()
def nofrz():
    ret = Zone(L)
    for i in range(L):
        ret.append(Warm())
    return ret

@pytest.fixture()
def frz():
    ret = Zone(L)
    for i in range(L-1):
        ret.append(Warm())
    ret.append(Cold())
    return ret

@pytest.fixture()
def gen():
    return Gen()

#
# Tests
#
def test_create(empty):
    assert len(empty.items) == L

def test_len(empty):
    assert len(empty) == L

def test_empty(empty):
    assert any(empty) == False
    assert empty.is_full() == False
    assert empty.is_empty() == True

def test_setitem(empty):
    empty[0] = 'a'
    assert empty.items[0] == 'a'

def test_getitem(empty):
    empty.items[0] = 'a'
    assert empty[0] == 'a'

def test_get(empty):
    for i in range(L):
        empty.append(i)
    assert empty.get(L-1) == L-1
    assert empty.get(0) == 0

def test_rm(empty):
    w = Warm()
    empty.append(w)
    assert empty.is_empty() == False
    empty.remove(w)
    assert empty.is_empty() == True

def test_notempty(nofrz):
    assert nofrz.is_full() == True

def test_clear(nofrz):
    nofrz.clear()
    assert any(nofrz) == False
    assert nofrz.is_full() == False
    assert nofrz.is_empty() == True

def test_too_full(nofrz):
    with pytest.raises(RuntimeError):
        nofrz.append(0)

def test_clear_frozen(frz):
    frz.clear()
    assert any(frz) == True
    assert len([f for f in frz if f is None]) == L-1
    assert frz.is_full() == False
    assert frz.is_empty() == False

def test_clear_fill_nofrz(nofrz, gen):
    refs = [i for i in nofrz] # keep objects in memory so 'id' checks work
    ids = [id(i) for i in refs]

    nofrz.clear_and_fill(gen)
    for i in nofrz:
        assert id(i) not in ids

    assert nofrz.is_full() == True
