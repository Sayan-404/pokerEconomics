# Motive: Cooperate until opponent/system cooperates. If opponent/system defects, always defect.

from poker_metrics.utils import *


def decide(state):
    # Response 0 when cooperative environment and 1 otherwise
    response = 0

    sysRes = systemResponse(state)
    defMove = prodigalMove(state)
    cooMove = frugalMove(state)

    def move_decider():
        nonlocal response
        nonlocal sysRes
        nonlocal defMove
        nonlocal cooMove

        if sysRes:
            response = 1

        if response == 0:
            return cooMove
        else:
            return defMove

    return move_decider()
