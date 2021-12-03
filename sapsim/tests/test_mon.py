import pytest

from sapsim.game.buyable.mon import Mon
from sapsim.game.settings.settings import Settings

nest = {
    "name": "nestor",
    "hp": 1,
    "atk": 1,
}

lest = {
    "name": "lestor",
    "hp": 2,
    "atk": 2,
}

@pytest.fixture
def nestor(settings):
    return Mon(nest, settings)

@pytest.fixture
def lestor(settings):
    return Mon(lest, settings)

def test_alive(nestor):
    assert nestor.is_alive()
    nestor.hp = 0
    assert not nestor.is_alive()

def test_exp(nestor, settings):
    #
    # Confusing setup
    #
    min_level = 1 # assumption...
    max_exp = settings.min_exp_per_level(settings.max_level())
    curr_level = min_level

    # We want to double check that nothing happens if exp increases higher
    # than what's possible so we add extra entries here.
    expected_exp = list(range(max_exp+1)) + [max_exp, max_exp]

    expected_lvl = []
    for exp in expected_exp:
        try:
            if exp == settings.min_exp_per_level(curr_level+1):
                curr_level += 1
        except IndexError:
            pass
        expected_lvl.append(curr_level)

    #
    # Actual test
    #
    for exp, lvl in zip(expected_exp, expected_lvl):
        assert exp == nestor.exp
        assert lvl == nestor.level
        nestor.inc_exp()

def test_combine(nestor, settings):
    if settings.min_exp_per_level(1) != 0:
        return # can't run test as is

    other = Mon(nest, settings)
    count = 0
    while True:
        other = nestor.combine(other)
        count += 1
        assert other.hp == nestor.hp + count
        assert other.atk == nestor.atk + count
        assert other.exp == nestor.exp + count

        # test until level up
        if count == settings.min_exp_per_level(2):
            assert other.level == nestor.level + 1
            break

        if count > 1000:
            print('This should have not happened')
            assert False

