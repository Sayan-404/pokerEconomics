# Motive: Replicate the opponent/system's last move (cooperate/defect)
# However, be more generous.

import random

from poker_metrics.utils import *


def decide(state):
    if systemResponse(state) == 0:
        return frugalMove(state)
    else:
        if random.randrange(0, 2) == 0:
            return frugalMove(state)
        else:
            return prodigalMove(state)
