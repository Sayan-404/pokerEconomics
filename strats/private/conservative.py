# Motive: Only play if the private value is really good

from ..utils import *


def decide(state):
    value = privateValue(state["player"]["hand"])

    if value > 9:
        return cooperativeMove(state)

    return "f", -1
