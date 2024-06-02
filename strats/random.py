# Motive: Random Moves

import random


def decide(state):
    max_bet = state["max_bet"]
    call_value = state["call_value"]

    valid_moves = []

    if call_value == 0 and state["round"] == 0:
        valid_moves = [("r", min(call_value + 10, max_bet)), ("ch", -1)]
    elif call_value != 0:
        valid_moves = [("c", -1), ("r", min(call_value + 10, max_bet))]
    else:
        valid_moves = [("ch", -1), ("b", min(call_value + 10, max_bet))]

    return valid_moves[random.randrange(0, len(valid_moves) + 1)]
