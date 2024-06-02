# This strategy considers the EV by considering chip equity and then plays
# For now this works for heads up mainly


def decide(state):
    max_bet = state["max_bet"]

    total_bankroll = 0

    for player in state["players"]:
        total_bankroll += player.bankroll

    equity = state["player"]["bankroll"] / total_bankroll

    if equity > 0.4:
        return "a", -1
    else:
        return "f", -1
