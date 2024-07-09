# Motive: Random Moves

import random

from poker_metrics.utils import availableMoves


def decide(state):
    # Removes the fold action from the available moves and return a random valid move
    valid_moves = availableMoves(state)

    valid_moves.remove(("f", -1))
    move = valid_moves[random.randrange(0, len(valid_moves))]

    return move
