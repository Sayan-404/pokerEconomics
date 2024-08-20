import json
import multiprocessing
import os
import subprocess
import time

from utils import initialise_run_config


def worker(_):
    game = initialise_run_config("benchmark_config", benchmark=True)
    game.play(True)

def adaptive_benchmark(multiplier=10):
    data = {}
    with open(f"configs/benchmark_config.json", "r") as f:
        data = json.load(f)
    runs = data["runs"]
    num_cores = os.cpu_count()
    best_time = float('inf')
    best_num_processes = 1
    best_its = 0
    best_its_processes = 1
    for num_processes in range(1, num_cores * multiplier):
        start_time = time.time()
        with multiprocessing.Pool(num_processes) as pool:
            _ = pool.map(worker, range(num_processes))
        end_time = time.time()
        duration = end_time - start_time

        if duration < best_time:
            best_time = duration
            best_num_processes = num_processes

        its = (num_processes*runs)/duration
        if its > best_its:
            best_its = its
            best_its_processes = num_processes
        print(f"Time taken with {num_processes} processes: {duration:.2f} seconds")
        print(f"Net iterations/second: {its}")

    print(f"\nOptimal number of processes: {best_num_processes} which took {best_time} seconds.")
    print(f"Best recorded iterations/second: {best_its} for {best_its_processes} processes\n")
    return best_num_processes, (best_its, best_its_processes)

def average_best_num_processes(multiplier=10, period=3):
    ret = [adaptive_benchmark(multiplier) for _ in range(period)]
    avg_proc = round(sum([r[0] for r in ret])/period)
    print("Iterations/second     Processes")
    for r in ret:
        print(f"{r[1][0]}     {r[1][1]}")
    print(f"Best Result: {avg_proc} processes.")

if __name__ == "__main__":
    multiplier = int(input("Enter multiplier: "))
    average_best_num_processes(multiplier)
    print("Cleaning up .....")
    _ = subprocess.Popen("rm -rf data/b_*/", shell=True)