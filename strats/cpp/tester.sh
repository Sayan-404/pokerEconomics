#!/bin/bash

# Initialize variables
total_time=0
count=0

# Run the script 100 times
for ((i=1; i<=100; i++)); do
    # Measure the execution time
    start_time=$(date +%s%N)
    "./hand_potential"
    end_time=$(date +%s%N)

    # Calculate the execution time in nanoseconds
    execution_time=$((end_time - start_time))

    # Add the execution time to the total
    total_time=$((total_time + execution_time))

    # Increment the count
    count=$((count + 1))
done

# Calculate the average time
average_time=$((total_time / count))

# Convert nanoseconds to seconds
total_time_seconds=$((total_time / 1000000000))
average_time_seconds=$((average_time / 1000000000))

# Print the results
echo "Total time taken for 100 runs: $total_time_seconds seconds"
echo "Average time per run: $average_time_seconds seconds"

