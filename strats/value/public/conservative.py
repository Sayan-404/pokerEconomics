# Motive: Only play if the private value is really good

from ...utils import *


def decide(state):
    value = publicValue(state["player"]["hand"])

    if value > 9:
        return frugalMove(state)

    return "f", -1
