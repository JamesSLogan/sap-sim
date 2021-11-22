from textwrap import dedent

from sapsim.game.state.zone import Zone
from sapsim.game.mon import mon
from sapsim.game.item import item

class Shop():
    def __init__(self, settings):
        self.settings = settings
        self.mons = mon.Mons(settings)
        self.items = item.Items(settings)
        self.mon_zone = Zone(settings.mon_zone_size(1))
        self.item_zone = Zone(settings.item_zone_size(1))

    # Used when rolling or starting a turn
    def refresh(self, turn_num=1):
        self.mon_zone.clear_and_fill(self.mons)
        self.item_zone.clear_and_fill(self.items)
        assert len(self.mon_zone) == self.settings.mon_zone_size(turn_num)
        assert len(self.item_zone) == self.settings.item_zone_size(turn_num)

    def get_all(self):
        return {
            'mons': self.mon_zone.get_all(),
            'items': self.item_zone.get_all()
        }

    def get_mon(self, num):
        return self.mon_zone.get(num)

    def get_item(self, num):
        return self.item_zone.get(num)

    def remove_mon(self, mon):
        return self.mon_zone.remove(mon)

    def remove_item(self, item):
        return self.item_zone.remove(item)

    def _freeze(self, src, num):
        if not (obj := src.get(num)):
            raise ValueError(f'invalid number ({num})')
        obj.freeze()

    def _unfreeze(self, src, num):
        if not (obj := src.get(num)):
            raise ValueError(f'invalid number ({num})')
        obj.unfreeze()

    def freeze_mon(self, num):
        return self._freeze(self.mon_zone, num)

    def freeze_item(self, num):
        return self._freeze(self.item_zone, num)

    def unfreeze_mon(self, num):
        return self._unfreeze(self.mon_zone, num)

    def unfreeze_item(self, num):
        return self._unfreeze(self.item_zone, num)
