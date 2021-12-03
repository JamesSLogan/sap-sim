from sapsim.game.buyable.buyable import Buyable

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
        'effects': None,
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
        frz = 'FROZEN' if self.frozen else ''
        eff = str(self.effect())+' ' if self.effects else ''

        return f'Lvl{self.level} {self.name}: ({self.atk},{self.hp}) ({self.exp}) {eff}{frz}'

    #def inc_exp(self, inc_stats=False):
    def inc_exp(self):
        if self.level == self.settings.max_level():
            return

        self.exp += 1

        if self.exp == self.settings.min_exp_per_level(self.level+1):
            self.level += 1
            # Level up effect
            #self.effects

        #if inc_stats:
        #    self.hp += 1
        #    self.atk += 1



    # Returns new mon using both inputs
    def combine(self, other):
        assert id(self) != id(other) # really should never happen
        assert self.name == other.name

        ret = Mon(self, self.settings)

        ret.hp = max(self.hp, other.hp) + 1
        ret.atk = max(self.atk, other.atk) + 1
        ret.exp = max(self.exp, other.exp)
        if not self.item and other.item:
            ret.item = other.item
        ret.inc_exp()

        return ret

    # "effect" is a function of a mon
    # "effects" is an attribute of a mon
    def effect(self):
        try:
            return self.effects.get_effect(self.level)
        except AttributeError:
            return None

    def is_alive(self):
        return self.hp > 0

class Mons():
    def __init__(self, settings):
        self.settings = settings
        self.load(settings)

    def load(self, settings):
        self.pool = []
        for mon in settings.mons():
            self.pool.append(Mon(mon, settings))

    def get(self, name):
        for mon in self.pool:
            if mon.name == name:
                return Mon(mon, self.settings)
        return mon

    def random(self):
        return Mon(random.choice(self.pool), self.settings)
