import ctypes

# Load the shared library
lib = ctypes.CDLL('./potential.so')

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


# Example usage
hole = [12, 25]  # Example hole cards
comm_cards = [2, 17, 30]  # Example community cards

ppot, npot = potential2(hole, comm_cards)
print(f"ppot: {ppot}, npot: {npot}")
