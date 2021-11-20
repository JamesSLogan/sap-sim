from sapsim.game.state import staging, shop
from sapsim.game.mon import mon
from sapsim.game.item import item

class State():
    Loading    = 0
    In_turn    = 1
    End_turn   = 2
    In_battle  = 3
    End_battle = 4
    Over = 5 #needed?

    def __init__(self, settings):
        self.staging = staging.Staging(settings)
        self.shop = shop.Shop(settings)
        self.mons = mon.Mons(settings)
        self.items = item.Items(settings)
        self.turn_num = 0
        self.currstate = State.Loading

    # Start 
    def advance_turn(self):
        self.turn_num += 1 # ??
        if self.turn_num > 1:
            # account for stuff that happened
            pass


        #self.staging.start_turn()
        self.shop.refresh(self.mons, self.items) # TODO: pass turn_num so shop knows sizes

        if self.currstate == State.Loading:
            self.currstate = State.In_turn

    def buy_mon(self, num):
        idx = num - 1
        if not self.mons.valid_idx(idx):
            raise ValueError()

    def buy_output(self):
        ret = []
        ret.append(self.shop.buy_output())
        return '\n'.join(ret)
