from itertools import combinations

from poker_metrics.utils import get_rank_category

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

def hs(hole, board):
    hand = hole+board
    rank_cat = get_rank_category(hand)[0]

    ranks = "23456789TJQKA"
    suits = "scdh"
    deck = [r+s for r in ranks for s in suits]

    intDeck = set(convertToInts(deck))
    intHands = set(convertToInts(hole + board))

    intDeck = intDeck - intHands 

    rHands = inRanks(intHands)

    if (rank_cat == 8):
        pass

def pairs(intHand, intDeck, rankCat):
    pair_rank = 0

    if rankCat == 7:
        hand = inRanks(intHand)

        while True:
            if len(hand) == 0:
                raise Exception("Hand erroneously flagged as pair.")
            
            card = hand.pop()
            if card in hand:
                pair_rank = card
                break

    card_pairs = combinations(intDeck, 2)

    aheadPairs = 0
    tiedPairs = 0

    for pair in card_pairs:
        p = (round(pair[0]/10), round(pair[1]/10))

        if p[0] == p[1]:
            if p[0] > pair_rank:
                aheadPairs += 1
            elif p[0] == pair_rank:
                tiedPairs += 1

    return aheadPairs, tiedPairs

def twoPairs(intHand, rHands, intDeck, rankCat):
    primPairRank = 0
    kickPairRank = 0

    if rankCat

def trips(intHand, intDeck, rHands, rankCat):
    tripRank = 0

    if rankCat == 5:
        combos = combinations(rHands, 3)

        for cards in combos:
            if cards[0] == cards[1] == cards[2]:
                tripRank = cards[0]


    card_trips = combinations(intDeck, 3)

    aheadTrips = 0
    tiedTrips = 0

    for trips in card_trips:
        p = (round(trips[0]/10), round(trips[1]/10), round(trips[2]/10))

        if p[0] == p[1] == p[2]:
            if p[0] > tripRank:
                aheadTrips += 1
            elif p[0] == tripRank:
                tiedTrips += 1

    return aheadTrips, tiedTrips

def straights():
    pass

def flushes():
    pass

def fullHouses():
    pass

def quads(intHand, intDeck, rHands, rankCat):
    quad_rank = 0

    if rankCat == 1:
        combos = combinations(rHands, 4)

        for cards in combos:
            if cards[0] == cards[1] == cards[2] == cards[3]:
                quad_rank = cards[0]

    card_quads = combinations(intDeck, 4)

    aheadQuads = 0
    tiedQuads = 0

    for quad in card_quads:
        p = (round(quad[0]/10), round(quad[1]/10), round(quad[2]/10), round(quad[3]/10))

        if p[0] == p[1] == p[2]:
            if p[0] > quad_rank:
                aheadQuads += 1
            elif p[0] == quad_rank:
                tiedQuads += 1

    return aheadQuads, tiedQuads

def straightFlushes():
    pass