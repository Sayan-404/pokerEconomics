from Deck import Deck
from strats.hand_potential import potential

import time
d = Deck()
d.create_deck()
d.shuffle()
deck = [str(card) for card in d.cards]
hole = [deck.pop() for _ in range(2)]
community_cards = [deck.pop() for _ in range(3)]
print()
for _ in range(5):
    a = time.time()
    p = potential(deck, hole, community_cards)
    b = time.time()
    print(b-a)
print()
print(p[0])
print(p[1])