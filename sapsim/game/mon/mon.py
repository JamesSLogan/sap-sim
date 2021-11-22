from sapsim.game.state.buyable import Buyable

import random

# triggers:
# start turn
# end turn
# mon faint
# mon hurt
# buy mon
# sell mon
# mon eat food
# buy food
# start battle
# friend summoned
# friend bought
# friend ahead attacks
# friend faints
# mon hurt
# mon gets a ko
# level-up
# tiger

class Mon(Buyable):
    # Define attributes and default values specific to a Mon
    Attrs = {
        'name': 'YOUSHOULDNEVERSEETHIS',
        'hp': 1,
        'atk': 1,
        'ability': None,
        'item': None,
        'exp': 0,
        'level': 1,
    }

    # Note that @data is another Mon or mon-specific data from settings
    def __init__(self, data, settings):
        super().__init__(data, settings, Mon.Attrs)
        if self.name == Mon.Attrs['name']:
            raise RuntimeError('You forgot to specify a mon name.')

    def __str__(self):
        frz = ''
        if self.frozen:
            frz = 'FROZEN'

        return f'Lvl{self.level} {self.name}: ({self.atk},{self.hp}) ({self.exp}) {frz}'

    def inc_exp(self):
        if self.level == self.settings.max_level():
            return
        self.exp += 1
        if self.exp == self.settings.min_exp_per_level(self.level+1):
            self.level += 1

        # TODO level up ability


    # Returns new mon using both inputs
    def combine(self, other):
        assert id(self) != id(other) # really should never happen
        assert self.name == other.name

        ret = Mon(self, self.settings)

        ret.hp = max(self.hp, other.hp) + 1
        ret.atk = max(self.atk, other.atk) + 1
        if not self.item and other.item:
            ret.item = other.item
        ret.inc_exp()

        return ret

class Mons():
    def __init__(self, settings):
        self.settings = settings
        self.load(settings)

    def load(self, settings):
        self.pool = []
        for mon in settings.mons():
            self.pool.append(Mon(mon, settings))

    def random(self):
        return Mon(random.choice(self.pool), self.settings)
