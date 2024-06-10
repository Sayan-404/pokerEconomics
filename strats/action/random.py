# Motive: Random Moves

from ..utils import availableMoves
import random


def decide(state):
    valid_moves = availableMoves(state)

    move = valid_moves[random.randrange(0, len(valid_moves))]

    # if state["player"]["bankroll"] <= move[1]:
    #     move = ("a", -1)

    return move
