def chen_formula(hand):
    ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    score = 0
    
    # Extract card ranks and suits
    card_ranks = [card[0] for card in hand]
    card_suits = [card[1] for card in hand]
    
    # Check if the hand is suited
    is_suited = len(set(card_suits)) == 1
    
    # Calculate score based on highest card value
    score += ranks[max(card_ranks)]
    
    # Adjust score based on pairs or connectedness
    if card_ranks[0] == card_ranks[1]:
        score *= 2  # Add bonus for pairs
    elif abs(ranks[card_ranks[0]] - ranks[card_ranks[1]]) == 1:
        score += 1  # Add bonus for connected cards
    elif abs(ranks[card_ranks[0]] - ranks[card_ranks[1]]) == 2:
        score += 0.5  # Add bonus for gapped connectors
        
    # Adjust score for suitedness
    if is_suited:
        score += 2
    
    return score

# Test the chen_formula function with a sample hand
hand = ['Ah', 'Ks']  # Example hand: Ace of hearts, King of spades
strength = chen_formula(hand)
print("Hand strength score:", strength)

