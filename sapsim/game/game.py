from sapsim.game.settings import settings as sttngs
from sapsim.game.state import state as mystate
from sapsim import ai

class Game():
    def __init__(self):
        pass

    def load_default(self):
        self.settings = sttngs.Settings()
        self.state = mystate.State(self.settings)

    def get_all(self):
        return self.state.get_all()

    def new_turn(self):
        self.state.new_turn()

    def end_turn(self):
        self.state.end_turn()

    def battle(self):
        self.state.battle()

    def buy_mon(self, shopnum, stagenum):
        return self.state.buy_mon(shopnum, stagenum)

    def buy_item(self, shopnum, stagenum):
        return self.state.buy_item(shopnum, stagenum)

    def freeze_mon(self, shopnum):
        return self.state.freeze_mon(shopnum)

    def unfreeze_mon(self, shopnum):
        return self.state.unfreeze_mon(shopnum)

    def move(self, src, dest):
        return self.state.move(src, dest)

    def sell(self, num):
        return self.state.sell(num)

    def roll(self):
        return self.state.roll()

    def lives_left(self):
        return self.state.lives

    def win(self):
        return self.state.win()

    def loss(self):
        return self.state.loss()

    def draw(self):
        return self.state.draw()
