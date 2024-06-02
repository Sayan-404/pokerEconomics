def decide(state):
    if state["call_value"] != 0:
        return "c", -1
    else:
        return "ch", -1
