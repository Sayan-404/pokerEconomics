# Motive: Be flexible and defects with good hands else cooperate

from ...utils import *


def decide(state):
    value = publicValue(state["player"]["hand"])

    if state["round"] == 0:
        return cooperativeMove
    elif value > 5:
        return defectiveMove(state)

    return cooperativeMove(state)
