import os
import json

def find(filename):
    for root, _, files in os.walk('.'):
        if filename in files:
            return os.path.join(root, filename)
    return None

class Settings():
    def __init__(self, fname='default.settings'):
        if not os.path.exists(fname):
            # Try and search for the file
            if search_res := find(fname):
                fname = search_res

        with open(fname) as f:
            self._settings = json.load(f)

    def __str__(self):
        return str(self._settings)

    def wins_needed(self):
        return self.game()['wins_needed']

    def starting_lives(self):
        return self.game()['starting_lives']

    def staging_zone_size(self):
        return self.game()['staging_zone_size']

    # coerces @turn to be within 0 and the length of @array then
    def turn_list_get(self, array, turn):
        index = turn - 1 # turn 1 == index 0
        index = min(index, len(array)-1)
        index = max(index, 0)
        return array[index]

    def item_zone_size(self, turn):
        return self.turn_list_get(self.game()['item_zone_size'], turn)

    def mon_zone_size(self, turn):
        return self.turn_list_get(self.game()['mon_zone_size'], turn)

    def game(self):
        return self._settings['game']

    def mons(self):
        return self._settings['mons']

    def items(self):
        return self._settings['items']
