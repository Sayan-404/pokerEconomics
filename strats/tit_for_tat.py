# Motive: Replicate the opponent/system's last move (cooperate/defect)


def decide(state):
    call_value = state["call_value"]
    max_bet = state["max_bet"] + call_value

    if state["round"] == 0:
        if call_value == 0:
            return "ch", -1
        if call_value == 1:
            return "c", -1 
    if call_value != 0:
        return "r", min(call_value * 2, max_bet)
    else:
        return "c", -1
