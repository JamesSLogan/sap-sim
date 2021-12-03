import random

def we_have_enough_gold(mons, gold):
    for mon in mons:
        if mon == None:
            continue
        if mon.price <= gold:
            return True
    return False

def random_null_idx(array):
    return random.choice([i for i, v in enumerate(array) if v is None])

def random_nonnull_idx(array):
    return random.choice([i for i, v in enumerate(array) if v is not None])

def get_random_mon(mons):
    return random_nonnull_idx(mons)

def get_random_empty_spot(team):
    return random_null_idx(team)

def spend_gold(g):
    while True:
        info = g.get_all()
        gold = info['gold']
        mons = info['mons']
        team = info['team']

        if gold == 0:
            break

        if not any(info['mons']):
            g.roll()
            continue

        # buy mon
        if we_have_enough_gold(mons, gold) and not g.state.team.is_full():
            mon = get_random_mon(mons)
            placement = get_random_empty_spot(team)
            g.buy_mon(mon, placement)
            continue

        g.roll()


