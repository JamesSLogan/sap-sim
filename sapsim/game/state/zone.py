# A Zone is an object that manages adding and removing items when told to do so.
# Zones are aware of frozen items.
# Zones can have their size expanded.
class Zone():
    def __init__(self, size):
        self.size = size
        self.items = [None for _ in range(size)]

    def __str__(self):
        return '\n'.join([str(i) for i in self])

    def __iter__(self):
        yield from self.items

    def __getitem__(self, k):
        return self.items[k]

    def __setitem__(self, k, v):
        self.items[k] = v

    def __len__(self):
        return len(self.items)

    def get(self, i):
        try:
            return self[i]
        except IndexError:
            return None

    def index(self, item):
        return self.items.index(item)

    def get_all(self):
        return self.items

    def expand(self, by=1):
        self.size += by

    # Will raise ValueError if @item is not in @self
    def remove(self, item):
        self[self.index(item)] = None

    def is_full(self):
        # Account for when size was increased
        if len(self) < self.size:
            return False

        for item in self:
            if item is None:
                return False
        return True

    def is_empty(self):
        for item in self:
            if item is not None:
                return False
        return True

    # places item in first empty slot
    def append(self, new_item):
        for i, item in enumerate(self):
            if item is None:
                self[i] = new_item
                break
        else:
            raise RuntimeError('added too many items to zone')

    # Clear out non-frozen items
    def clear(self):
        for i, item in enumerate(self):
            try:
                if item.frozen: # object needs to support 'frozen'
                    continue
            except AttributeError:
                continue
            self[i] = None

    # Uses 'gen' to add objects to self
    def clear_and_fill(self, gen):
        self.clear()
        while not self.is_full():
            self.append(gen.random()) # object needs to support 'random'
