from random import sample

# Zone where user places and arranges their mons
class Team():
    def __init__(self, settings):
        self.settings = settings
        self.size = settings.team_size()
        self.zone = [None for _ in range(self.size)]

    def __str__(self):
        return '\n'.join(f'{mon}' for mon in self.zone)

    def __getitem__(self, k):
        return self.zone[k]

    def __setitem__(self, k, v):
        self.zone[k] = v

    def __iter__(self):
        yield from self.zone

    def is_full(self):
        return all(self.zone)

    def is_empty(self):
        return not any(self.zone)

    def num_alive(self):
        return len([mon for mon in self if mon is not None])

    def index(self, mon):
        return self.zone.index(mon)

    def get(self, num):
        try:
            return self[num]
        except IndexError:
            return None

    def delete_by_ref(self, mon):
        self[self.index(mon)] = None

    def delete(self, num):
        try:
            self[num] = None
        except IndexError:
            pass

    def get_all(self):
        return self[:]

    # returns a list
    def random(self, count=1):
        if count > self.num_alive():
            raise RuntimeError('Internal error: too many random mons requested')

        return sample([mon for mon in self if mon is not None], count)

    # Place mon at num. Overwrites current object when @combine is true
    # Could have better error handling?
    def add(self, mon, num, combine=False):
        currmon = self.get(num)
        assert combine == (currmon is not None)
        self[num] = mon
