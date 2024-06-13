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
    roundZeroSumValidator(rawActionChain, actionChain, handNumber)


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
                    legalPriorActions = ["b", "c", "r"]
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


def roundZeroSumValidator(rawActionChain, actionChain, handNumber):

    # Assumes both player have same bankroll
    if rawActionChain:
        player_1_bankroll = rawActionChain[0]["player_prev_bankroll"]
        player_2_bankroll = player_1_bankroll

        condition = (
            player_1_bankroll
            + player_2_bankroll
            - actionChain[-1]["pot_after"]
            - actionChain[-1]["player"]["bankroll"]
            - actionChain[-2]["player"]["bankroll"]
        )

        assert condition == 0, "Round zero sum validator (return {}) failed.".format(
            condition
        )

        print("Round is validated.", hand_number=handNumber)


def validator(actionChain, handNumber):
    """
    Validates each specific metrics of each hands.
    """

    for i in range(len(actionChain)):
        # Pass if it is the first action of a game or the last winning action

        actionData = actionChain[i]

        # Pot validation
        pot0SumCondition = actionData["pot_after"] - (
            actionData["pot_before"]
            + (actionData["bet"] if (actionData["bet"] != -1) else 0)
            + (actionData["call_size"] if (actionData["action"] in ["c", "ch"]) else 0)
        )

        assert (
            pot0SumCondition == 0
        ), "Pot zero sum condition (returned {}) failed in action: \n{}".format(
            pot0SumCondition, actionData
        )

        # Bankroll Validation
        bankroll0SumCondition = (
            actionData["player_prev_bankroll"]
            - actionData["player"]["bankroll"]
            - (
                actionData["bet"]
                if actionData["bet"] != -1
                else (actionData["call_size"] + blind(actionChain, actionData))
            )
        )

        assert (
            bankroll0SumCondition == 0
        ), "Bankroll zero sum condition (returned {}) failed in action: \n {}".format(
            bankroll0SumCondition, actionData
        )

        # Unstable and prolly not required
        # # Call size validation
        # if i - 1 >= 0:
        #     priorActionData = actionChain[i - 1]
        #     call0SumCondition = (
        #         (
        #             actionData["call_size"]
        #             + (
        #                 actionData["player"]["betamt"]
        #                 - (
        #                     priorActionData["bet"]
        #                     if priorActionData["bet"] != -1
        #                     else 0
        #                 )
        #             )
        #         )
        #         - (priorActionData["bet"] if priorActionData["bet"] != -1 else 0)
        #         - priorActionData["call_size"]
        #         - priorActionData["player"]["betamt"]
        #     )

        #     assert (
        #         call0SumCondition == 0
        #     ), "Call zero sum condition (returned {}) failed in action: \n {}".format(
        #         call0SumCondition, actionData
        #     )

    print("Pot and bankrolls validated successfully.", hand_number=handNumber)


def blind(actionChain, actionInObs):
    playerID = actionInObs["player"]["id"]
    for i in range(2):
        if actionChain[i] == actionInObs:
            if (
                actionChain[i]["round"] == 0
                and actionChain[i]["player"]["id"] == playerID
            ):
                if actionChain[i]["blind"]["bb"]["player"] == playerID:
                    return actionChain[i]["blind"]["bb"]["amt"]
                elif actionChain[i]["blind"]["sb"]["player"] == playerID:
                    return actionChain[i]["blind"]["sb"]["amt"]

    return 0


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
