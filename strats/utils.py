# Include utilities for developing strategies


def systemResponse(state):
    """
    Analyse the response from the opponents/system.

    Returns 0 for cooperative and 1 for defective.
    """
    if state["call_value"] != 0:
        return 1

    return 0


def defectiveMove(
    state, betAmt=10
):  # By default bet amount (betAmt) is set to 10 units
    """
    Returns the suitable defective move based on the current state of the game.
    """

    callValue = state["call_value"]
    bankroll = state["player"]["bankroll"]
    maxBet = state["max_bet"]

    move = []

    if callValue != 0:
        if maxBet == 0:
            move = ["c", -1]
        else:
            move = ["r", min(callValue + betAmt, maxBet)]
    elif callValue == 0:
        if state["round"] == 0:
            move = ["r", min(callValue + betAmt, maxBet)]
        else:
            move = ["b", min(callValue + betAmt, maxBet)]

    if bankroll <= move[1]:
        move = ["a", -1]

    return move


def cooperativeMove(state):
    """
    Returns the suitable cooperative move based on the current state of the game.
    """

    callValue = state["call_value"]
    bankroll = state["player"]["bankroll"]

    if callValue != 0:
        return "c", -1

    return "ch", -1


def availableMoves(state):
    """
    Returns a list of available moves based on the current state of the game.
    """
    max_bet = state["max_bet"]
    call_value = state["call_value"]

    valid_moves = []

    if call_value == 0 and state["round"] == 0:
        valid_moves = [("r", min(call_value + 10, max_bet)), ("ch", -1), ("f", -1)]
    elif call_value != 0:
        valid_moves = [("c", -1), ("r", min(call_value + 10, max_bet)), ("f", -1)]
    else:
        valid_moves = [("ch", -1), ("b", min(call_value + 10, max_bet)), ("f", -1)]

    return valid_moves
