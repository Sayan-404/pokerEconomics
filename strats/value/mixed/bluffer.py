from ...utils import *


def decide(state):
    private = privateValue(state["player"]["hand"])
    public = publicValue(state["player"]["hand"])

    if state["round"] == 0:
        return cooperativeMove(state)

    # Bluff
    if (publicValue - privateValue) >= 3:
        return defectiveMove(state)

    return cooperativeMove(state)
