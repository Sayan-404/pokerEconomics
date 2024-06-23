# Motive: Be flexible and defects with good hands else cooperate

from ...utils import *


def decide(state):
    value = privateValue(state["player"]["hand"])

    if state["round"] == 0:
        return frugalMove
    elif value > 5:
        return prodigalMove(state)

    return frugalMove(state)
