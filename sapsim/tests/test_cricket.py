from sapsim.game.buyable.mon import Mons

import pytest
 
# Test assumes that Team size won't be lower than 3

# TODO test with pill

@pytest.fixture()
def not_cricket_2(mons):
    ret = []
    while True:
        if (curr := mons.random()).name != 'cricket':
            ret.append(curr)
            if len(ret) == 2:
                break
    return ret

def cricket_faint(bteam, data):
    cricket = data['cricket']
    other1 = data['other1']
    other2 = data['other2']

    assert bteam.is_empty()

    bteam.add(cricket[0], cricket[1])
    bteam.add(other1[0], other1[1])
    bteam.add(other2[0], other2[1])

    # Make sure everything is in place
    for i, mon in enumerate(bteam):
        if i == cricket[1]:
            assert mon is cricket[0]
        elif i == other1[1]:
            assert mon is other1[0]
        elif i == other2[1]:
            assert mon is other2[0]
        else:
            assert mon is None

    bteam.faint(cricket[0])

    # Make sure effect spawned new cricket in same place
    for i, mon in enumerate(bteam):
        if i == cricket[1]:
            assert mon is not cricket[0]
            assert mon.name == 'cricket'
            assert mon.effects == None
        elif i == other1[1]:
            assert mon is other1[0]
        elif i == other2[1]:
            assert mon is other2[0]
        else:
            assert mon is None

def test_front(bteam, cricket, not_cricket_2):
    cricket_faint(
        bteam,
        {
            'cricket': (cricket, 0),
            'other1': (not_cricket_2[0], 1),
            'other2': (not_cricket_2[1], 2),
        }
    )

def test_mid(bteam, cricket, not_cricket_2):
    cricket_faint(
        bteam,
        {
            'other1': (not_cricket_2[0], 0),
            'cricket': (cricket, 1),
            'other2': (not_cricket_2[1], 2),
        }
    )

def test_back(bteam, cricket, not_cricket_2):
    cricket_faint(
        bteam,
        {
            'other1': (not_cricket_2[0], 0),
            'other2': (not_cricket_2[1], 1),
            'cricket': (cricket, 2),
        }
    )

def test_levels(bteam, cricket, cricket_lvl2, cricket_lvl3):
    bteam.add(cricket, 0)
    bteam.add(cricket_lvl2, 1)
    bteam.add(cricket_lvl3, 2)

    bteam.faint(cricket)
    bteam.faint(cricket_lvl2)
    bteam.faint(cricket_lvl3)

    c0 = bteam.get(0)
    c1 = bteam.get(1)
    c2 = bteam.get(2)

    assert c0 is not None
    assert c1 is not None
    assert c2 is not None

    assert c0 is not cricket
    assert c1 is not cricket_lvl2
    assert c2 is not cricket_lvl3

    # This could change in the future
    assert c2.hp > c1.hp > c0.hp
    assert c2.atk > c1.atk > c0.atk
