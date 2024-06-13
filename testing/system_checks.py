"""
- see if every hand is zero sum
- see if every round is zero sum (total money in play - bankrolls - pot = 0)
- make a list of all possible legal transitions, and see if they are maintained
"""

import json as js


def chainValidate(rawActionChain, handNumber):
    actionChain = extractChain(rawActionChain, handNumber)
    debugPrint(actionChain, handNumber)
    actionsValidator(actionChain, handNumber)
    validator(actionChain, handNumber)


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
                    condition = (
                        priorAction in ["c", "ch", "a", "f"]
                        and presentActionData["call_size"] == 0
                    )
                    assert (
                        condition
                    ), "Player is not checking appropriately in {}".format(
                        presentActionData
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


def roundZeroSumValidator(actionChain, handNumber):
    pass


def validator(actionChain, handNumber):
    """
    Validates each specific items of each hands.
    """

    for i in range(len(actionChain)):
        # Pass if it is the first action of a game or the last winning action

        actionData = actionChain[i]

        # Pot validation

        condition = actionData["pot_after"] == (
            actionData["pot_before"]
            + (actionData["bet"] if (actionData["bet"] != -1) else 0)
            + (actionData["call_size"] if (actionData["action"] in ["c", "ch"]) else 0)
        )

        assert condition, "Pot value not appropriate in action: \n{}".format(actionData)


def actionAssert(presentAction, priorAction, legalPriorActions, playerId):

    condition = priorAction in legalPriorActions

    assert condition, "Player {} cannot {} when prior action is {}.".format(
        playerId, presentAction, priorAction
    )


def extractRoundChain(actionChain):
    rounds = []
    currentRound = -1
    for action in actionChain:
        roundNumber = action["round"]
        if roundNumber != currentRound:
            rounds.append([])
            currentRound = roundNumber
        rounds[-1].append(action)
    return rounds


def debugPrint(rawActionChain, handNumber):
    if rawActionChain:
        print(
            "\n\n\n\n-------------------------------For Debug-------------------------------\n\n\n\n",
            hand_number=handNumber,
        )

        prettyPrint(rawActionChain, handNumber)
        print("", hand_number=handNumber)


def prettyPrint(chain, handNumber):
    print(js.dumps(chain, indent=4), hand_number=handNumber)
