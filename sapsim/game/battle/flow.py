from sapsim.game.buyable.mon import Mon

# @mon is the now fainted mon
# @idx is the index of the now fainted mon
def process_faint_effect(team, effect, mon, idx):
    if effect.effect == 'summon_inplace':
        process_summon(team, effect, mon, idx)

    elif effect.effect == 'buff_random':
        process_buff_random(team, effect)

    else:
        raise RuntimeError('Invalid faint effect')

def process_sell_effect(team, effect):
    if effect.effect == 'buff_random_2':
        process_buff_random(team, effect, 2)

    else:
        raise RuntimeError('Invalid sell effect')

def process_summon(team, effect, orig_mon, idx):
    if team.is_full():
        return

    new_mon = Mon(effect.data, orig_mon.settings)
    team.add(new_mon, idx, False)

def process_buff_random(team, effect, count=1):
    if team.is_empty():
        return # nothing to do

    # Get random mons to apply effect. If requested amount is more than the
    # team can provide, we request fewer. This means that, for example, the
    # beaver will only buff 1 mon instead of 2 if only 1 mon is alive.
    while True:
        try:
            mons = team.random(count)
            break
        except RuntimeError:
            count -= 1
            assert count > 0 # hope this doesn't happen

    for mon in mons:
        mon.atk += effect.data.get('atk', 0)
        mon.hp += effect.data.get('hp', 0)
