# Motive: Cooperate until opponent/system cooperates. If opponent/system defects, always defect.

from poker_metrics.utils import *


def decide(state):
    # NOTE: This function has an encapsulated function to store data as memory
    # The data outside the move_decider does not change to their default values
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

        # Changes response to 1 is opponent's last action was raise/bet
        if sysRes:
            response = 1

        # If response is 0, return check/call
        # Else return raise/bet
        if response == 0:
            return cooMove
        else:
            return defMove

    return move_decider()
