def find_repeated_sequences(arr):
    if not arr:
        return []

    repeated_sequences = []
    current_sequence = [arr[0]]

    for i in range(1, len(arr)):
        if arr[i] == arr[i - 1]:
            current_sequence.append(arr[i])
        else:
            if len(current_sequence) > 1:
                repeated_sequences.append(current_sequence)
            current_sequence = [arr[i]]

    # Final check to add the last sequence if it's a repeated one
    if len(current_sequence) > 1:
        repeated_sequences.append(current_sequence)

    return repeated_sequences

# Example usage:
arr = [5, 9, 10, 13]
print("All sequences of repeated numbers:", find_repeated_sequences(arr))
