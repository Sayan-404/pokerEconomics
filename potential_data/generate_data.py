import json
import multiprocessing
from hand_potential import potential
from tqdm import tqdm
from itertools import combinations

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
        p = potential(deck, cards[:2], cards[-(len(cards) - 2):])
        data.update({
            tuple(cards): p
        })
    return data

def run():
    processes = int(input("Enter number of processes: "))
    suits = ["h", "d", "c", "s"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    deck = [suit + rank for suit in suits for rank in ranks]
    r = int(input("Enter 0 for flop and 1 for turn: "))
    possible_range = list(combinations(deck, 5+r))
    possible_range = [cards.sort() for cards in possible_range]
    possible_range.sort()
    total_range = len(possible_range)
    # processes-1 number of processes each handling a range of size batch_size
    # last process handling process of rest
    input_range = int(input(f"Enter range between 1 and {total_range} (0 for full range): "))
    if input_range == 0:
        input_range = total_range

    # split the range into batches for each process
    batch_size = input_range // processes
    batches = [possible_range[i * batch_size:(i + 1) * batch_size] for i in range(processes)]
    if input_range % processes != 0:
        batches.append(possible_range[processes * batch_size:])

    pool = multiprocessing.Pool(processes)
    results = [pool.apply_async(p, args=(deck, batch, i)) for i, batch in enumerate(batches)]
    
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
