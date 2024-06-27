from itertools import combinations
import math

def process(cards):
    new_cards = []
    for c in cards:
        if c[0] == "A":
            new_cards.append(f"14{c[-1]}")
        elif c[0] == "K":
            new_cards.append(f"13{c[-1]}")
        elif c[0] == "Q":
            new_cards.append(f"12{c[-1]}")
        elif c[0] == "J":
            new_cards.append(f"11{c[-1]}")
        elif c[0] == "T":
            new_cards.append(f"10{c[-1]}")
        else:
            new_cards.append(c)
    suits = [card[-1] for card in new_cards]
    ranks = [int(card[:-1]) for card in new_cards]
    unique_ranks = len(set(ranks))
    unique_suits = len(set(suits))
    rank_frequency = {r: ranks.count(r) for r in set(ranks)}
    repeated_ranks = sum(1 for r in rank_frequency.values() if r > 1)
    suit_frequency = {s: suits.count(s) for s in set(suits)}
    repeated_suits = sum(1 for s in suit_frequency.values() if s > 1)
    return {
        "cards": new_cards,
        "suits": suits,
        "ranks": ranks,
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
            return ((two*2) + (math.comb((data["unique_ranks"] - two), 2)*3)) / (52 - len(cards))
            # two card combinations of non repeated cards * 3 / total cards in deck
        elif data["remaining_cards"] == 1:
            return (two*2) / (52 - len(cards))

def get_longest_sequence(cards):
    data = process(cards)
    values = data["ranks"]
    cards_wrt_ranks = {}
    for c in data["cards"]:
        rank = int(c[:-1])
        if rank not in cards_wrt_ranks:
            cards_wrt_ranks.update({
                rank:[c[-1]]
            })
        else:
            cards_wrt_ranks[rank].append(c[-1])
    if 14 in values:
        values.append(1)  # Consider Ace as both high and low
        cards_wrt_ranks.update({
            1: cards_wrt_ranks[14]
        })

    values = sorted(set(values))
    cards_wrt_ranks = {v: cards_wrt_ranks[v] for v in values}

    max_length = 1
    current_length = 1
    longest_sequence = []
    current_sequence = [values[0]]
    
    for i in range(1, len(values)):
        if values[i] == values[i - 1] + 1:
            current_length += 1
            current_sequence.append(values[i])
        else:
            if current_length > max_length:
                max_length = current_length
                longest_sequence = current_sequence
            current_length = 1
            current_sequence = [values[i]]
    
    # Final check at the end of the loop
    if current_length > max_length:
        longest_sequence = current_sequence
    
    most_frequent_suit = ''
    for s in ['s', 'c', 'h', 'd']:
        ctr = 0
        max_ctr = 0
        for i in longest_sequence:
            if s in cards_wrt_ranks[i]:
                ctr += 1
        if ctr > max_ctr:
            max_ctr = ctr
            most_frequent_suit = s

    final_longest_sequence = []
    for i in longest_sequence:
        s = most_frequent_suit if most_frequent_suit in cards_wrt_ranks[i] else cards_wrt_ranks[i][0]
        final_longest_sequence.append(f"{i}{s}")

    return final_longest_sequence

def straight(cards):
    data = process(cards)
    rank = "23456789TJQKA"
    suit = "csdh"
    deck = [r+s for r in rank for s in suit]
    deck = [card for card in deck if card not in cards]
    if len(get_longest_sequence(cards)) >= 5:
        return 1.0
    if not data["remaining_cards"]:
        return 0.0
    possible_cards = list(combinations(deck, data["remaining_cards"]))
    total = 0
    straights = 0
    for c in possible_cards:
        if len(get_longest_sequence(list(c)+cards)) >= 5:
            straights += 1
        total += 1
    return straights / total

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
    longest_sequence = get_longest_sequence(cards)
    longest_sequence_suits = [i[-1] for i in longest_sequence]
    if len(longest_sequence) >= 5:
        if len(set(longest_sequence_suits)) == 1:
            return 1.0
    if not data["remaining_cards"]:
        return 0.0
    possible_cards = list(combinations(deck, data["remaining_cards"]))
    total = 0
    straights = 0
    for c in possible_cards:
        longest_sequence = get_longest_sequence(list(c)+cards)
        longest_sequence_suits = [i[-1] for i in longest_sequence]
        if len(longest_sequence) >= 5:
            if len(set(longest_sequence_suits)) == 1:
                straights += 1
        total += 1
    return straights / total
    
def royal_flush(cards):
    data = process(cards)
    rank = "23456789TJQKA"
    suit = "csdh"
    deck = [r+s for r in rank for s in suit]
    deck = [card for card in deck if card not in cards]
    longest_sequence = get_longest_sequence(cards)
    longest_sequence_suits = [i[-1] for i in longest_sequence]
    if len(longest_sequence) >= 5:
        if len(set(longest_sequence_suits)) == 1:
            if longest_sequence[-1][:-1] == "14" and longest_sequence[-5][:-1] == "10":
                return 1.0
    if not data["remaining_cards"]:
        return 0.0
    possible_cards = list(combinations(deck, data["remaining_cards"]))
    total = 0
    straights = 0
    for c in possible_cards:
        longest_sequence = get_longest_sequence(list(c)+cards)
        longest_sequence_suits = [i[-1] for i in longest_sequence]
        if len(longest_sequence) >= 5:
            if len(set(longest_sequence_suits)) == 1:
                if longest_sequence[-1][:-1] == "14" and longest_sequence[-5][:-1] == "10":
                    straights += 1
        total += 1
    return straights / total

def equity(hole_cards, community_cards):
    # call only on flop and turn
    cards = list(hole_cards + community_cards)
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

if __name__ == "__main__":
    comm_cards = ["8s", "7c", "9c"]
    hole = ["Ah", "5h"]
    print(equity(hole, comm_cards))