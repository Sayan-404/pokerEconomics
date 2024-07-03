import json
import multiprocessing
from tqdm import tqdm
from itertools import combinations

import ctypes

ranks = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5,
         '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
suits = {'c': 0, 'd': 1, 'h': 2, 's': 3}

# Load the shared library
lib_path = './multi'

lib = ctypes.CDLL(lib_path)

# Define the argument and return types of the `potential2` function
# potentials is a struct with two floats


class Potentials(ctypes.Structure):
    _fields_ = [("ppot", ctypes.c_float), ("npot", ctypes.c_float)]


lib.potential2.argtypes = [ctypes.POINTER(
    ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
lib.potential2.restype = Potentials


def card_to_value(card):
    """
    Convert a card string to its integer representation.

    Parameters:
    card (str): A string representing the card, e.g., 'Qc' or '9h'.

    Returns:
    int: The integer representation of the card.
    """
    rank, suit = card[0], card[1]
    return ranks[rank] * 4 + suits[suit]


def potential2(hole, comm_cards):
    # Convert card strings to integer values
    hole_int_array = [card_to_value(card) for card in hole]
    comm_int_array = [card_to_value(card) for card in comm_cards]

    result = lib.potential2(hole_int_array, comm_int_array)
    return result

# get combinations for specified range in 52c5 combinations
# create dictionary with potential for sorted combinations of 5 cards and 6 cards (sort)

# create deck
# get 52c5 combinations
# divide total range


def p(full_deck, cards_range, id):
    data = {}
    for i in tqdm(range(len(cards_range)), desc=f"Process ##{id} ", position=id):
        cards = cards_range[i]
        deck = [card for card in full_deck if card not in cards]
        p = potential2(cards[:2], cards[2:])
        data.update({
            tuple(cards): p
        })
    return data


def run():
    processes = int(input("Enter number of processes: "))
    suits = ["h", "d", "c", "s"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    deck = [rank + suit for suit in suits for rank in ranks]
    r = int(input("Enter 0 for flop and 1 for turn: "))
    possible_range = [sorted(list(comb)) for comb in combinations(deck, 5+r)]
    # possible_range = [sorted(cards) for cards in possible_range]
    # print(possible_range)
    possible_range.sort()
    total_range = len(possible_range)
    # processes-1 number of processes each handling a range of size batch_size
    # last process handling process of rest
    input_range = int(
        input(f"Enter range between 1 and {total_range} (0 for full range): "))
    if input_range == 0:
        input_range = total_range

    # split the range into batches for each process
    batch_size = input_range // processes
    batches = [
        possible_range[i * batch_size:(i + 1) * batch_size] for i in range(processes)]
    if input_range % processes != 0:
        batches.append(possible_range[processes * batch_size:])

    pool = multiprocessing.Pool(processes)
    results = [pool.apply_async(p, args=(deck, batch, i))
               for i, batch in enumerate(batches)]

    pool.close()
    pool.join()

    final_data = {}
    for result in results:
        final_data.update(result.get())

    return final_data


if __name__ == "__main__":
    final_data = run()
    with open("final_data.json", "w") as f:
        json.dump(final_data, f, indent=4)
    print("Data saved to final_data.json")
    # Optionally, you can save final_data to a file or process it further
