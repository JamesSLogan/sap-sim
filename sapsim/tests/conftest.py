from sapsim.game.state.team import Team
from sapsim.game.battle.battle import BattleTeam
from sapsim.game.buyable.mon import Mons
from sapsim.game.settings.settings import Settings

import pytest

@pytest.fixture(scope='module')
def settings():
    return Settings('../game/settings/default.settings')

@pytest.fixture(scope='module')
def mons(settings):
    return Mons(settings)

@pytest.fixture(scope='function')
def team(settings):
    return Team(settings)

@pytest.fixture(scope='function')
def bteam(team):
    return BattleTeam(team)

@pytest.fixture(scope='function')
def randmon(mons):
    return mons.random()

def get_and_lvl_up(mons, name, lvl=1):
    mon = mons.get(name)
    while mon.level < lvl:
        mon.inc_exp()
    return mon

@pytest.fixture(scope='function')
def cricket(mons):
    return get_and_lvl_up(mons, 'cricket', 1)

@pytest.fixture(scope='function')
def cricket_lvl2(mons):
    return get_and_lvl_up(mons, 'cricket', 2)

@pytest.fixture(scope='function')
def cricket_lvl3(mons):
    return get_and_lvl_up(mons, 'cricket', 3)

@pytest.fixture(scope='function')
def ant(mons):
    return get_and_lvl_up(mons, 'ant', 1)

@pytest.fixture(scope='function')
def ant_lvl2(mons):
    return get_and_lvl_up(mons, 'ant', 2)

@pytest.fixture(scope='function')
def ant_lvl3(mons):
    return get_and_lvl_up(mons, 'ant', 3)

@pytest.fixture(scope='function')
def beaver(mons):
    return get_and_lvl_up(mons, 'beaver', 1)

@pytest.fixture(scope='function')
def beaver_lvl2(mons):
    return get_and_lvl_up(mons, 'beaver', 2)

@pytest.fixture(scope='function')
def beaver_lvl3(mons):
    return get_and_lvl_up(mons, 'beaver', 3)
