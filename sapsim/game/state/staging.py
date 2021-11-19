# Zone where user places and arranges their mons
class Staging():
    def __init__(self, settings):
        self.settings = settings
        self.zone = [None for _ in range(settings.staging_zone_size())]
