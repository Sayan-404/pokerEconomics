"""
- see if every hand is zero sum
- see if every round is zero sum (total money in play - bankrolls - pot = 0)
- make a list of all possible legal transitions, and see if they are maintained
"""


def chainValidate(rawActionChain, handNumber):
    actionChain = extractChain(rawActionChain, handNumber)
    debugPrint(rawActionChain, handNumber)
    actionsValidator(actionChain, handNumber)


def extractChain(rawActionChain, handNumber):
    actionChain = []

    for actionData in rawActionChain:
        if actionData["hand_number"] == handNumber:
            actionChain.append(actionData)

    return actionChain


def actionsValidator(actionChain, handNumber):
    """
    Validates all the actions taken in a hand.
    """

    for i in range(len(actionChain)):

        # Validate the first action (Can only call, raise, all-in, or fold)
        if i == 0:
            action = actionChain[i]["action"]
            playerId = actionChain[i]["player"]["id"]
            condition = (
                (action == "c") or (action == "r") or (action == "a") or (action == "f")
            )

            assert (
                condition
            ), f"Player {playerId} made an invalid move {action} on first move."
        else:
            priorActionData = actionChain[i - 1]
            presentActionData = actionChain[i]

            presentPlayer = presentActionData["player"]

            action = presentActionData["action"]
            priorAction = priorActionData["action"]

            if priorActionData["round"] == presentActionData["round"]:

                if action == "c":
                    legalPriorActions = ["r", "b", "c", "a"]
                    actionAssert(
                        action, priorAction, legalPriorActions, presentPlayer["id"]
                    )

                elif action == "ch":
                    legalPriorActions = ["ch", "a"]
                    actionAssert(
                        action, priorAction, legalPriorActions, presentPlayer["id"]
                    )

                elif action == "r":
                    legalPriorActions = ["b", "c"]
                    actionAssert(
                        action, priorAction, legalPriorActions, presentPlayer["id"]
                    )

                elif action == "b":
                    legalPriorActions = ["ch"]
                    actionAssert(
                        action, priorAction, legalPriorActions, presentPlayer["id"]
                    )
            else:
                # This is when it is the first hand of a specific round
                legalActions = ["b", "ch", "a", "f"]
                assert (
                    action in legalActions
                ), "Player {} cannot {} in first action of a round.".format(
                    presentPlayer["id"], action
                )

    print("Actions have been validated successfully.", hand_number=handNumber)


def actionAssert(presentAction, priorAction, legalPriorActions, playerId):

    condition = priorAction in legalPriorActions

    assert condition, "Player {} cannot {} when prior action is {}.".format(
        playerId, presentAction, priorAction
    )


def debugPrint(rawActionChain, handNumber):
    if rawActionChain:
        print(
            "\n\n\n\n-------------------------------For Debug-------------------------------\n\n\n\n",
            hand_number=handNumber,
        )

        print(rawActionChain, hand_number=handNumber)
        print("", hand_number=handNumber)
