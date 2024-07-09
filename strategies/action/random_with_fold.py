# Motive: Random Moves

import random

from poker_metrics.utils import availableMoves


def decide(state):
    # Makes a random move between the available valid moves
    valid_moves = availableMoves(state)

    move = valid_moves[random.randrange(0, len(valid_moves))]

    return move
