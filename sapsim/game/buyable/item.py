from sapsim.game.buyable.buyable import Buyable

import random

# add stats
# add stats temporarily
# +atk in battle (steak is 1x only)
# +def in battle ("def")
# -def in battle
# splash attack
# armor
# extra life
# +exp
# canned food
# pill
# scorp

class Item(Buyable):
    # Define attributes and default values specific to an Item
    Attrs = {
        'name': 'INCONCEIVABLE',
        'effect': None
    }

    # Note that @data is another Item or item-specific data from settings
    def __init__(self, data, settings):
        super().__init__(data, settings, Item.Attrs)
        if self.name == Item.Attrs['name']:
            raise RuntimeError('You forgot to specify an item name.')

    def __str__(self):
        return f'{self.name}'

class Items():
    def __init__(self, settings):
        self.settings = settings
        self.load(settings)

    def load(self, settings):
        self.pool = []
        for item in settings.items():
            self.pool.append(Item(item, settings))

    def random(self):
        return Item(random.choice(self.pool), self.settings)
