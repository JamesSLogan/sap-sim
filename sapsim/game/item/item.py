import random

class Item():
    def __init__(self, data):
        #print(data)
        #print(type(data))
        #print()
        self.name = data['name']
        self.effect = data.get('effect') # could be implemented same way as a mon ability?

    def __str__(self):
        return f'{self.name}'

class Items():
    def __init__(self, settings):
        self.settings = settings
        self.load(self.settings.items())

    def load(self, items):
        self.pool = []
        for item in items:
            self.pool.append(Item(item))

    def random(self):
        return random.choice(self.pool)
