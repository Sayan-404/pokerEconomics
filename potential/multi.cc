#include <iostream>
#include <thread>
#include <vector>
#include <chrono>
#include <iomanip>
#include <iterator>
#include <mutex>
#include <fstream>
// #include <nlohmann/json.hpp>
// #include "utils/combinations.h"

// using json = nlohmann::json;
std::mutex mtx; // Mutex to protect console output

void print_progress(int thread_id, int progress, double it_per_sec, double eta)
{
    std::lock_guard<std::mutex> guard(mtx); // Ensure exclusive access to console

    // Move cursor to the appropriate line for this thread
    std::cout << "\033[" << thread_id + 1 << ";0H";

    // Print the progress bar
    std::cout << "Thread " << thread_id << ": [";
    int bar_width = 50;
    int pos = bar_width * progress / 100;
    for (int i = 0; i < bar_width; ++i)
    {
        if (i < pos)
            std::cout << "#";
        else
            std::cout << " ";
    }
    std::cout << "] " << progress << "% ";

    // Print it/s and ETA
    std::cout << std::fixed << std::setprecision(2);
    std::cout << it_per_sec << " it/s ETA: " << eta << " s";

    std::cout.flush(); // Ensure the output is printed immediately
}

std::vector<std::string> create_deck()
{
    std::vector<std::string> suits = {"h", "d", "c", "s"};
    std::vector<std::string> ranks = {"2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"};
    std::vector<std::string> deck;
    for (const auto &suit : suits)
    {
        for (const auto &rank : ranks)
        {
            deck.push_back(rank + suit);
        }
    }
    return deck;
}

void childWorker()
{
    /*
        Worker function for multi-threading.
    */
   int a = 1+1;
}

void updateBar(std::chrono::time_point<std::chrono::high_resolution_clock> start_time, int thread_id, int present_iteration, int total_iterations)
{
    using namespace std::chrono;

    auto now = high_resolution_clock::now();
    duration<double> elapsed = now - start_time;
    double elapsed_sec = elapsed.count();
    double it_per_sec = present_iteration / elapsed_sec;
    double eta = (total_iterations - present_iteration) / it_per_sec;

    print_progress(thread_id, present_iteration, it_per_sec, eta);
}

void parentWorker(int thread_id)
{
    using namespace std::chrono;

    auto start_time = high_resolution_clock::now(); // Start time

    int iterations = 100;

    for (int i = 0; i <= iterations; ++i)
    {
        childWorker();
        updateBar(start_time, thread_id, i, iterations);
    }
}

int main()
{
    int numThreads;

    std::cout << "Enter number of threads: ";
    std::cin >> numThreads;

    // std::vector<std::string> deck = create_deck();

    // int r;
    // std::cout << "Enter 0 for flop and 1 for turn: ";
    // std::cin >> r;

    // // std::vector<std::vector<std::string>> possible_range = generateCombinations(deck, r);

    // // Print the generated combinations
    // for (const auto &combo : deck)
    // {
    //     for (const auto &card : combo)
    //     {
    //         std::cout << card << " ";
    //     }
    //     std::cout << std::endl;
    // }

    std::vector<std::thread> threads;

    std::cout << "Starting threads...\n";

    // Move cursor to start of the screen and clear the screen
    std::cout << "\033[H\033[J";

    // Start the threads
    for (int i = 0; i < numThreads; ++i)
    {
        threads.emplace_back(parentWorker, i);
    }

    // Wait for all threads to finish
    for (auto &t : threads)
    {
        t.join();
    }

    std::cout << "\n\nAll threads completed.\n";

    return 0;
}
