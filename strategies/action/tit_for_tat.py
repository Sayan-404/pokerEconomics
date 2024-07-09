# Motive: Replicate the opponent/system's last move (cooperate/defect)

from poker_metrics.utils import *


def decide(state):
    # If opponent's last move was check/call
    if systemResponse(state) == 0:
        return frugalMove(state)
    else:
        # If opponent's last move was raise/bet
        return prodigalMove(state)
