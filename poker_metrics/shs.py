import os
import sys

sys.path.append(os.getcwd())

from hand_evaluator.evaluate_cards import evaluate_cards

def handStrength(hole, board):
    board_len = len(board)

    # Use Pre-Calculated values for faster performance
    # Flop = (52 - (3 + 2)) C 2 = 1081
    # Turn = (52 - (4 + 2)) C 2 = 1035
    # River = (52 - (5 + 2)) C 2 = 990
    total = 1081 if board_len == 3 else (1035 if board_len == 4 else (990 if board_len == 5 else 0))
    rank = evaluate_cards(hole + board)

    ahead = aheadInRank(hole, board, rank)
    tied = handsTied(hole, board, rank)

    return (ahead + tied/2)/total

def aheadInRank(hole, board, rank):
    """Returns the number of hands ahead in same hand rank"""

    ranks = "23456789TJQKA"
    suits = "scdh"
    deck = [r+s for r in ranks for s in suits]

    intDeck = set(convertToInts(deck))
    intHands = set(convertToInts(hole + board))

    intDeck = intDeck - intHands 

    rHands = inRanks(intHands)

    # High Card
    if (rank > 6185):
        # Get the maximum rank in hand
        highest = max(rHands)

        # Determine the possible higher ranks by subtracting from 14 (Ace)
        possible_higher_ranks = 14 - highest

        # There are 4 suits of each possible higher ranked card
        return possible_higher_ranks * 4

    # Pair
    if (rank > 3325):
        # Get the card rank of the pair
        pair_rank = 0
        hand = rHands

        while True:
            if len(hand) == 0:
                raise Exception("Hand erroneously flagged as pair.")
            
            card = hand.pop()
            if card in hand:
                pair_rank = card
                break

        # Determine the possible higher ranked pairs
        possible_higher_pairs = 14 - pair_rank

        # All higher ranked pairs have 4 suits of cards
        # Number of pairs formed by them = 4C2 = 6
        possible_higher_pairs *= 6

        return possible_higher_pairs
    
    # Two Pair
    if (rank > 2467):
        # Get the card rank of both pairs
        pair_ranks = []
        hand = rHands

        while True:
            if len(hand) == 0:
                raise Exception("Hand erroneously flagged as two pair.")
            card = hand.pop()
            if card in hand:
                pair_ranks.append(card)

            if len(pair_ranks) == 2:
                break

        ahead = 0

        # Determine the possible higher ranked primary pair
        primary_pair_rank = max(pair_ranks)

        ahead += (14 - primary_pair_rank)*6

        # Given that hero and villain have same kicker pair
        # Determine the possible higher ranked kicker pair
        kicker_pair_rank = min(pair_ranks)

        ahead += (14 - kicker_pair_rank)*6

        # Subtract the doubly counted higher ranked primary pairs
        # Along with primary rank of the pair also
        ahead -= (14 - primary_pair_rank)*6 - 6

        return ahead


    # Trips
    if (rank > 1609):
        # Get the card rank of trips
        quad_rank = 0
        hand = rHands

        while True:
            if len(hand) == 0:
                raise Exception("Hand erroneously flagged as trips.")
            
            card = hand.pop()

            if card in hand:
                quad_rank = card
                break

        # Determine the possible higher ranked trips
        possible_higher_quads = 14 - quad_rank

        # All higher ranked trips have 4 suits of cards
        # Number of trips formed by them = 4C3 = 4
        possible_higher_quads *= 4

        return possible_higher_quads
    
    # Straight
    if (rank > 1599):
        # TODO Update the method by considering the suits of cards as well
        # TODO This method under estimates the number of straights
        # Get the sequence of straight
        straight_seq = straight(rHands)

        # Get the highest ranked card of straight
        straight_high = max(straight_seq)

        # Get the number of higher highs of straight possible
        highs = 14 - straight_high

        return highs
    
    # Flush
    if (rank > 322):
        flush_seq = sorted(flush(intHands))

        flush_high = flush_seq[-1]

        # Number of higher highs of flush possible
        highs = 14 - round(flush_high/10)
        
        # Since no two player can have same highs in flush 
        # The following code is abandoned

        # Number of higher highs of flush possible when same high card sequentially
        # while True:
        #     if len(flush_seq == 0):
        #         break

        #     # Observes the last card
        #     # Determines cards above than that rank
        #     # Adds it to highs
        #     # Does it sequentially for considering the following scenario
        #     # "Both players have same high but not the same kicker and so on"
        #     card_in_obs = flush_seq.pop()
        #     highs += 14 - round(card_in_obs/10)

        return highs

    # Full House
    if (rank > 166):
        # Will be similar like trips
        # No two player can have the same trips
        # So only higher ranked trips are counted
        pos_rank = 0

        for i in range(len(hand)):
            if hand[i] - hand[i+1] == 0:
                # Trip rank confirmed
                if pos_rank == hand[i]:
                    return pos_rank
                
                pos_rank = hand[i]

        return 14 - pos_rank
    
    # Quads
    if (rank > 10):
        # Get the card rank of quads
        quad_rank = 0
        hand = rHands

        while True:
            if len(hand) == 0:
                raise Exception("Hand erroneously flagged as quads.")
            
            card = hand.pop()

            if card in hand:
                quad_rank = card
                break

        # Determine the possible higher ranked trips
        possible_higher_quads = 14 - quad_rank

        return possible_higher_quads

    # Straight Flush
    if (rank < 10):
        # Get the sequence of straight
        straight_seq = straight(rHands)

        # Get the highest ranked card of straight
        straight_high = max(straight_seq)

        # Get the number of higher highs of straight possible
        highs = 14 - straight_high

        return highs        

def aheadByRank(hole, board, rank):
    pass

def straight(nums):
    if len(nums) < 5:
        return []

    # Remove duplicates and sort the list
    nums = sorted(set(nums))

    longest_straight = []

    # Iterate through the list to find straight sequences of length 5
    for i in range(len(nums) - 4):
        # Check if the current window of 5 numbers forms a consecutive sequence
        if (nums[i + 4] - nums[i] == 4):
            current_straight = nums[i:i + 5]
            # Update the longest straight found so far
            longest_straight = current_straight

    return longest_straight

def flush(hand):
    seqs = {}

    for card in hand:
        if seqs[card%10]:
            seqs[card%10].append(card)
        else:
            seqs[card%10] = [card]

    for seq in seqs:
        if len(seq) == 5:
            return seq
        
    raise Exception("Hand erroneously flagged as flush.")

def handsTied(hole, board, rank):
    pass

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

if __name__ == "__main__":
    hole = ["Ah", "Ad"]
    board = ["2c", "3s", "7c"]
    intHands = convertToInts(hole + board)
    print(intHands)
    print(inRanks(intHands))