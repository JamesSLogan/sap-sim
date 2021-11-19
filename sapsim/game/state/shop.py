from textwrap import dedent

from sapsim.game.state.zone import Zone

class Shop():
    def __init__(self, settings):
        self.settings = settings
        self.mon_zone = Zone(settings.mon_zone_size(1))
        self.item_zone = Zone(settings.item_zone_size(1))

    # Used when rolling or starting a turn
    def refresh(self, mons, items):
        self.mon_zone.clear_and_fill(mons)
        self.item_zone.clear_and_fill(items)

    def buy_output(self):
        ret = ['Animals:']
        for i, mon in enumerate(self.mon_zone):
            display_i = i+1
            ret.append(f'{display_i}: {mon}')
        ret.append('')

        ret.append('Items:')
        for i, item in enumerate(self.item_zone):
            display_i = i+1
            ret.append(f'{display_i}: {item}')
        return '\n'.join(ret)
