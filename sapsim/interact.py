#!/usr/bin/env python
import code
import readline
import rlcompleter

from textwrap import dedent

from sapsim.game import game as mygame
from sapsim.game.state import state as mystate

def input_error_msg():
    print('\033[31mInvalid input, please try again.\033[0m\n')

def input_loop(allowed, prompt):
    while True:
        text = input(prompt)
        if text.lower() in allowed:
            return text.lower()
        else:
            input_error_msg()

def help_buy():
    print(dedent('''\
        Available Commands:
        -------------------
        buy mon|item <id>         ex: "buy mon 1", "buy item 2"
        sell <id>                 ex: "sell 1"
        freeze mon|item <id>      ex: "freeze mon 1"
        move <id> <id>            ex: "move 4 1"
    '''))

def prompt_buy(g):
    return g.state.buy_output()

def process_buy(g, text):
    tokens = text.split()
    cmd = tokens[0].lower()

    if cmd == 'h':
        return help_buy()

    elif cmd == 'buy':
        try:
            location = tokens[1]
            buyid = tokens[2]
        except IndexError:
            return input_error_msg()

        print('need to implement')
        return

        if location == 'mon':
            return g.buy_mon(buyid)
        elif location == 'item':
            return g.buy_item(buyid)
        else:
            return input_error_msg()

    else:
        return input_error_msg()

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
        choice = input_loop(['y', 'n'], 'Are you sure? (y/n): ')

        if choice == 'y':
            ret['done'] = True
            return ret
        elif choice == 'n':
            return ret

    if g.get_state_num() == mystate.State.In_turn:
        process_buy(g, text)
        return ret

# Sets up a game and lets the user interact with it
def launch():
    g = mygame.Game()
    g.load_default()

    g.advance_turn()

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
