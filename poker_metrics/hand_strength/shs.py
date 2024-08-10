import ctypes
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the shared library
lib_path = os.path.join(script_dir, 'hs.so')

# Load the shared library
hs_lib = ctypes.CDLL(lib_path)

# Define the argument and return types of the handStrength function
hs_lib.handStrength.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int,
                                ctypes.POINTER(ctypes.c_int), ctypes.c_int)
hs_lib.handStrength.restype = ctypes.c_double

def card_to_int(card):
    rank_map = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
    suit_map = {'c': 0, 'd': 1, 'h': 2, 's': 3}
    return rank_map[card[0]] * 4 + suit_map[card[1]]

def handStrength(hole, board):
    hole = [card_to_int(card) for card in hole]
    board = [card_to_int(card) for card in board]

    hole_arr = (ctypes.c_int * len(hole))(*hole)
    board_arr = (ctypes.c_int * len(board))(*board)
    return hs_lib.handStrength(hole_arr, len(hole), board_arr, len(board))
