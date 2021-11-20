from sapsim.game.settings import settings as sttngs
from sapsim.game.state import state as mystate

class Game():
    def __init__(self):
        pass

    #def load(self, fname):
    #    self.settings = sttngs.Settings(fname=fname)
    #    return self.settings

    def load_default(self):
        self.settings = sttngs.Settings()
        self.state = mystate.State(self.settings)

    def get_state_num(self):
        return self.state.currstate

    def advance_turn(self):
        self.state.advance_turn()

    def buy_mon(self, num):
        return self.state.buy_mon(num)
