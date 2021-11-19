import random

class Mon():
    def __init__(self, data):
        self.name = data['name']
        self.hp = data['hp']
        self.atk = data['atk']
        self.ability = data.get('ability', None)
        self.item = data.get('item', None)

    def __str__(self):
        return f'{self.name}: ({self.atk},{self.hp})'

class Mons():
    def __init__(self, settings):
        self.settings = settings
        self.load(settings.mons())

    def load(self, mons):
        self.pool = []
        for mon in mons:
            self.pool.append(Mon(mon))

    def random(self):
        return random.choice(self.pool)
