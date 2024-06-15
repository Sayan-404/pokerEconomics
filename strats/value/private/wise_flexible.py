# Motive: Be flexible and defect aggressively with very good hands, cooperate with good hands else fold

from ...utils import *


def decide(state):
    value = privateValue(state["player"]["hand"])

    if state["round"] == 0 and value > 9:
        # Bet 20% of max_bet amount if very good hands
        return defectiveMove(state, 0.2 * state["max_bet"])
    elif state["round"] == 0:
        return cooperativeMove()
    elif value > 6:
        return cooperativeMove(state)

    return "f", -1
