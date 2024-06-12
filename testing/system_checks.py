"""
- see if every hand is zero sum
- see if every round is zero sum (total money in play - bankrolls - pot = 0)
- make a list of all possible legal transitions, and see if they are maintained
"""


def chainValidate(rawActionChain, handNumber):
    actionChain = extractChain(rawActionChain, handNumber)
    debugPrint(rawActionChain, handNumber)
    actionsValidator(actionChain)


def extractChain(rawActionChain, handNumber):
    actionChain = []

    for actionData in rawActionChain:
        if actionData["hand_number"] == handNumber:
            actionChain.append(actionData)

    return actionChain


def actionsValidator(actionChain):
    pass


def debugPrint(rawActionChain, handNumber):
    if rawActionChain:
        print(
            "\n\n\n\n-------------------------------For Debug-------------------------------\n\n\n\n",
            hand_number=handNumber,
        )

        print(rawActionChain, hand_number=handNumber)
