def decide(state):
    call_value = state["call_value"]
    max_bet = state["max_bet"] + call_value
    if state["call_value"] != 0 or (state["call_value"] == 0 and state["round"] == 0):
        return "r", min(call_value + 10, max_bet)
    else:
        return "b", min(10, max_bet)
