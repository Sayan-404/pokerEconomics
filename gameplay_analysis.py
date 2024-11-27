import json
import os
import argparse
from collections import defaultdict

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Process poker hand files and analyze betting stats.")
parser.add_argument("directory", type=str, help="Directory path containing hand JSON files")
args = parser.parse_args()

# Initialize stats dictionary
stats = defaultdict(lambda: defaultdict(list))

# Process each file in the directory
for filename in os.listdir(args.directory):
    if filename.endswith(".json"):  # Ensure only JSON files are processed
        filepath = os.path.join(args.directory, filename)
        with open(filepath, "r") as file:
            try:
                hand_data = json.load(file)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON file: {filename}")
                continue
            
            # Iterate through each phase of the game
            for phase in ["pre-flop", "flop", "turn", "river"]:
                if phase in hand_data:
                    for action in hand_data[phase].get("betting", []):
                        player = action["player"]
                        action_type = action["action"]
                        
                        # Accumulate actions
                        stats[player][action_type].append(action["bet"])

# Display statistics for specified players
for player in stats:
    print(f"{player} Stats:")
    print(
        f"F: {len(stats[player].get('f', []))}",
        f"C: {len(stats[player].get('c', []))}",
        f"Ch: {len(stats[player].get('ch', []))}",
        f"B: {len(stats[player].get('b', []))}",
        f"R: {len(stats[player].get('r', []))}"
    )
    print()

# Calculate and print aggression stats for each player
for player in stats:
    frugal_actions = len(stats[player].get("c", [])) + len(stats[player].get("ch", [])) + len(stats[player].get("f", []))
    prodigal_actions = len(stats[player].get("b", [])) + len(stats[player].get("r", []))
    total_actions = frugal_actions + prodigal_actions

    # Compute Frugality Ratio
    frugality_ratio = prodigal_actions / frugal_actions if frugal_actions > 0 else float("inf")

    # Compute Aggression (Weighted)
    total_bets = sum(stats[player].get("c", [])) + sum(stats[player].get("ch", [])) + sum(stats[player].get("f", [])) + \
                 sum(stats[player].get("b", [])) + sum(stats[player].get("r", []))
    aggression = ((sum(stats[player].get("b", []) + stats[player].get("r", [])) * prodigal_actions) - 
                  (sum(stats[player].get("c", []) + stats[player].get("ch", []) + stats[player].get("f", [])) * frugal_actions)) / \
                 (total_bets * total_actions) if total_bets > 0 else 0

    print(f"{player} Frugality Ratio: {frugality_ratio:.2f}")
    print(f"{player} Aggression: {aggression:.2f}")
    print()
