# Motive: Random Moves

import random

from poker_metrics.utils import availableMoves


def decide(state):
    valid_moves = availableMoves(state)

    valid_moves.remove(("f", -1))
    move = valid_moves[random.randrange(0, len(valid_moves))]

    return move
