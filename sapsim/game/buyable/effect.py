from sapsim.game.buyable.trigger import Trigger

class Effect():
    def __init__(self, data):
        self.description = data['description']
        #self.trigger = Trigger(data['trigger'])
        self.trigger = data['trigger']
        self.effect = data['effect']
        self.data = data['data']

    def __str__(self):
        return f'{self.description}'

# Mons have a list of effects, 1 per level.
# Some mons' effects don't level up but there isn't a way to specify that
# non-redundantly yet.
class Effects():
    def __init__(self, data):
        assert isinstance(data, list) # expect to remove later
        self.effects = [Effect(d) for d in data]

    def get_effect(self, level):
        return self.effects[level-1]


