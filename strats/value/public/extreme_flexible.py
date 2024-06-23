# Motive: flexible strategy but defect even with bad hands

from ...utils import *


def decide(state):
    value = publicValue(state["player"]["hand"])

    if state["round"] == 0:
        return prodigalMove

    if value > 2:
        return prodigalMove(state)

    return frugalMove(state)
