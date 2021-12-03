from sapsim.game.state.team import Team
from sapsim.game.buyable.mon import Mon
from sapsim.game.battle.flow import process_faint_effect

black  = '\033[30m'
red    = '\033[31m'
green  = '\033[32m'
yellow = '\033[33m'
blue   = '\033[34m'
purple = '\033[35m'
cyan   = '\033[36m'
clear  = '\033[0m' # default color, not see-through "clear"
bold   = '\033[1m'
strike = '\033[9m'

sep = '#' * 40

class BattleTeam(Team):
    def __init__(self, team):
        self.settings = team.settings
        self.size = team.size

        # Deep copy the zone
        # TODO: make sure spaces can be eliminated here
        #self.zone = [Mon(m, self.settings) for m in team.zone if m is not None]
        self.zone = team.zone

    def get_first(self):
        for item in self.zone:
            if item:
                return item
        raise RuntimeError('get_first called on empty team')

    def all_dead(self):
        return not any(self.zone)

    # different than Team's is_full
    # TODO investigate if Team's is_full can just be this
    def is_full(self):
        if len(self.zone) < self.size:
            return False
        return all(self.zone)

    # note that this is slightly different from Team's faint due to
    # how spaces between mons are handled
    # TODO: handle spaces
    def faint(self, mon):
        idx = self.index(mon)
        self.delete_by_ref(mon)
        effect = mon.effect()
        if not effect or effect.trigger != 'faint':
            return

        process_faint_effect(self, effect, mon, idx)

def battle_output(mon1, mon2):
    color = blue+strike if not mon1.is_alive() else blue
    print(f'{color}{mon1}{clear}')
    color = purple+strike if not mon2.is_alive() else purple
    print(f'{color}{mon2}{clear}')
    print()

def mon_battle(mon1, mon2):
    battle_output(mon1, mon2)
    while mon1.is_alive() and mon2.is_alive():
        mon1.hp -= mon2.atk
        mon2.hp -= mon1.atk
    battle_output(mon1, mon2)

def battle(team1_in, team2_in):
    team1 = BattleTeam(team1_in)
    team2 = BattleTeam(team2_in)

    print(sep)
    print('START BATTLE:')
    print(team1)
    print('VS')
    print(team2)

    iterations = 0

    while not team1.all_dead() and not team2.all_dead():
        print(sep)
        mon1 = team1.get_first()
        mon2 = team2.get_first()
        mon_battle(mon1, mon2)
        if not mon1.is_alive():
            team1.faint(mon1)
        if not mon2.is_alive():
            team2.faint(mon2)

        iterations += 1
        if iterations > 200:
            raise RuntimeError('infinite battle detected\n{team1}\n{team2}')

    if team1.all_dead() and team2.all_dead():
        print('DRAW')
        return None
    elif team1.all_dead():
        print('AI win')
        return team2_in
    else:
        print('You win')
        return team1_in

