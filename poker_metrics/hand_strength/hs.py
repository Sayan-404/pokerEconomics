import ctypes

# Load the shared library
lib = ctypes.CDLL('./hs.so')  # Adjust the path and filename

# Define the argument and return types for the functions
lib.calculate_card_value.argtypes = [ctypes.c_int, ctypes.c_int]
lib.calculate_card_value.restype = ctypes.c_int

lib.create_probabilistic_score.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
lib.create_probabilistic_score.restype = ctypes.c_double

# Define constants for card ranks and suits
ranks = "23456789TJQKA"
suits = "scdh"

def card_to_value(card):
    """Convert a card string to its integer value."""
    rank_str = card[0]
    suit_str = card[1]
    rank = ranks.index(rank_str) + 2  # +2 because card ranks start at 2
    suit = suits.index(suit_str)
    return lib.calculate_card_value(rank, suit)

def handStrength(hole_cards, community_cards=[]):
    """Calculate the strength of the hand given hole and community cards."""
    # Convert cards to their integer values
    hole_values = [card_to_value(card) for card in hole_cards]
    community_values = [card_to_value(card) for card in community_cards]
    
    # Prepare ctypes arrays for the C function
    hole_array = (ctypes.c_int * len(hole_values))(*hole_values)
    community_array = (ctypes.c_int * len(community_values))(*community_values)
    
    # Call the C function to get the hand strength
    strength = lib.create_probabilistic_score(hole_array, len(hole_values), community_array, len(community_values))
    
    return strength

if __name__ == "__main__":
    # Example usage
    # hole = ["As", "7d"]
    # community = ["8h", "3c", "2s", "Kc"]

    hole = ["Ad", "Kd"]
    community = ["Qd", "Jd", "Td", "Kc"]

    print("Hand Strength:", handStrength(hole, community))
