from itertools import combinations

def handStrength(hole, board):
    hand = hole+board

    ranks = "23456789TJQKA"
    suits = "scdh"
    deck = [r+s for r in ranks for s in suits]

    iDeck = convertToInts(deck)
    iHand = convertToInts(hand)
    iBoard = convertToInts(board)

    rank = getPattern(iHand)

    ahead = behind = tied = 0

    possibleHands = [iBoard + list(ioHole) for ioHole in combinations(iDeck, 2)]

    for ioHand in possibleHands:
        oRank = getPattern(ioHand)
        state = getState(rank, oRank)
        if state == -1:
            behind += 1
        elif state == 0:
            tied += 1
        else:
            ahead += 1

    return (ahead + tied/2)/(ahead + behind + tied/2)

def getState(rank, oRank):
    if rank[0] > oRank[0]:
        return 1
    elif rank[0] < oRank[0]:
        return -1
    else:
        if rank[1] > oRank[1]:
            return 1
        elif rank[1] < oRank[1]:
            return -1
        
        return 0

def getPattern(iHand):
    rHand = inRanks(iHand)
    sHand = inSuits(iHand)

    srHand = set(rHand)
    ssHand = set(sHand)

    n = len(srHand)
    rLenDiff = len(rHand) - n
    sLenDiff = len(sHand) - len(ssHand)

    # print(sHand)
    # print(ssHand)
    # print(len(sHand))
    # print(len(ssHand))
    # print(sLenDiff)
    # exit()

    rSum = sum(rHand)
    srSum = sum(srHand)

    sumDiff = rSum - srSum

    flush = ()
    if sLenDiff >= 4:
        # Case for flush
        flush = (3, rSum)
        # NOTE: rSum may not be an appropriate specific strength for flush

    # Confirming for straight
    for posStraight in list(combinations(rHand, 5)):
        # Basic logic is straight follows AP order
        # a is minimum term in posStraight
        # d is 1
        # n is 5
        # If sum of hands converted to integer ranks
        # And sum of AP is equal then its Straight
        s = sum(posStraight)
        sn = int((((2*min(posStraight)) + 4)*5)/2)

        if s == sn:
            if flush != ():
                # print(flush)
                # exit()
                # Case for straight flush
                return 0, s

            # Case for straight
            return 4, s

    if flush:
        return flush

    if rLenDiff == 1:
        # Case for pair
        # If difference is 1
        # That means 1 cards are out from set
        # Only pair is possible
        return 7, sumDiff
    
    if rLenDiff == 2:
        # If difference is 2
        # That means 2 cards are out from set
        # It could either be trips
        # Or it could be two pair

        if (sumDiff % 2) == 0:
            # Case for three of a kind
            # If diff % 2 == 0
            # Then 2 same cards were out
            # Thus its trips

            # Diff/2 gives the card that is out
            tripsHigh = int(sumDiff/2)

            if tripsHigh in rHand:
                return 5, tripsHigh
        
        # Case for two pair
        # If not trips then two pair
        return 6, sumDiff
    
    if 5 >= rLenDiff >= 3:
        # This is the case for quads and full houses
        # This bracket has been found empirically

        if rLenDiff == 5:
            # Definitely Quad
            # This is because diff can never be 5 for full houses
            # Again, it is emperically determined
            return 1, rSum
            # NOTE: Need to check if rSum appropriate or not

        if (sumDiff % 3) == 0:
            # Case for quad
            # Kind of cheated here
            # No maths actually
            # Sad ngl
            highRank, count = longSeq(rHand)
            if count == 4:
                return 1, highRank
        
        # Case for full house
        return 2, sumDiff
        
    return 8, rSum

def convertToInts(hand):
    ret_hand = []
    suitsInInt = {"s": 0, "c": 1, "d": 2, "h": 3}
    ranksInInt = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14
    }

    for card in hand:
        r = ranksInInt[card[0]]
        s = suitsInInt[card[1]]

        ret_hand.append(r*10 + s)

    return ret_hand

def inRanks(hand):
    return [round(card/10) for card in hand]

def inSuits(hand):
    return [card%10 for card in hand]

def longSeq(hand):
    counts = {}

    for card in hand:
        if card in counts.keys():
            counts[card] += 1
        else:
            counts[card] = 1

    maxRank = max(counts)

    return maxRank, counts[maxRank]  

if __name__ == "__main__":
    ioHands = [
            [23, 81, 92, 121, 144, 32, 52], #8
            [23, 81, 82, 121, 144, 53, 33], #7
            [23, 81, 82, 121, 144, 143, 33],    #6
            [23, 81, 72, 121, 144, 143, 142],   #5
            [23, 52, 31, 21, 42, 63, 71],   #4
            [23, 24, 84, 124, 144, 134, 34],    #3
            [23, 81, 82, 141, 144, 143, 33],  #2
            [23, 81, 82, 141, 144, 143, 142], #1
            [23, 54, 34, 24, 44, 64, 74], #0
        ]
    
    for ioHand in ioHands:
        analysis = getPattern(ioHand)

        print(analysis)

    # hole = ('4d', '8c')  
    # board = ('8s', 'Ac', 'Ad')
    # print(handStrength(hole, board))

    # print(longSeq([2, 8, 8, 14, 14, 14, 14]))
