def decide(state):
    if state["call_value"] != -1:
        return "r", state["call_value"] + 10
    else:
        return "b", 10
