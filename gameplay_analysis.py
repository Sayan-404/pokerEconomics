import json
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Process poker hand files and analyze betting stats.")
parser.add_argument("directory", type=str, help="Directory path containing hand JSON files")
args = parser.parse_args()

# Initialize stats dictionary
stats = {}
player = []

with open(args.directory, 'r') as f:
    stats = json.load(f)

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

        print(f"{player} Frugality Ratio: {len(prodigal_bets) / len(frugal_bets):.2f}")
        print(f"{player} Aggression: {aggression:.2f}")
        print()
