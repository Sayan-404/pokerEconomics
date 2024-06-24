from Deck import Deck
from strats.hand_potential import potential
d = Deck()
d.create_deck()
d.shuffle()
deck = [str(card) for card in d.cards]
hole = [deck.pop() for _ in range(2)]
community_cards = [deck.pop() for _ in range(3)]
p = potential(deck, hole, community_cards)
print(p[0])
print(p[1])