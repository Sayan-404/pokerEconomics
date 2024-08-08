from itertools import combinations
from collections import Counter

from utils import get_rank_category

def handStrength(hole, board):
    hand = hole+board
    rank = get_rank_category(hand)[0]

    ranks = "23456789TJQKA"
    suits = "scdh"
    deck = [r+s for r in ranks for s in suits]

    intDeck = set(convertToInts(deck))
    intBoard = set(convertToInts(board))
    intHand = set(convertToInts(hole + board))

    intDeck = intDeck - intHand 

    rHand = inRanks(intHand)

    ahead = 0
    tied = 0
    behind = 0

    possible_hands = [intBoard | set(hole) for hole in combinations(intDeck, 2)]

    for hand in possible_hands:
        state = getState(rHand, hand, rank, intHand)
        if state == -1:
            behind += 1
        if state == 0:
            tied += 1
        if state == 1:
            ahead += 1

    return (ahead + tied/2)/(ahead + behind + tied/2)

def getState(phand, hand, rank, intHand):
    pattern = getPattern(hand)
    rhand = sorted(inRanks(hand))

    if pattern > rank:
        return 1
    elif pattern < rank:
        return -1
    elif pattern == rank:
        if rank == 8:
            return getHigher(phand, rhand)

        if rank == 7:
            # Consider only the highest pair formed
            p_pair_seq = sorted(seqs(phand))[-1]
            pair_seq = sorted(seqs(rhand))[-1]

            if p_pair_seq[0] > pair_seq[0]:
                return 1
            elif p_pair_seq[0] < pair_seq[0]:
                return -1
            else:
                mod_phand = set(phand) - set(p_pair_seq)
                mod_rhand = set(rhand) - set(p_pair_seq)

                return getHigher(mod_phand, mod_rhand)             

        if rank == 6:
            p_seqs = sorted(seqs(phand))
            h_seqs = sorted(seqs(rhand))

            if p_seqs[1][0] > h_seqs[1][0]:
                return 1
            elif p_seqs[1][0] < h_seqs[1][0]:
                return -1
            else:
                if p_seqs[0][0] > h_seqs[0][0]:
                    return 1
                elif p_seqs[0][0] < h_seqs[0][0]:
                    return -1
                else:
                    mod_phand = set(phand) - set(p_seqs[0]) - set(p_seqs[1])
                    mod_rhand = set(rhand) - set(p_seqs[0]) - set(p_seqs[1])

                    return getHigher(mod_phand, mod_rhand)    
        
        if rank == 5:
            # Consider only the highest trip formed
            p_trip_seq = sorted(seqs(phand))[-1]
            trip_seq = sorted(seqs(rhand))[-1]

            if p_trip_seq[0] > trip_seq[0]:
                return 1
            elif p_trip_seq[0] < trip_seq[0]:
                return -1
            else:
                return 0
            
        if rank == 4:
            p_straight = straight(phand)
            r_straight = straight(rhand)

            return getHigher(p_straight, r_straight)
        
        if rank == 3:
            return getHigher(phand, rhand)
        
        if rank == 2:
            # Consider only the highest trip formed
            p_fh_seq = sorted(seqs(phand))[-1]
            fh_seq = sorted(seqs(rhand))[-1]

            if p_fh_seq[0] > fh_seq[0]:
                return 1
            elif p_fh_seq[0] < fh_seq[0]:
                return -1
            else:
                return 0
            
        if rank == 1:
            # Consider only the highest quad formed (obv 1 quad)
            p_q_seq = sorted(seqs(phand))[-1]
            q_seq = sorted(seqs(rhand))[-1]

            if p_q_seq[0] > q_seq[0]:
                return 1
            else:
                return -1
            
        if rank == 0:
            p_straight = straight(phand)
            r_straight = straight(rhand)

            return getHigher(p_straight, r_straight)

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


def getHigher(phand, rhand):
    p_hand = sorted(set(phand))
    r_hand = sorted(set(rhand))

    if max(p_hand) == max(r_hand):
        p_hand.pop()
        r_hand.pop()

        if len(p_hand) == 0 or len(r_hand) == 0:
            return 0
        
        getHigher(p_hand, r_hand)
    
    else:
        if p_hand[-1] > r_hand[-1]:
            return 1
        else:
            return -1
    
def getPattern(hand):
    hand = sorted(set(hand))
    rhand = sorted(inRanks(hand))

    # Handle the cases of straight and flushes
    straight = isStraight(rhand)
    flush = isFlush(hand)
    if straight:
        if flush:
            return 0
        return 4
    
    if flush:
        return 3
    
    # Handle the cases of pairs, trips and quads
    sequences = seqs(rhand)

    if sequences is None:
        return 8
    
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
    
def seqs(nums):
    if not nums:
        return []

    # Count the occurrences of each number
    counts = Counter(nums)
    
    # Build the sequences based on counts greater than 1
    sequences = [[num] * count for num, count in counts.items() if count > 1]
    
    return sequences if sequences else None

def isStraight(nums):
    if len(nums) < 5:
        return None

    # Remove duplicates and sort the list
    nums = sorted(set(nums))

    # Iterate through the list to find straight sequences of length 5
    for i in range(len(nums) - 4):
        # Check if the current window of 5 numbers forms a consecutive sequence
        if (nums[i + 4] - nums[i] == 4) and (nums[i + 1] == nums[i] + 1) and (nums[i + 2] == nums[i] + 2) and (nums[i + 3] == nums[i] + 3):
            return nums[i:i + 5]

    return None

def isFlush(hand):
    seqs = {}

    for card in hand:
        suit = card % 10
        if suit in seqs:
            seqs[suit].append(card)
        else:
            seqs[suit] = [card]

    for seq in seqs.values():
        if len(seq) == 5:
            return seq
        
    return None


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
    hole = ('3s', '6s') 
    board = ('6h', '8c', '9d')
    print(handStrength(hole, board))

    # print(seqs([2, 2, 2, 2, 5, 5, 3, 3, 7]))