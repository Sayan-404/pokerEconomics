#include <iostream>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <cmath>
#include <cstring>
#include "hand_potential.h"

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

    // Sorting the deck
    std::sort(deck.begin(), deck.end());

    return deck;
}

std::vector<long long> generate_first_n_primes(int n)
{
    std::vector<long long> primes;
    long long num = 2; // The first prime number
    while (primes.size() < n)
    {
        bool isPrime = true;
        for (long long i = 2; i <= std::sqrt(num); ++i)
        {
            if (num % i == 0)
            {
                isPrime = false;
                break;
            }
        }
        if (isPrime)
        {
            primes.push_back(num);
        }
        ++num;
    }
    return primes;
}

std::unordered_map<std::string, long long> create_card_prime_map(const std::vector<std::string> &deck, const std::vector<long long> &primes)
{
    std::unordered_map<std::string, long long> cardPrimeMap;
    for (size_t i = 0; i < deck.size(); ++i)
    {
        cardPrimeMap[deck[i]] = primes[i];
    }
    return cardPrimeMap;
}

int main()
{
    std::vector<std::string> deck = create_deck();
    std::vector<long long> primes = generate_first_n_primes(52);

    std::unordered_map<std::string, long long> cardPrimeMap = create_card_prime_map(deck, primes);

    // Select example hole cards and community cards
    std::string hole_cards[] = {deck[0], deck[1]};
    std::string community_cards[] = {deck[2], deck[3], deck[4], deck[5], deck[6]};

    // Convert hole cards to C-style char arrays
    char hole[2][3];
    for (int i = 0; i < 2; ++i) {
        std::strcpy(hole[i], hole_cards[i].c_str());
    }

    // Convert community cards to C-style char arrays
    char comm_cards[5][3];
    for (int i = 0; i < 5; ++i) {
        std::strcpy(comm_cards[i], community_cards[i].c_str());
    }

    // Call the C function
    potentials result = potential2(hole, comm_cards);
    std::cout << result.ppot << std::endl;
    std::cout << result.npot << std::endl;

    return 0;
}
