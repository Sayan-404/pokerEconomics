# Motive: flexible strategy but defect even with bad hands

from ..utils import *


def decide(state):
    value = privateValue(state["player"]["hand"])

    if value > 2:
        return defectiveMove(state)

    return cooperativeMove(state)
