from itertools import combinations
import math

def process(cards):
    suits = [card[-1] for card in cards]
    ranks = [card[0] for card in cards]
    new_ranks = []
    for r in ranks:
        if r == "A":
            new_ranks.append(14)
        elif r == "K":
            new_ranks.append(13)
        elif r == "Q":
            new_ranks.append(12)
        elif r == "J":
            new_ranks.append(11)
        elif r == "T":
            new_ranks.append(10)
        else:
            new_ranks.append(r)
    unique_ranks = len(set(ranks))
    unique_suits = len(set(suits))
    rank_frequency = {r: ranks.count(r) for r in set(ranks)}
    repeated_ranks = sum(1 for r in rank_frequency.values() if r > 1)
    suit_frequency = {s: suits.count(s) for s in set(suits)}
    repeated_suits = sum(1 for s in suit_frequency.values() if s > 1)
    return {
        "suits": suits,
        "ranks": new_ranks,
        "unique_ranks": unique_ranks,
        "unique_suits": unique_suits,
        "repeated_ranks": repeated_ranks,
        "repeated_suits": repeated_suits,
        "rank_frequency": rank_frequency,
        "suit_frequency": suit_frequency,
        "remaining_cards": 7 - len(cards)
    }

def pair(cards):
    data = process(cards)
    if data["repeated_ranks"] >= 1:
        return 1.0
    else:
        return (data["unique_ranks"] * 3) / (52 - len(cards))
        # (number of cards with unique ranks * number of cards with same rank left) / total cards left in deck

def two_pair(cards):
    data = process(cards)
    if data["repeated_ranks"] >= 2:
        return 1.0
    elif data["repeated_ranks"] == 1:
        return (data["unique_ranks"] * 3) / (52 - len(cards))
        # (number of cards with unique ranks * number of cards with same rank left) / total cards left in deck
    elif data["remaining_cards"] == 2:
        return (math.comb(data["unique_ranks"], 2) * 3) / (52 - len(cards))
        # (number of two card combinations with unique ranks * number of cards with same rank left) / total cards left in deck
    else:
        return 0.0

def three_of_a_kind(cards):
    data = process(cards)
    if any(data["rank_frequency"][r] >=3 for r in data["rank_frequency"]):
        return 1.0
    else:
        two = 0
        for r in data["rank_frequency"]:
            if data["rank_frequency"][r] == 2:
                two += 1
        if data["remaining_cards"] == 2:
            return ((two*2) + (math.comb((len(data["unique_ranks"]) - two), 2)*3)) / (52 - len(cards))
            # two card combinations of non repeated cards * 3 / total cards in deck
        elif data["remaining_cards"] == 1:
            return (two*2) / (52 - len(cards))

def straight(cards):
    data = process(cards)
    rank = "23456789TJQKA"
    suit = "csdh"
    deck = [r+s for r in rank for s in suit]
    deck = [card for card in deck if card not in cards]
    def length(cards):
        data = process(cards)
        values = data["ranks"]
        if 14 in values:
            values.append(1)
        values = sorted(set(values))
        max_length = 1
        current_length = 1
        
        for i in range(1, len(values)):
            if values[i] == values[i - 1] + 1:
                current_length += 1
            else:
                max_length = max(max_length, current_length)
                current_length = 1
        return max_length
    if length(cards) >= 5:
        return 1.0
    if data["remaining_cards"] == 2:
        possible_cards = list(combinations(deck, 2))
        total = 0
        straights = 0
        for c in possible_cards:
            if length(c+cards) >= 5:
                straights += 1
            total += 1
        return straights / total
    elif data["remaining_cards"] == 1:
        possible_cards = list(combinations(deck, 1))
        total = 0
        straights = 0
        for c in possible_cards:
            if length(c+cards) >= 5:
                straights += 1
            total += 1
        return straights / total
    else:
        return 0.0

def flush(cards):
    data = process(cards)
    net_probability = 0.0
    for suit in data["suit_frequency"]:
        frequency = data["suit_frequency"][suit]
        if frequency >= 5:
            return 1.0
        if frequency == 4 and data["remaining_cards"] >= 1:
            net_probability += (13-4) / (52-len(cards))
        if frequency == 3 and data["remaining_cards"] == 2:
            net_probability += math.comb((13-3), 2) / math.comb(52 - len(cards), 2)
    return net_probability

def full_house(cards):
    data = process(cards)
    if 3 in data["rank_frequency"].values() and 2 in data["rank_frequency"].values():
        return 1.0
    if 3 in data["rank_frequency"].values():
        return ((data["unique_ranks"]-1)*12) / (52 - len(cards))
    if 2 in data["rank_frequency"].values():
        if data["repeated_ranks"] > 1:
            return ((13-2)*2) / (52 - len(cards))
        if data["repeated_ranks"] == 1 and data["remaining_cards"] == 2:
            return (math.comb(12, 2)*13) / (math.comb(52-len(cards), 2))
    return 0.0

def four_of_a_kind(cards):
    data = process(cards)
    if 4 in data["rank_frequency"].values():
        return 1
    if 3 in data["rank_frequency"].values():
        return 1 / (52 - len(cards))
    if data["remaining_cards"] == 2:
        if 2 in data["rank_frequency"].values():
            if data["repeated_ranks"] > 1:
                return 2 / (math.comb(52-len(cards), 2))
    return 0.0

def straight_flush(cards):
    data = process(cards)
    rank = "23456789TJQKA"
    suit = "csdh"
    deck = [r+s for r in rank for s in suit]
    deck = [card for card in deck if card not in cards]
    def length(cards):
        data = process(cards)
        values = data["ranks"]
        if 14 in values:
            values.append(1)
        values = sorted(set(values))
        max_length = 1
        current_length = 1
        
        for i in range(1, len(values)):
            if values[i] == values[i - 1] + 1:
                current_length += 1
            else:
                max_length = max(max_length, current_length)
                current_length = 1
        return max_length
    if length(cards) >= 5:
        return 1.0
    if data["remaining_cards"] == 2:
        possible_cards = list(combinations(deck, 2))
        total = 0
        straights = 0
        for c in possible_cards:
            if length(c+cards) >= 5:
                inter = process(c+cards)
                straights += 1
            total += 1
        return straights / total
    elif data["remaining_cards"] == 1:
        possible_cards = list(combinations(deck, 1))
        total = 0
        straights = 0
        for c in possible_cards:
            if length(c+cards) >= 5:
                straights += 1
            total += 1
        return straights / total
    else:
        return 0.0
    
def royal_flush(cards):
    data = process(cards)

def equity(hole_cards, community_cards):
    # call only on flop and turn
    cards = hole_cards + community_cards
    if len(cards) > 6 or len(cards) < 5:
        return -1
    return {
        "pair": pair(cards),
        "two_pair": two_pair(cards),
        "three_of_a_kind": three_of_a_kind(cards),
        "straight": straight(cards),
        "flush": flush(cards),
        "full_house": full_house(cards),
        "four_of_a_kind": four_of_a_kind(cards),
        "straight_flush": straight_flush(cards),
        "royal_flush": royal_flush(cards)
    }