# Motive: Cooperate until opponent/system cooperates. If opponent/system defects, always defect.

from .utils import *


def decide(state):
    # Response 0 when cooperative environment and 1 otherwise
    response = 0

    sysRes = systemResponse(state)
    defMove = defectiveMove(state)
    cooMove = cooperativeMove(state)

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
