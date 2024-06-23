# Motive: Replicate the opponent/system's last move (cooperate/defect)

from ..utils import *


def decide(state):
    if systemResponse(state) == 0:
        return frugalMove(state)
    else:
        return prodigalMove(state)
