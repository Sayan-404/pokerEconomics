def decide(state):
    max_bet = state["max_bet"]
    if state["call_value"] != 0:
        return "r", min(state["call_value"] + 10, max_bet)
    else:
        return "b", min(10, max_bet)
