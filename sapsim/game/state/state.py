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
        self.settings = settings
        self.currstate = State.Loading

        self.staging = staging.Staging(settings)
        #self.mons = mon.Mons(settings)
        #self.items = item.Items(settings)
        self.shop = shop.Shop(settings)

        self.turn_num = 0
        self.gold = None
        self.wins = 0
        self.lives = settings.starting_lives()

    def get_all(self):
        ret = {
            'turn': self.turn_num,
            'gold': self.gold,
            'wins': self.wins,
            'lives': self.lives,
        }
        ret.update({'staging': self.staging.get_all()})
        ret.update(self.shop.get_all())
        return ret

    def new_turn(self):
        self.turn_num += 1 # ??
        if self.turn_num > 1:
            # account for stuff that happened
            pass

        self.gold = self.settings.gold_per_turn()

        #self.shop.refresh(self.mons, self.items) # TODO: pass turn_num so shop knows sizes
        self.shop.refresh(self.turn_num) # TODO: pass turn_num so shop knows sizes

        if self.currstate == State.Loading:
            self.currstate = State.In_turn

    def end_turn(self):
        pass

    def battle(self, other):
        pass

    def buy_mon(self, shopnum, stagenum):
        combine = False

        # Validate purchase
        purchase_mon = self.shop.get_mon(shopnum)
        save_ref = purchase_mon
        if not purchase_mon:
            raise ValueError('Invalid shop id')

        if purchase_mon.price > self.gold:
            raise ValueError('Not enough gold')

        stage_mon = self.staging.get(stagenum)
        if stage_mon is not None and stage_mon.name != purchase_mon.name:
            raise ValueError('Invalid placement')

        if stage_mon:
            combine = True
            purchase_mon = stage_mon.combine(purchase_mon)

        # Execute purchase
        self.gold -= purchase_mon.price
        self.shop.remove_mon(save_ref) # shop doesn't contain the combined one
        self.staging.add(purchase_mon, stagenum, combine)

    def buy_item(self, shopnum, stagenum):
        return self.shop.buy_item(num)

    def freeze_mon(self, num):
        self.shop.freeze_mon(num)

    def freeze_item(self, num):
        self.shop.freeze_item(num)

    def unfreeze_mon(self, num):
        self.shop.unfreeze_mon(num)

    def unfreeze_item(self, num):
        self.shop.unfreeze_item(num)

    def sell(self, num):
        if not (mon := self.staging.get(num)):
            raise ValueError('invalid number')
        self.gold += self.settings.gold_per_level(mon.level)
        self.staging.rm(num)

    def move(self, src, dest):
        if src == dest:
            return

        try:
            src_mon = self.staging[src]
        except IndexError:
            raise ValueError('Invalid source specified')
        try:
            dest_mon = self.staging[dest]
        except IndexError:
            raise ValueError('Invalid destination specified')

        self.staging[src] = dest_mon
        self.staging[dest] = src_mon

    def roll(self):
        gpr = self.settings.gold_per_roll()
        if self.gold < gpr:
            raise ValueError('Not enough gold')
        self.gold -= gpr
        self.shop.refresh()
