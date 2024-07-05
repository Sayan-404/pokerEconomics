import ctypes
import os

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


def potential2(hole, comm_cards):
    # Convert input lists to ctypes arrays
    hole_array = (ctypes.c_int * 2)(*hole)
    comm_cards_array = (ctypes.c_int * 3)(*comm_cards)

    # Call the C function
    result = lib.potential2(hole_array, comm_cards_array)

    return result.ppot, result.npot


if __name__ == "__main__":
    # Example usage
    hole = [12, 25]  # Example hole cards
    comm_cards = [2, 17, 30]  # Example community cards

    ppot, npot = potential2(hole, comm_cards)
    print(f"ppot: {ppot}, npot: {npot}")
