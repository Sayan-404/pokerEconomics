from ...utils import *


def decide(state):
    private = privateValue(state["player"]["hand"])
    public = publicValue(state["player"]["hand"])

    if state["round"] == 0:
        return frugalMove(state)

    # Bluff
    if (public - private) >= 3:
        return prodigalMove(state)

    return frugalMove(state)
