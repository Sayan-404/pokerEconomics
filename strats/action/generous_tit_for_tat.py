# Motive: Replicate the opponent/system's last move (cooperate/defect)
# However, be more generous.

import random
from ..utils import *


def decide(state):
    if systemResponse(state) == 0:
        return cooperativeMove(state)
    else:
        if random.randrange(0, 2) == 0:
            return cooperativeMove(state)
        else:
            return defectiveMove(state)
