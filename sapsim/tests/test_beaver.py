from sapsim.game.buyable.mon import Mons

import pytest
 
def test_faint_simple(bteam, ant, randmon):
    bteam.add(ant, 0)
    bteam.add(randmon, 1)

    prev_atk = randmon.atk
    prev_hp = randmon.hp

    bteam.faint(ant)

    assert bteam.get(0) is None
    assert randmon.atk == prev_atk + 2
    assert randmon.hp == prev_hp + 1

def test_faint_team(bteam, ant, mons):
    r1 = mons.random()
    r2 = mons.random()

    bteam.add(ant, 0)
    bteam.add(r1, 1)
    bteam.add(r2, 2)

    prev_atk = sum((r1.atk, r2.atk))
    prev_hp = sum((r1.hp, r2.hp))

    bteam.faint(ant)

    assert bteam.get(0) is None
    assert sum((r1.atk, r2.atk)) == prev_atk + 2
    assert sum((r1.hp, r2.hp)) == prev_hp + 1

# basically makes sure no errors are thrown
def test_faint_empty(bteam, ant):
    bteam.add(ant, 0)
    bteam.faint(ant)

    assert bteam.get(0) is None
