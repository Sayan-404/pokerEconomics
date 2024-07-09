# Motive: Replicate the opponent/system's last move (cooperate/defect)
# However, be generous by pardoning some of opponent's raises randomly

import random

from poker_metrics.utils import *


def decide(state):
    # Checks whether opponent has raised or not

    # If opponent called/checked return check/call
    if systemResponse(state) == 0:
        return frugalMove(state)
    else:
        # Opponent raised
        # Randomly return a check/call or bet/raise
        return random.choice([frugalMove(state), prodigalMove(state)])
