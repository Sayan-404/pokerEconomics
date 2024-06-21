from itertools import combinations
from .math_utils import create_probabilistic_score
from phevaluator.evaluator import evaluate_cards
import numpy as np
import sys
import os

sys.path.append(os.getcwd())

# Include utilities for developing strategies


def systemResponse(state):
    """
    Analyse the response from the opponents/system.

    Returns 0 for cooperative and 1 for defective.
    """
    if state["call_value"] != 0 and state["round"] != 0:
        return 1

    return 0


# By default bet amount (betAmt) is set to 10 units
def defectiveMove(state, betAmt=10):
    """
    Returns the suitable defective move based on the current state of the game.
    """

    # Returns suitable defective move from the available moves

    if not canDefect(state):
        return cooperativeMove(state)

    moves = availableMoves(state, betAmt)

    for move in moves:
        if move[0] in ["r", "b"]:
            return move
        elif move[0] == "a":
            return move

    # Previous Implementation
    # callValue = state["call_value"]
    # bankroll = state["player"]["bankroll"]
    # maxBet = state["max_bet"]

    # move = []

    # if callValue != 0:
    #     if maxBet == 0:
    #         move = ["c", -1]
    #     else:
    #         move = ["r", min(callValue + betAmt, maxBet)]
    # elif callValue == 0:
    #     if state["round"] == 0:
    #         move = ["r", min(callValue + betAmt, maxBet)]
    #     else:
    #         move = ["b", min(callValue + betAmt, maxBet)]

    # if bankroll <= move[1]:
    #     move = ["a", -1]

    # return move


def cooperativeMove(state):
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

    # Previous Implementation
    # if state["call_value"] != 0:
    #     move = ("c", -1)
    # else:
    #     move = ("ch", -1)

    # if state["call_value"] >= state["player"]["bankroll"]:
    #     move = ("a", -1)

    # return move


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

        # If call_value is greater than bankroll, to be in the game, one has to go all in e>ither cooperative/defective ways
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


def privateValue(hole_cards, community_cards=[]):
    # returns a probability of roughly how good the hand is compared to other possible hands
    return create_probabilistic_score(hole_cards, community_cards)

def potential(hole_cards, community_cards):
    community_cards = set(community_cards)
    if len(community_cards) < 3:
        return -1 # only plausible post flop
    hole_cards = set(hole_cards)
    ranks = "23456789TJQKA"
    suits = "scdh"
    deck = set([r+s for r in ranks for s in suits])
    deck = deck - hole_cards
    deck = deck - community_cards
    future_board = list(combinations(deck, 1)) # only implements one card look-ahead
    opp_cards = list(combinations(deck, 2))
    w = {card: 1/len(opp_cards) for card in opp_cards}
    hp = np.zeros((3, 3))
    t = hole_cards | community_cards
    current_rank5 = evaluate_cards(*t)
    for cards in opp_cards:
        t = set(cards) | community_cards
        opp_rank = evaluate_cards(*t)
        if current_rank5 > opp_rank:
            index = 0
        elif current_rank5 == opp_rank:
            index = 1
        else:
            index = 2
        for future_cards in future_board:
            board = community_cards | set(future_cards)
            t = hole_cards | board
            current_rank6 = evaluate_cards(*t)
            t = set(cards) | board
            opp_rank = evaluate_cards(*t)
            if current_rank6 > opp_rank:
                hp[index][0] += w[cards]
            elif current_rank6 == opp_rank:
                hp[index][1] += w[cards]
            else:
                hp[index][2] += w[cards]
    hp_total = hp.sum(axis=0)
    print(hp)
    print(hp_total)
    ppot1 = (hp[2][0] + hp[2][1]/2 + hp[1][0]/2) / (hp_total[2] + hp_total[1]/2)
    npot1 = (hp[0][2] + hp[0][1]/2 + hp[1][2]/2) / (hp_total[0] + hp_total[1]/2)
    return ppot1, npot1