import ctypes
import os

# Get the absolute path to the current directory
base_dir = os.path.dirname(os.path.abspath(__file__))
libpheval_path = os.path.join(base_dir, 'build', 'libpheval.so.0.6.0')
wrapper_path = os.path.join(base_dir, 'wrapper.so')

# Preload libpheval.so.0.6.0
libpheval = ctypes.CDLL(libpheval_path)

# Load the wrapper shared library
lib = ctypes.CDLL(wrapper_path)

# Define function prototypes
lib.evaluate5_cards.argtypes = [
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
    ctypes.c_char_p, ctypes.c_char_p
]
lib.evaluate5_cards.restype = ctypes.c_int

lib.evaluate6_cards.argtypes = [
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p
]
lib.evaluate6_cards.restype = ctypes.c_int

lib.evaluate7_cards.argtypes = [
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
    ctypes.c_char_p
]
lib.evaluate7_cards.restype = ctypes.c_int

# Python functions to call the C++ functions


def evaluate_cards(card1, card2, card3, card4, card5, card6=None, card7=None):
    if card6 is not None:
        if card7 is not None:
            return lib.evaluate7_cards(
                card1.encode(), card2.encode(), card3.encode(),
                card4.encode(), card5.encode(), card6.encode(), card7.encode()
            )
        return lib.evaluate6_cards(
            card1.encode(), card2.encode(), card3.encode(),
            card4.encode(), card5.encode(), card6.encode()
        )
    return lib.evaluate5_cards(
        card1.encode(), card2.encode(), card3.encode(),
        card4.encode(), card5.encode()
    )


if __name__ == "__main__":
    # Example usage
    result5 = evaluate_cards("Ah", "Kh", "Qh", "Jh", "4h")
    print("Result of evaluate5_cards:", result5)

    result6 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "Qc")
    print("Result of evaluate6_cards:", result6)

    result7 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "Qc", "6c")
    print("Result of evaluate7_cards:", result7)
