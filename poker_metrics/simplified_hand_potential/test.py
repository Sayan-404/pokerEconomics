import potential as pt


def potential2(hole, comm_cards):
    return pt.potential2(tuple(hole), tuple(comm_cards))


if __name__ == "__main__":
    hole = [12, 25]  # Example hole cards
    comm_cards = [2, 17, 30]  # Example community cards

    ppot, npot = potential2(hole, comm_cards)
    print(f"ppot: {ppot}, npot: {npot}")
