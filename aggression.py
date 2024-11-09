import json
import argparse
import os

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Process poker hand files and analyze betting stats.")
parser.add_argument("directory", type=str, help="Directory path containing hand JSON files")
args = parser.parse_args()

# Initialize stats dictionary
stats = {}
hands = []

# Load each hand JSON file from the specified directory
for i in range(100000):
    filepath = os.path.join(args.directory, f"hand_{i}.json")
    try:
        with open(filepath, "r") as f:
            hand_obj = json.load(f)
            hands.append([
                hand_obj['pre-flop'],
                hand_obj['flop'],
                hand_obj['turn'],
                hand_obj['river'],
            ])
    except FileNotFoundError:
        print(f"File {filepath} not found. Stopping at file {i-1}.")
        break

# Process each hand and calculate stats
for hand in hands:
    for round in hand:
        for bet in round["betting"]:
            player = bet["player"]
            action = bet["action"]

            if player not in stats:
                stats[player] = {}

            if action not in stats[player]:
                stats[player][action] = []

            if action in ['c', 'f']:
                stats[player][action].append(bet.get("callsize", 0))
            else:
                stats[player][action].append(bet.get("bet", 0))

# Display statistics for specified players
for player in ["Sourjya", "Sayan"]:
    if player in stats:
        print(f"{player} Stats:")
        print(
            'F: ' + str(len(stats[player].get('f', []))),
            'C: ' + str(len(stats[player].get('c', []))),
            'Ch: ' + str(len(stats[player].get('ch', []))),
            'B: ' + str(len(stats[player].get('b', []))),
            'R: ' + str(len(stats[player].get('r', [])))
        )
    else:
        print(f"No data found for player {player}")

print()

# Calculate and print aggression stats for each player
for player in stats:
    frugal_bets = stats[player].get('c', []) + stats[player].get('ch', []) + stats[player].get('f', [])
    prodigal_bets = stats[player].get('b', []) + stats[player].get('r', [])

    if frugal_bets and prodigal_bets:
        aggression = ((sum(prodigal_bets) * len(prodigal_bets)) - (sum(frugal_bets) * len(frugal_bets))) / \
                     (sum(prodigal_bets + frugal_bets) * len(frugal_bets + prodigal_bets))

        print(f"{player} Frugality Ratio: {sum(prodigal_bets) / sum(frugal_bets):.2f}")
        print(f"{player} Aggression: {aggression:.2f}")
        print()
