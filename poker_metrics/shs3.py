from itertools import combinations

def handStrength(hole, board):
    hand = hole+board

    ranks = "23456789TJQKA"
    suits = "scdh"
    deck = [r+s for r in ranks for s in suits]

    iDeck = convertToInts(deck)
    iHand = convertToInts(hand)
    iBoard = convertToInts(board)

    pAnalysis = processHand(iHand)
    rank = getPattern(pAnalysis)

    ahead = behind = tied = 0

    possibleHands = [list(ioHole) for ioHole in combinations(iDeck, 2)]
    possibleHands = [iBoard + hole for hole in possibleHands]

    for ioHand in possibleHands:
        state = getState(iHand, pAnalysis, rank, ioHand)
        if state == -1:
            behind += 1
        elif state == 0:
            tied += 1
        else:
            ahead += 1

    return (ahead + tied/2)/(ahead + behind + tied/2)

def getState(iHand, pAnalysis, rank, ioHand):
    ioAnalysis = processHand(ioHand)
    pattern = getPattern(ioAnalysis)
    
    if rank < pattern:
        return -1
    elif rank > pattern:
        return 1
    else:
        if rank == pattern == 8:
            oHand = counting_sort(inRanks(ioHand), 14)
            pHand = counting_sort(inRanks(iHand), 14)

            if (pHand < oHand):
                return -1
            elif (pHand > oHand):
                return 1
            else:
                return 0
            
        if rank == pattern == 7:
            if pAnalysis[0][-1][0] < ioAnalysis[0][-1][0]:
                return -1
            elif pAnalysis[0][-1][0] > ioAnalysis[0][-1][0]:
                return  1
            else:
                return 0
            
        if rank == pattern == 6:
            if pAnalysis[0][-1][0] < ioAnalysis[0][-1][0]:
                return -1
            elif pAnalysis[0][-1][0] > ioAnalysis[0][-1][0]:
                return  1
            else:
                if pAnalysis[0][-2][0] < ioAnalysis[0][-2][0]:
                    return -1
                elif pAnalysis[0][-2][0] > ioAnalysis[0][-2][0]:
                    return  1
                else:
                    return 0      
                
        if rank == pattern == 5:
            if pAnalysis[0][-1][0] < ioAnalysis[0][-1][0]:
                return -1
            else:
                return  1
            
        if rank == pattern == 4:
            if (pAnalysis[-1] < ioAnalysis[-1]):
                return -1
            elif (pAnalysis[-1] > ioAnalysis[-1]):
                return 1
            else:
                return 0
            
        if rank == pattern == 3:
            oHand = counting_sort(inRanks(ioHand), 14)
            pHand = counting_sort(inRanks(iHand), 14)

            if (pHand < oHand):
                return -1
            elif (pHand > oHand):
                return 1
            else:
                return 0

        if rank == pattern == 2:
            if pAnalysis[0][-1][0] < ioAnalysis[0][-1][0]:
                return -1
            elif pAnalysis[0][-1][0] > ioAnalysis[0][-1][0]:
                return  1
            else:
                if pAnalysis[0][-2][0] < ioAnalysis[0][-2][0]:
                    return -1
                elif pAnalysis[0][-2][0] > ioAnalysis[0][-2][0]:
                    return  1
                else:
                    return 0   

        if rank == pattern == 1:
            if pAnalysis[0][-1][0] < ioAnalysis[0][-1][0]:
                return -1
            elif pAnalysis[0][-1][0] > ioAnalysis[0][-1][0]:
                return  1
            else:
                return 0
        
        if rank == pattern == 0:
            if (pAnalysis[-1] < ioAnalysis[-1]):
                return -1
            elif (pAnalysis[-1] > ioAnalysis[-1]):
                return 1
            else:
                return 0
        
def getPattern(analysis):
    sequences, flush, straight = analysis

    
    # Handle the cases of straight and flushes
    if straight:
        if flush:
            return 0
        return 4
    
    if flush:
        return 3
    
    sequences = sorted(sequences)

    if len(sequences) >= 2:
        max_seq = len(sequences[-1])

        if max_seq == 3:
            return 2
        
        if max_seq == 2:
            return 6
    elif len(sequences) == 1:
        if len(sequences[0]) == 4:
            return 1
        elif len(sequences[0]) == 3:
            return 5
        else:
            return 7
        
    return 8

def processHand(ioHand):
    Sorted_io_hand = counting_sort(ioHand, 144)

    seqs = []
    tempSeq = []

    straights = []
    tempStraights = []

    flushes = []
    tempFlushes = []
    
    for iCard in Sorted_io_hand:
        rCard = round(iCard / 10)
        sCard = iCard % 10

        # Arranging to sequences
        if len(tempSeq) == 0:
            tempSeq = [rCard]
        elif len(tempSeq) > 0 and rCard == tempSeq[-1]:
            pass


        # Arranging to Straights
        if len(tempStraights) == 0 or (tempStraights[-1] - rCard) == -1:
            tempStraights.append(rCard)
            continue
        else:
            straights.append(tempStraights)
            tempStraights = [rCard]

        # Arranging to Flushes
        if len(tempFlushes) == 0:
            tempFlushes.append(sCard)
            continue
        elif tempFlushes[-1] == sCard:
            flushes.append(tempFlushes)
            tempFlushes = [sCard]
            continue

    if tempSeq:
        seqs.append(tempSeq)
    if tempStraights:
        straights.append(tempStraights)
    if tempFlushes:
        flushes.append(tempFlushes)

    # Filtering sequences
    seqs = [seq for seq in seqs if len(seq) > 1]

    # Filtering straights
    straights = [st for st in straights if len(st) == 5]

    # Filtering flushes
    flushes = [fl for fl in flushes if len(fl) == 5]
    
    # Sort sequences
    seqs = sorted(seqs)
    
    # Since only one straight and flush is required in the return,
    # we will return the first one found or an empty list if none are 
    straight = straights[0] if straights else []
    flush = flushes[0] if flushes else []
    
    return seqs, flush, straights

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

# Time Complexity: O(N + max_value)
def counting_sort(arr, max_value):
    count = [0] * (max_value + 1)
    output = [0] * len(arr)

    # Count the occurrences of each number
    for num in arr:
        count[num] += 1

    # Compute the cumulative count
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # Place the elements in the output array in sorted order
    for num in reversed(arr):
        output[count[num] - 1] = num
        count[num] -= 1

    return output


if __name__ == "__main__":
    ioHands = [
            # [23, 81, 92, 121, 144, 32, 52], #8
            # [23, 81, 82, 121, 144, 53, 33], #7
            # [23, 81, 82, 121, 144, 143, 33],    #6
            # [23, 81, 72, 121, 144, 143, 142],   #5
            # [23, 52, 31, 21, 42, 63, 71],   #4
            [23, 24, 84, 124, 144, 134, 34],    #3
            [23, 81, 82, 141, 144, 143, 33],
            [23, 81, 82, 141, 144, 143, 142],
            [23, 54, 34, 24, 44, 64, 74],
        ]
    
    for ioHand in ioHands:
        print()
        analysis = processHand(ioHand)

        print(processHand(ioHand))
        print(getPattern(analysis))

    # hole = ('4d', '8c')  
    # board = ('8s', 'Ac', 'Ad')
    # print(handStrength(hole, board))
