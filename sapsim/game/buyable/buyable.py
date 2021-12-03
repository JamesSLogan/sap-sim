from sapsim.game.buyable.effect import Effect, Effects

# Common code for Mon and Item objects
class Buyable():
    # Define default attributes to allow some flexibility in settings
    Attrs = {
        'price': 3,
    }

    # @data is another Buyable object or a dict with data
    # @settings is a Settings object
    # @myattrs is a dict with attributes and default values
    def __init__(self, data, settings, myattrs):
        self.settings = settings
        self.frozen = False

        self.assign(data, Buyable.Attrs)
        self.assign(data, myattrs)

    def assign(self, data, attrs):
        #
        # Called when reading from settings
        #
        if isinstance(data, dict):
            for attr in attrs:
                if attr in data:
                    #
                    # Most attributes are simple to load but for any nested
                    # JSON we need to do some additional parsing
                    #
                    if attr == 'effects': # for mons
                        setattr(self, attr, Effects(data[attr]))
                    #elif attr == 'effect': # for items
                    #    setattr(self, attr, Effect(data[attr]))
                    else:
                        setattr(self, attr, data[attr])
                #
                # Use defaults
                #
                else:
                    setattr(self, attr, attrs[attr])

        #
        # Called when copying from existing buyables
        #
        else:
            for attr in attrs:
                try:
                    setattr(self, attr, getattr(data, attr))
                #
                # Use defaults - could this be deleted?
                #
                except AttributeError:
                    setattr(self, attr, attrs[attr])

    def freeze(self):
        self.frozen = True

    def unfreeze(self):
        self.frozen = False

    def is_frozen(self):
        return self.frozen
