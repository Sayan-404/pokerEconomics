# Motive: Be flexible and defects with good hands else cooperate

from ..utils import *


def decide(state):
    value = privateValue(state["player"]["hand"])

    if value > 5:
        return defectiveMove(state)

    return cooperativeMove(state)
