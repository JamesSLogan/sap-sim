from sapsim.game.state import team, shop
from sapsim.game.battle.flow import process_sell_effect

class State():
    def __init__(self, settings):
        self.settings = settings
        self.team = team.Team(settings)
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
        ret.update({'team': self.team.get_all()})
        ret.update(self.shop.get_all())
        return ret

    def new_turn(self):
        self.turn_num += 1 # ??

        self.gold = self.settings.gold_per_turn()

        self.shop.refresh(self.turn_num)

    def end_turn(self):
        pass

    #def battle(self, other):
    #    pass

    def buy_mon(self, shopnum, stagenum):
        combine = False

        # Validate purchase
        purchase_mon = self.shop.get_mon(shopnum)
        save_ref = purchase_mon
        if not purchase_mon:
            raise ValueError('Invalid shop id')

        if purchase_mon.price > self.gold:
            raise ValueError('Not enough gold')

        stage_mon = self.team.get(stagenum)
        if stage_mon is not None and stage_mon.name != purchase_mon.name:
            raise ValueError('Invalid placement')

        if stage_mon:
            combine = True
            purchase_mon = stage_mon.combine(purchase_mon)

        # Execute purchase
        self.gold -= purchase_mon.price
        self.shop.remove_mon(save_ref) # shop doesn't contain the combined one
        self.team.add(purchase_mon, stagenum, combine)

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
        if not (mon := self.team.get(num)):
            raise ValueError('invalid number')
        self.gold += self.settings.gold_per_level(mon.level)
        self.team.delete(num)

        effect = mon.effect()
        if effect and effect.trigger == 'sell':
            process_sell_effect(self.team, effect)

    def move(self, src, dest):
        if src == dest:
            return

        try:
            src_mon = self.team[src]
        except IndexError:
            raise ValueError('Invalid source specified')
        try:
            dest_mon = self.team[dest]
        except IndexError:
            raise ValueError('Invalid destination specified')

        self.team[src] = dest_mon
        self.team[dest] = src_mon

    def roll(self):
        gpr = self.settings.gold_per_roll()
        if self.gold < gpr:
            raise ValueError('Not enough gold')
        self.gold -= gpr
        self.shop.refresh()

    def win(self):
        self.wins += 1

    def loss(self):
        self.lives -= 1

    def draw(self):
        pass
