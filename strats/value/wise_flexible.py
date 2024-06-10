# Motive: Be flexible and defect aggressively with very good hands, cooperate with good hands else fold

from ..utils import *


def decide(state):
    value = privateValue(state["player"]["hand"])

    if value > 9:
        # Bet 10% of max_bet amount if very good hands
        return defectiveMove(state, 0.1 * state["max_bet"])
    elif value > 6:
        return cooperativeMove(state)

    return "f", -1
