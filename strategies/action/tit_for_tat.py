# Motive: Replicate the opponent/system's last move (cooperate/defect)

from poker_metrics.utils import *


def decide(state):
    if systemResponse(state) == 0:
        return frugalMove(state)
    else:
        return prodigalMove(state)
