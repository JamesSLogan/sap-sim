#!/usr/bin/env python
import code
import readline
import rlcompleter

from textwrap import dedent

from sapsim.game import game as mygame
from sapsim.game.state import state as mystate

black  = '\033[30m'
red    = '\033[31m'
green  = '\033[32m'
yellow = '\033[33m'
blue   = '\033[34m'
purple = '\033[35m'
cyan   = '\033[36m'
clear  = '\033[0m'
bold   = '\033[1m'

sep = '-' * 40

def input_error_msg(obj=''):
    if isinstance(obj, BaseException):
        try:
            msg = obj.args[0]
        except IndexError:
            msg = ''
    else:
        msg = obj

    if msg:
        printme = f': ({msg})'
    else:
        printme = ''

    print(f'{red}Invalid input{printme}. Please try again.{clear}\n')
    return False

def input_loop(allowed, prompt):
    while True:
        text = input(prompt)
        if text.lower() in allowed:
            return text.lower()
        else:
            input_error_msg()

def turn_help():
    print(dedent(f'''\
        {purple}Available Commands{clear}:
        {sep}
        buy mon|item <id> <id>    ex: "buy mon 1 4", "buy item 2 1"
        [un]freeze mon|item <id>  ex: "freeze mon 1", "unfreeze item 2"
        move <id> <id>            ex: "move 4 1"
        sell <id>                 ex: "sell 1"
        roll
        done
    '''))

# Converts user input to what the game expects
def usernum_to_gamenum(num):
    try:
        num = int(num)
    except:
        raise RuntimeError

    num -= 1

    if num < 0:
        raise RuntimeError

    return num

# Converts game input to something the user can more easily digest
def gamenum_to_usernum(num):
    return num + 1

# Converts 'None' input to a string suitable for the user.
def no_none(arg):
    if arg is None:
        return '_____'
    else:
        return arg

def numbered_output(array):
    ret = []
    for i, item in enumerate(array):
        ret.append(f'{gamenum_to_usernum(i)}: {no_none(item)}')
    return ret

def prompt_buy(g):
    info = g.get_all()

    staging_list = [f'{bold}Your team{clear}:'] + numbered_output(info['staging'])
    mons_list    = [f'{bold}Animals{clear}:'] + numbered_output(info['mons'])
    items_list   = [f'{bold}Items{clear}:'] + numbered_output(info['items'])

    ret = [
        sep,
        ' '.join([
            f'{bold}Turn{clear}: {info["turn"]}',
            f'{bold}Wins{clear}: {info["wins"]}',
            f'{bold}Lives{clear}: {info["lives"]}',
        ]),
        f'{yellow}Gold{clear}: {info["gold"]}',
        '',
        '\n'.join(mons_list),
        '',
        '\n'.join(items_list),
        '',
        '\n'.join(staging_list),
        '',
    ]
    return '\n'.join(ret)

def process_buy(g, tokens):
    try:
        location = tokens[1]
        shopnum = usernum_to_gamenum(tokens[2])
        stagenum = usernum_to_gamenum(tokens[3])
    except IndexError:
        return input_error_msg('too few arguments')
    except RuntimeError as e:
        return input_error_msg(e)

    if location == 'mon':
        try:
            return g.buy_mon(shopnum, stagenum)
        except ValueError as e:
            return input_error_msg(e)

    elif location == 'item':
        try:
            return g.buy_item(shopnum, stagenum)
        except ValueError as e:
            return input_error_msg(e)
    else:
        return input_error_msg('argument #2 is invalid.')

def process_freezes(g, tokens):
    try:
        action = tokens[0]
        location = tokens[1]
        num = usernum_to_gamenum(tokens[2])
    except IndexError:
        return input_error_msg('too few arguments')
    except RuntimeError as e:
        return input_error_msg(e)

    if location == 'mon':
        try:
            if action == 'freeze':
                return g.freeze_mon(num)
            else:
                return g.unfreeze_mon(num)
        except ValueError as e:
            return input_error_msg(e)
    elif location == 'item':
        try:
            if action == 'freeze':
                return g.freeze_item(num)
            else:
                return g.unfreeze_item(num)
        except ValueError as e:
            return input_error_msg(e)
    else:
        return input_error_msg('argument #2 is invalid.')

def process_move(g, tokens):
    try:
        action = tokens[0]
        src = usernum_to_gamenum(tokens[1])
        dest = usernum_to_gamenum(tokens[2])
    except IndexError:
        return input_error_msg('too few arguments')
    except RuntimeError as e:
        return input_error_msg(e)

    try:
        return g.move(src, dest)
    except ValueError as e:
        return input_error_msg(e)

def process_sell(g, tokens):
    try:
        sell_num = usernum_to_gamenum(tokens[1])
    except IndexError:
        return input_error_msg('too few arguments')
    except RuntimeError as e:
        return input_error_msg(e)

    try:
        print(f'try sell {sell_num}')
        return g.sell(sell_num)
    except ValueError as e:
        return input_error_msg(e)

def process_roll(g):
    try:
        g.roll()
    except ValueError as e:
        return input_error_msg(e)

def process_end_turn(g):
    g.end_turn()

def process_turn(g, text):
    tokens = text.split()
    cmd = tokens[0].lower() # this is safe

    if cmd == 'h' or cmd == 'help':
        turn_help()
        return False

    elif cmd == 'buy':
        process_buy(g, tokens)

    elif cmd == 'freeze' or cmd == 'unfreeze':
        process_freezes(g, tokens)

    elif cmd == 'move':
        process_move(g, tokens)

    elif cmd == 'sell':
        process_sell(g, tokens)

    elif cmd == 'roll':
        process_roll(g)

    elif cmd == 'done':
        process_end_turn(g)

    else:
        input_error_msg('invalid command')
    return True

def _prompt(g):
    if g.get_state_num() == mystate.State.In_turn:
        return prompt_buy(g)

def prompt(g):
    print(_prompt(g))

def process(g, text):
    ret = {
        'done': False,
        'prompt': True,
    }

    if not text or text.isspace():
        ret['prompt'] = False
        return ret

    if text.lower() == 'q':
        if True: # remove later
            ret['done'] = True
            return ret

        choice = input_loop(['y', 'n'], 'Are you sure? (y/n): ')

        if choice == 'y':
            ret['done'] = True
            return ret
        elif choice == 'n':
            return ret

    if g.get_state_num() == mystate.State.In_turn:
        ret['prompt'] = process_turn(g, text)
        return ret

# Sets up a game and lets the user interact with it
def launch():
    g = mygame.Game()
    g.load_default()
    g.new_turn()

    # initialize AI team
    g2 = mygame.Game()
    g2.load_default()
    g2.new_turn()
    g2.spend_gold()


    status = {
        'done': False,
        'prompt': True,
    }

    while not status['done']:
        if status['prompt']:
            prompt(g)

        userin = input('Next input (h=help, q=quit): ')
        status = process(g, userin)

    #print('Store:')
    #print(g.state.shop.mon_zone)
    #print(g.state.shop.item_zone)

    #readline.set_completer(rlcompleter.Completer(globals()).complete)
    #readline.parse_and_bind('tab: complete')
    #code.interact(local=globals())
