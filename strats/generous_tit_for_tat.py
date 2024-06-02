# Motive: Replicate the opponent/system's last move (cooperate/defect)
# However, be more generous.

import random


def decide(state):
    max_bet = state["max_bet"]
    call_value = state["call_value"]

    if call_value == 0 and state["round"] == 0:
        return "ch", -1
    elif call_value != 0:
        if random.randrange(0, 2) == 0:
            return "c", -1
        else:
            return "r", min(call_value * 2, max_bet)
    else:
        return "ch", -1
