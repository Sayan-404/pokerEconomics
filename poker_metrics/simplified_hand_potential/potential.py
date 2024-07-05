import ctypes
import os

# Get the absolute path to the current directory
base_dir = os.path.dirname(os.path.abspath(__file__))
libpheval_path = os.path.join(base_dir, 'build', 'libpheval.so.0.6.0')
wrapper_path = os.path.join(base_dir, 'potential.so')

# Preload libpheval.so.0.6.0
libpheval = ctypes.CDLL(libpheval_path)

# Load the wrapper shared library
lib = ctypes.CDLL(wrapper_path)

# Define the struct for potentials


class Potentials(ctypes.Structure):
    _fields_ = [("ppot", ctypes.c_float),
                ("npot", ctypes.c_float)]


# Define the function prototype
lib.potential2.argtypes = [ctypes.POINTER(
    ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
lib.potential2.restype = Potentials


def cleanCard(card):
    # Define rank and suit mappings
    rank_map = {
        '2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5,
        '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12
    }
    suit_map = {
        'c': 0, 'd': 1, 'h': 2, 's': 3
    }
    # Extract rank and suit from the card string
    rank = card[0]
    suit = card[1]
    # Calculate numeric representation
    rank_value = rank_map[rank]
    suit_value = suit_map[suit]
    numeric_value = rank_value * 4 + suit_value
    return numeric_value


def potential2(hole, comm_cards):
    hole = [int(cleanCard(card)) for card in hole]
    comm_cards = [int(cleanCard(card)) for card in comm_cards]
    # Convert input lists to ctypes arrays
    hole_array = (ctypes.c_int * len(hole))(*hole)
    comm_cards_array = (ctypes.c_int * len(comm_cards))(*comm_cards)

    result = wrapper(hole_array, comm_cards_array)
    return result


def wrapper(hole, comm_cards):
    # Call the C function
    result = lib.potential2(hole, comm_cards)
    return result.ppot, result.npot


if __name__ == "__main__":
    # Example usage
    hole = ['Qc', '6c']  # Example hole cards
    comm_cards = ['9c', '4c', '4s']  # Example community cards
    ppot, npot = potential2(hole, comm_cards)
    print(f"ppot: {ppot}, npot: {npot}")
