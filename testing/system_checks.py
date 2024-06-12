def chainValidate(rawActionChain, handNumber):
    actionChain = extractChain(rawActionChain, handNumber)
    actionsValidate(actionChain, handNumber)

    debugPrint(rawActionChain, handNumber)


def extractChain(rawActionChain, handNumber):
    actionChain = []

    for actionData in rawActionChain:
        if actionData["hand_number"] == handNumber:
            actionChain.append(actionData)

    return actionChain


def actionsValidate(actionChain, handNumber):
    for i in range(len(actionChain)):
        action = actionChain[i]["action"]

        if i == 0:
            assert (action == "c") or (
                action == "r"
            ), f"Player made an invalid move on first bet."
        else:
            if actionChain[i]["round"] == actionChain[i - 1]["round"]:
                before = actionChain[i - 1]["action"]
                callValue = actionChain[i]["call_size"]

                if action == "ch":
                    assert (
                        callValue == 0
                    ), f"Player checked when call value is {callValue}."
                    assert before == "ch", f"Player checked after {before}."

                # if action == "c":
                #     assert (
                #         callValue != 0
                #     ), f"Player cannot call when call value is not equal to 0."

                #     if len(actionChain[i]["players"]) == 2:
                #         assert (before == "r") or (
                #             before == "b"
                #         ), f"Player cannot call when opponent has not raised or bet."

                # if action == "r":
                #     assert (
                #         callValue > 0
                #     ), f"Player cannot raise when call value is equal to 0."
                #     assert (before == "c") or (
                #         before == "b"
                #     ), f"Player cannot raise if no one called or bet more."


def debugPrint(rawActionChain, handNumber):
    print(
        "\n\n\n\n---------------------------------------------------------------------------------\n\n\n\n",
        hand_number=handNumber,
    )
    print(rawActionChain, hand_number=handNumber)
