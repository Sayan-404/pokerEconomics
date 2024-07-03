#include <iostream>
#include <thread>
#include <vector>
#include <chrono>
#include <iomanip>
#include <iterator>
#include <mutex>
#include <fstream>
#include <unordered_map>
#include <algorithm>

#include "hand_potential.h"
// #include <nlohmann/json.hpp>
// #include "utils/combinations.h"

// using json = nlohmann::json;
std::mutex mtx; // Mutex to protect console output

void print_progress(int thread_id, int progress, double it_per_sec, double eta);
std::vector<std::string> create_deck();
void updateBar(std::chrono::time_point<std::chrono::high_resolution_clock> start_time, int thread_id, int present_iteration, int total_iterations);
void parentWorker(int thread_id, std::vector<std::vector<std::string>> &thread_combos);
std::vector<std::vector<std::string>> generateCombinations(const std::vector<std::string> &elements, int r);
std::vector<std::vector<std::string>> vectorSlice(std::vector<std::vector<std::string>> &arr, int X, int Y);
int *cardsToNumbers(const std::vector<std::string> &cards);

int main()
{
    int numThreads;
    int totalCalls;

    std::cout << "Enter number of threads/processes: ";
    std::cin >> numThreads;

    std::cout << "Enter number of total calls: ";
    std::cin >> totalCalls;

    std::vector<std::string> deck = create_deck();
    std::vector<std::vector<std::string>> flopCombos = generateCombinations(deck, 3);

    // Include only the totalCalls
    flopCombos = vectorSlice(flopCombos, 0, totalCalls);

    // Subdivide the combinations into numThreads number of groups
    std::vector<std::vector<std::vector<std::string>>>
        thread_combos(numThreads);
    for (int i = 0; i < totalCalls; ++i)
    {
        thread_combos[i % numThreads].push_back(flopCombos[i]);
    }

    std::vector<std::thread> threads;

    std::cout << "Starting threads...\n";

    // Move cursor to start of the screen and clear the screen
    std::cout << "\033[H\033[J";

    // Start the threads
    for (int i = 0; i < numThreads; ++i)
    {
        threads.emplace_back(parentWorker, i, std::ref(thread_combos[i]));
    }

    // Wait for all threads to finish
    for (auto &t : threads)
    {
        t.join();
    }

    std::cout << "\n\nAll threads completed.\n";

    return 0;
}

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

void parentWorker(int thread_id, std::vector<std::vector<std::string>> &thread_combos)
{
    using namespace std::chrono;

    auto start_time = high_resolution_clock::now(); // Start time

    int iterations = thread_combos.size();

    for (int i = 0; i <= iterations; ++i)
    {
        try
        {
            /* code */
            int *cards = cardsToNumbers(thread_combos[i]);

            int hole_cards[2] = {cards[0], cards[1]};
            int comm_cards[3] = {cards[2], cards[3], cards[4]};

            potentials pot = potential2(hole_cards, comm_cards);

            updateBar(start_time, thread_id, i, iterations);
        }
        catch (const std::exception &e)
        {
            std::cerr << e.what() << '\n';
        }
    }
}

// Function to generate combinations
std::vector<std::vector<std::string>> generateCombinations(const std::vector<std::string> &elements, int r)
{
    std::vector<std::vector<std::string>> combinations;

    if (r > elements.size() || r <= 0)
        return combinations;

    std::vector<bool> v(elements.size());
    std::fill(v.begin(), v.begin() + r, true);

    do
    {
        std::vector<std::string> combination;
        for (size_t i = 0; i < elements.size(); ++i)
        {
            if (v[i])
                combination.push_back(elements[i]);
        }
        combinations.push_back(combination);
    } while (std::prev_permutation(v.begin(), v.end()));

    return combinations;
}

// Function to slice a given vector
// from range X to Y
std::vector<std::vector<std::string>> vectorSlice(std::vector<std::vector<std::string>> &arr, int X, int Y)
{

    // Starting and Ending iterators
    auto start = arr.begin() + X;
    auto end = arr.begin() + Y + 1;

    // To store the sliced vector
    std::vector<std::vector<std::string>> result(Y - X + 1);

    // Copy vector using copy function()
    copy(start, end, result.begin());

    // Return the final sliced vector
    return result;
}

// Function to convert a vector of card strings to a C-compatible array of numerical representations
int *cardsToNumbers(const std::vector<std::string> &cards)
{
    // Define rank mappings
    std::unordered_map<char, int> rankMap = {
        {'2', 0}, {'3', 1}, {'4', 2}, {'5', 3}, {'6', 4}, {'7', 5}, {'8', 6}, {'9', 7}, {'T', 8}, {'J', 9}, {'Q', 10}, {'K', 11}, {'A', 12}};

    // Define suit mappings
    std::unordered_map<char, int> suitMap = {
        {'c', 0}, {'d', 1}, {'h', 2}, {'s', 3}};

    // Allocate memory for the result array
    int *cardNumbers = new int[cards.size()];

    for (size_t i = 0; i < cards.size(); ++i)
    {
        const std::string &card = cards[i];

        if (card.length() != 2)
        {
            std::cerr << "Invalid card format: " << card << std::endl;
            cardNumbers[i] = -1;
            continue;
        }

        char rank = card[0];
        char suit = card[1];

        if (rankMap.find(rank) == rankMap.end() || suitMap.find(suit) == suitMap.end())
        {
            std::cerr << "Invalid card rank or suit: " << card << std::endl;
            cardNumbers[i] = -1;
            continue;
        }

        int rankValue = rankMap[rank];
        int suitValue = suitMap[suit];

        cardNumbers[i] = rankValue * 4 + suitValue;
    }

    return cardNumbers;
}
