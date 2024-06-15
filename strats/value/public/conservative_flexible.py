# Motive: Be flexible and defects with good hands else fold

from ...utils import *


def decide(state):
    value = publicValue(state["player"]["hand"])

    if state["round"] == 0:
        return cooperativeMove
    elif value > 8:
        return cooperativeMove(state)

    return "f", -1
