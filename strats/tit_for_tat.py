# Motive: Replicate the opponent/system's last move (cooperate/defect)

from .utils import *


def decide(state):
    if systemResponse(state) == 0:
        return cooperativeMove(state)
    else:
        return defectiveMove(state)
