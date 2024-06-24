from .math_utils import create_probabilistic_score
from .hand_potential import potential
import sys
import os

sys.path.append(os.getcwd())

# Include utilities for developing strategies

# Pre-defined variables
IR2 = [
    [7, -351, -334, -314, -318, -308, -264, -217, -166, -113, -53, 10, 98],
    [-279, 74, -296, -274, -277, -267, -251, -201, -148, -93, -35, 27, 116],
    [-263, -225, 142, -236, -240, -231, -209, -185, -130, -75, -17, 46, 134],
    [-244, -206, -169, 207, -201, -189, -169, -148, -114, -55, 2, 68, 153],
    [-247, -208, -171, -138, 264, -153, -134, -108, -78, -43, 19, 85, 154],
    [-236, -200, -162, -125, -91, 324, -99, -72, -43, -6, 37, 104, 176],
    [-192, -182, -143, -108, -74, -43, 384, -39, -4, 29, 72, 120, 192],
    [-152, -134, -122, -84, -50, -17, 16, 440, 28, 65, 106, 155, 215],
    [-104, -86, -69, -56, -19, 12, 47, 81, 499, 102, 146, 195, 254],
    [-52, -35, -19, 0, 11, 46, 79, 113, 149, 549, 161, 212, 271],
    [2, 21, 34, 55, 72, 86, 121, 153, 188, 204, 598, 228, 289],
    [63, 79, 98, 116, 132, 151, 168, 200, 235, 249, 268, 647, 305],
    [146, 164, 180, 198, 198, 220, 240, 257, 291, 305, 323, 339, 704]
]

cardTypes = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


def systemResponse(state):
    """
    Analyse the response from the opponents/system. This function is only suitable for heads-up.

    Returns 0 for cooperative and 1 for defective.
    """
    if state["call_value"] != 0 and state["round"] != 0:
        return 1

    # Handles pre-flop's special cases
    if state["round"] == 0:
        blindType = ""
        blind = 0

        if state["player"]["id"] == state["blinds"]["bb"]["player"]:
            blind = state["blinds"]["bb"]["amt"]
            blindType = "bb"
        elif state["player"]["id"] == state["blinds"]["sb"]["player"]:
            blind = state["blinds"]["sb"]["amt"]
            blindType = "sb"

        if (blindType == "sb") and ((state["call_value"] - blind) != 0):
            return 1
        elif (blindType == "bb") and ((state["call_value"] - blind) != (-blind)):
            return 1

    return 0


# By default bet amount (betAmt) is set to 10 units
def prodigalMove(state, betAmt=10):
    """
    Returns the suitable defective move based on the current state of the game.
    """

    # Returns suitable defective move from the available moves

    if not canDefect(state):
        return frugalMove(state)

    moves = availableMoves(state, betAmt)

    for move in moves:
        if move[0] in ["r", "b"]:
            return move
        elif move[0] == "a":
            return move


def frugalMove(state):
    """
    Returns the suitable cooperative move based on the current state of the game.
    """

    # Returns suitable cooperative move from available moves

    moves = availableMoves(state)

    for move in moves:
        if move[0] in ["c", "ch"]:
            return move
        elif move[0] == "a":
            return move


def availableMoves(state, betamt=10):
    """
    Returns a list of available moves based on the current state of the game.
    """
    effective_max_bet = min(betamt, state["max_bet"])
    call_value = state["call_value"]

    valid_moves = []

    if call_value == 0 and state["round"] == 0:
        # In the round 0, if call_value is 0 and regardless of the blinds
        # One can raise, check or fold
        valid_moves = [("r", call_value + effective_max_bet),
                       ("ch", -1), ("f", -1)]

        # (fixDefection) Still accounting for a corner case of bankroll being lesser than or equal to call_value

    elif call_value > 0:
        # If call_value is not equal to 0, one can call, raise or fold
        valid_moves = [("c", -1), ("r", call_value +
                                   effective_max_bet), ("f", -1)]

        # If call_value is greater than bankroll, to be in the game, one has to go all in either cooperative/defective ways
        if call_value >= state["player"]["bankroll"]:
            valid_moves = [("a", -1), ("f", -1)]

        # (fixDefection) If raise amount is greater than bankroll, one has to go all in

    elif call_value <= 0:
        valid_moves = [("ch", -1), ("b", call_value +
                                    effective_max_bet), ("f", -1)]

        # (fixDefection) If bet amount is greater than bankroll, one has to go all in

    valid_moves = fixDefection(valid_moves, state)

    return valid_moves


def fixDefection(moves, state):
    # Finds a defective move and fix it if required
    return_moves = []
    for i in range(len(moves)):
        move = moves[i]

        if move[1] >= state["player"]["bankroll"]:
            move = ("a", -1)

        return_moves.append(move)

    return return_moves


def canDefect(state):
    return_value = False

    for player in state["players"]:
        if player.id != state["player"]["id"]:
            if player.ingame == 1:
                if player.bankroll > 0:
                    return_value = True
                    break

    return return_value


def privateValue(deck, hole_cards, community_cards=[]):
    # returns a probability of roughly how good the hand is compared to other possible hands
    return create_probabilistic_score(deck, hole_cards, community_cards)


def potentialPrivateValue(deck, hole_cards, community_cards):
    return potential(deck, hole_cards, community_cards)


def ir(holeCards):
    # Lowest: -351
    # Highest: 704

    first = cardTypes.index(holeCards[0][0])
    second = cardTypes.index(holeCards[1][0])

    return IR2[first][second]
