# Zone where user places and arranges their mons
class Staging():
    def __init__(self, settings):
        self.settings = settings
        self.zone = [None for _ in range(settings.staging_zone_size())]

    def __getitem__(self, k):
        return self.zone[k]

    def __setitem__(self, k, v):
        self.zone[k] = v

    def is_full(self):
        return all(self.zone)

    def get(self, num):
        try:
            return self[num]
        except IndexError:
            return None

    def rm(self, num):
        try:
            self[num] = None
        except IndexError:
            pass

    def get_all(self):
        return self[:]

    # Place mon at num. Overwrites current object when @combine is true
    # Could have better error handling?
    def add(self, mon, num, combine=False):
        currmon = self.get(num)
        assert combine == (currmon is not None)
        self[num] = mon
