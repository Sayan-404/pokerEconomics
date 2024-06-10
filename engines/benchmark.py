import multiprocessing
import time
import os
from engine import initialise_run

def worker(n):
    game = initialise_run("benchmark_config")
    game.play(True)
    time.sleep(0.01)
    return n * n

def adaptive_benchmark(multiplier=10):
    num_cores = os.cpu_count()
    best_time = float('inf')
    best_num_processes = 1

    for num_processes in range(1, num_cores * multiplier):
        start_time = time.time()
        with multiprocessing.Pool(num_processes) as pool:
            _ = pool.map(worker, range(100))
        end_time = time.time()
        duration = end_time - start_time

        if duration < best_time:
            best_time = duration
            best_num_processes = num_processes

        print(f"Time taken with {num_processes} processes: {duration:.2f} seconds")

    print(f"Optimal number of processes: {best_num_processes}")
    return best_num_processes

def average_best_num_processes(multiplier=10, period=3):
    return round(sum([adaptive_benchmark(multiplier) for _ in range(period)])/period)

if __name__ == "__main__":
    print(average_best_num_processes(15))
